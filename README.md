# Unit Zero Labs Research: Ionic Protocol

A collection of notebooks and resources of on-chain data specific to the Ionic Protocol. Repo includes notebooks for on-chain tracking: changes in supply and borrowing to vaults across Mode, OP, and Base, emissions tracking (by epoch and quarterly), revenue analysis, etc.

# Tokenomics
- [Tokenomics Model](https://docs.google.com/spreadsheets/d/1tWPMKIqRxg_noABRmQLhti0qXwG3c8bM30bvdzvxruE/edit?usp=sharing)

# Data

## Dune
- [Ionic Protocol](https://dune.com/mrwildcat/ionic-protocol)
- [Daily Emissions](https://dune.com/queries/4354659)
- [Post Reward User Behavior](https://dune.com/queries/4365031)
  
# Colab Notebooks

## Prices
- [Daily Prices](https://colab.research.google.com/drive/1Fx-mc15oYvhneCZjJBsFMds6Pcr0NESo?usp=sharing)

## Emissions
- [Emissions Analysis by Epoch](https://colab.research.google.com/drive/1Fx-mc15oYvhneCZjJBsFMds6Pcr0NESo?usp=sharing)
- [Quarterly Emissions Analysis](https://colab.research.google.com/drive/1w5vE_XBC-GAM-JypagmVXwAkgQjD6_oa?usp=sharing)

## Base Emissions
- [Base Quarterly Emissions Analysis](https://colab.research.google.com/drive/1AKj0aX8pRstYcr5sSJhj422DOLdDbwHy?usp=sharing)
- [Base Quartlery Emissions - Grouped by Vault Age and Size](https://colab.research.google.com/drive/16CkWZJFyZUFkJv6l_3LcU7no5Pfy4Bnh?usp=sharing)

## Regressions
- [Base Vault Emissions Regression](https://colab.research.google.com/drive/16CkWZJFyZUFkJv6l_3LcU7no5Pfy4Bnh?usp=sharing)
  

## Notebook Details & Assumptions
- base_qt_emissions_review.ipynb observes revenues based on changes to [supply and borrows in Base vaults](https://dune.com/mrwildcat/ionic-protocol) since start of emissions. Queries track emissions from [distributor addresses on Base](https://dune.com/queries/4354659).
- Revenues calculated based on direct and indirect revenue Ionic earns from vaults, less liquidiations/repayments. Estimates are within 1 std of averages.  
