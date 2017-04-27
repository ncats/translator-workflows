### Green Team Q3: Drug Repurposing for the Prevention of Asthma Exacerbations in Response to PM2.5 and Ozone Exposures

## Query:

What medications are available that act on the protein (gene) targets and biological pathways that are activated or inhibited by particulate matter <=2.5 micrometers in diameter (PM2.5) and ozone exposure?

## Goal:

Asthma exacerbations in response to airborne pollutants such as PM2.5 and ozone can be life threatening and result in hospitalization or even death. While numerous medications have received FDA approval for the treatment of asthma, a need exists for new treatments to prevent asthma exacerbations in response to exposure to airborne pollutants. This query should allow us to identify existing medications that may be effective in preventing asthma exacerbations in response to exposure to PM2.5 and ozone. As such, the query should provide insight into drugs that may be repurposed for the treatment of asthma.

## Data Types, Sources, and Routes:
CTD: human proteins/genes

KEGG, Reactome (via CTD): biological pathways

DrugBank: medications

**Input:** ‘PM2.5’ or ‘particulate matter’; ‘ozone’

1. List protein (gene) targets for PM2.5
2. List protein (gene) targets for ozone exposure
3. Identify commonalities in (1) and (2)
4. List up/downstream biological pathways affected by protein (gene) targets in (3) 
5. Rank output from (3) by frequency (most common to least common)
6. Rank output from (4) by frequency (most common to least common)
7. List FDA-approved medications for top 100 protein (gene) targets identified in (5)
8. List FDA-approved medications for top 100 biological pathways identified in (6)
9. Identify commonalities in (7) and (8)
10. Rank list in (9)

**Output:** Ranked list of FDA-approved medications that may be repurposed for the prevention of asthma exacerbations triggered by PM2.5 and ozone
