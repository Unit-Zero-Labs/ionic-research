import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pathlib import Path

st.set_page_config(
    page_title="Ionic Emissions Analysis",
    page_icon="📊",
    layout="wide"
)

#  description section
st.title("Ionic Protocol Emissions Analysis")

with st.expander("About this Analysis", expanded=True):
    st.markdown("""
    This dashboard presents analysis of emissions impact on Ionic Protocol metrics. The data tracks changes 
    in supply and borrowing across vaults on Mode, OP, and Base networks, along with emissions tracking and revenue analysis. Currently Base only.
    
    📊 **Data Source**: Data primarily sourced from Dune Analytics. Click the repo for links to queries.
    
    🔍 **View Source**: [Ionic Research Github](https://github.com/Unit-Zero-Labs/ionic-research/tree/main)
    
    *For more details about the analysis methodology and assumptions, please visit the GitHub repository.*
    """)

st.markdown("---")

#  absolute path to the data directory
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = SCRIPT_DIR / "data"

# load CSVs
@st.cache_data
def load_data():
    try:
        emissions_path = DATA_DIR / "ionic_emissions_results.csv"
        vault_path = DATA_DIR / "ionic_vault_analysis.csv"
        age_size_path = DATA_DIR / "ionic_vault_analysis_age_and_size.csv"
        
        if not all(p.exists() for p in [emissions_path, vault_path, age_size_path]):
            raise FileNotFoundError(f"One or more CSV files not found in {DATA_DIR}")
            
        emissions_results = pd.read_csv(emissions_path)
        vault_analysis = pd.read_csv(vault_path)
        age_size_analysis = pd.read_csv(age_size_path)
        return emissions_results, vault_analysis, age_size_analysis
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None

emissions_results, vault_analysis, age_size_analysis = load_data()


if emissions_results is not None and vault_analysis is not None:

    tab1, tab2, tab3 = st.tabs(["Base Vaults", "Vault Analysis", "Raw Data"])

    with tab1:
        # Display key metrics in columns
        metrics = emissions_results.set_index('Metric')['Value']
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total ION Emissions", f"{metrics['Total ION Emissions']:,.2f}")
            st.metric("Days Analyzed", f"{metrics['Days Analyzed']:.0f}")
            st.metric("Daily Emission Rate", f"{metrics['Daily Emission Rate']:,.2f}")
        
        with col2:
            st.metric("Total Deposit Change", f"${metrics['Total Deposit Change ($)']:,.2f}")
            st.metric("Total Borrow Change", f"${metrics['Total Borrow Change ($)']:,.2f}")

        # Create visualization of changes
        st.subheader("Vault Changes Analysis")
        
        # Prepare data for visualization
        vault_analysis_melted = pd.melt(
            vault_analysis.reset_index(),
            id_vars=['vaultName'],
            value_vars=['Deposit Change', 'Borrow Change'],
            var_name='Metric',
            value_name='Change'
        )

        # Create bar chart
        fig = px.bar(
            vault_analysis_melted,
            x='vaultName',
            y='Change',
            color='Metric',
            barmode='group',
            title='Deposit and Borrow Changes by Vault',
            labels={'vaultName': 'Vault', 'Change': 'Change in USD'},
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Vault Analysis Details")
        
        # Create size/age distribution table
        st.subheader("Vault Distribution by Size and Age")
        
        # Calculate the number of vaults in each category
        size_age_dist = pd.crosstab(
            age_size_analysis['Size Category'],
            age_size_analysis['Age Category'],
            values=age_size_analysis['Current Deposits'],
            aggfunc='sum'
        ).round(2)
        
        # Format the values as currency
        size_age_dist = size_age_dist.applymap(lambda x: f"${x:,.2f}")
        
        # Display the crosstab
        st.dataframe(size_age_dist, use_container_width=True)
        
        # Original vault analysis table
        st.subheader("Individual Vault Details")
        formatted_vault_analysis = vault_analysis.copy()
        for col in formatted_vault_analysis.select_dtypes(include=['float64']).columns:
            formatted_vault_analysis[col] = formatted_vault_analysis[col].apply(lambda x: f"${x:,.2f}")
        
        st.dataframe(
            formatted_vault_analysis,
            use_container_width=True,
            height=400
        )

    # Update the tab3 section:
    with tab3:
        st.subheader("Raw Data")
        
        # Create dropdown for CSV selection
        csv_option = st.selectbox(
            'Select CSV to view',
            ('Emissions Results', 'Vault Analysis', 'Age and Size Analysis')
        )
        
        if csv_option == 'Emissions Results':
            st.dataframe(
                emissions_results,
                use_container_width=True,
                height=400
            )
            
            st.download_button(
                label="Download Emissions Results CSV",
                data=emissions_results.to_csv(index=False),
                file_name="ionic_emissions_results.csv",
                mime="text/csv"
            )
        elif csv_option == 'Vault Analysis':
            st.dataframe(
                vault_analysis,
                use_container_width=True,
                height=400
            )
            
            st.download_button(
                label="Download Vault Analysis CSV",
                data=vault_analysis.to_csv(index=False),
                file_name="ionic_vault_analysis.csv",
                mime="text/csv"
            )
        else:  # Age and Size Analysis
            st.dataframe(
                age_size_analysis,
                use_container_width=True,
                height=400
            )
            
            st.download_button(
                label="Download Age and Size Analysis CSV",
                data=age_size_analysis.to_csv(index=False),
                file_name="ionic_vault_analysis_age_and_size.csv",
                mime="text/csv"
            )

