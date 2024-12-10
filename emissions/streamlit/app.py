import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pathlib import Path

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="Ionic Emissions Analysis",
    page_icon="📊",
    layout="wide"
)

# Get the absolute path to the data directory
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = SCRIPT_DIR / "data"

# Load CSVs with explicit error handling
@st.cache_data
def load_data():
    try:
        emissions_path = DATA_DIR / "ionic_emissions_results.csv"
        vault_path = DATA_DIR / "ionic_vault_analysis.csv"
        
        if not emissions_path.exists() or not vault_path.exists():
            raise FileNotFoundError(f"CSV files not found in {DATA_DIR}")
            
        emissions_results = pd.read_csv(emissions_path)
        vault_analysis = pd.read_csv(vault_path)
        return emissions_results, vault_analysis
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

emissions_results, vault_analysis = load_data()

if emissions_results is not None and vault_analysis is not None:

    tab1, tab2, tab3 = st.tabs(["Key Metrics", "Vault Analysis", "Raw Data"])

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
        
        # Format vault analysis for display
        formatted_vault_analysis = vault_analysis.copy()
        for col in formatted_vault_analysis.select_dtypes(include=['float64']).columns:
            formatted_vault_analysis[col] = formatted_vault_analysis[col].apply(lambda x: f"${x:,.2f}")
        
        st.dataframe(
            formatted_vault_analysis,
            use_container_width=True,
            height=400
        )

    with tab3:
        st.subheader("Raw Data")
        
        # Create dropdown for CSV selection
        csv_option = st.selectbox(
            'Select CSV to view',
            ('Emissions Results', 'Vault Analysis')
        )
        
        if csv_option == 'Emissions Results':
            st.dataframe(
                emissions_results,
                use_container_width=True,
                height=400
            )
            
            # Add download button
            st.download_button(
                label="Download Emissions Results CSV",
                data=emissions_results.to_csv(index=False),
                file_name="ionic_emissions_results.csv",
                mime="text/csv"
            )
        else:
            st.dataframe(
                vault_analysis,
                use_container_width=True,
                height=400
            )
            
            # Add download button
            st.download_button(
                label="Download Vault Analysis CSV",
                data=vault_analysis.to_csv(index=False),
                file_name="ionic_vault_analysis.csv",
                mime="text/csv"
            )

else:
    st.error("Failed to load data. Please check if the CSV files exist in the correct location.")