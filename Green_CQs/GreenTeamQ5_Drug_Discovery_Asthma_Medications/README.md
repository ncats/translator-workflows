### Green Team Q5: Drug Discovery for New Asthma Medications

## Query:

What is the protein (gene) target and biological pathway of medications currently prescribed to patients with an asthma-like phenotype who are responsive to treatment despite high levels of exposure to particulate matter <=2 micrometers in diameter (PM2.5) and ozone?

## Goal:
Understanding the mechanism of action of medications associated with responsive to treatment among patients who are typically difficult to treat should provide insight into the etiology and pathophysiology of asthma and also facilitate new drug discovery and development. This query aims to identify the protein/gene targets and biological pathways associated with medications that are effective in patients with asthma and high levels of exposure to PM2.5 and ozone. As such, the query should further efforts to delineate asthma ‘endotypes’. The query also should facilitate drug discovery for the treatment of asthma through the identification of drug targets that might be investigated for drug repurposing or new drug development.

## Data Types, Sources, and Routes:
Patient Data: Patient Data: Green Team HuSH+ Patient Data

Exposure Data: PM2.5 and ozone exposure estimates from the Center for the Community Modeling and Assessment System (CMAS), UNC Institute for the Environment (raw sensor data from US EPA)

DrugBank: medication mechanism of action

CTD: protein (gene) targets

KEGG, Reactome: biological pathways

**Input:** Data on HuSH+ patients with <=2 or >2 ED visits over 12-month period after diagnosis for 'asthma-like phenotype'; patient latitude and longitude

1. List the date of ED visits for pediatric patients with an asthma-like phenotype
2. Identify patients in (1) with <=2 ED visits over the 12-month period after diagnosis*
3. List max daily PM2.5 exposure score per day for the 14-day period prior to each ED visit in (1)
4. List max daily ozone exposure score per day for the 14-day period prior to each ED visit in (1)
5. Calculate the 7- and 14-day PM2.5 and ozone exposure scores for each ED visit in (1)
6. Identify patients in (2) with high PM2.5 and ozone exposure scores**
7. List prescribed and administered medications for patients identified in (6) over the 12-month period after diagnosis
8. Rank the medications identified in (7)
9. List the ‘mechanism of action’ for the medications identified in (8)
10. List the protein (gene) targets for the medications identified in (8)
11. Identify commonalities in (9) and (10)
12. Rank the list in (11)
12. List the biological pathways for the protein (gene) targets in (12)
13. Rank the list in (12)

*Response to treatment defined as <=2 ED visits over 12-month period; 'diagnosis' refers to the diagnosis used in the CDWH query

**"High" and "low" exposure scores to be defined under (Green Team Q1)

**Output:** Ranked lists of (1) the protein (gene) targets (1) and biological pathways of FDA-approved medications that are effective in patients with asthma and high levels of exposure to airborne pollutants

