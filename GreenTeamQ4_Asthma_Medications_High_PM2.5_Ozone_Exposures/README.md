### Green Team Q4: Medications Effective in Patients with Asthma and High PM2.5 and Ozone Exposures

## Query:

Which medications are currently prescribed to pediatric patients with an asthma-like phenotype who are responsive to treatment despite high levels of exposure to particulate matter <=2.5 micrometers in diameter (PM2.5) and ozone?

## Goal:

Patients with asthma and high levels of exposure to airborne pollutants such as PM2.5 and ozone have frequent asthma exacerbations and are generally difficult to treat. However, a subset of these patients are responsive to treatment, either because of unique biological characteristics (i.e., a distinct asthma ‘endotype’), or because the medications they are being treated with are highly effective, or both. This query aims to identify medications associated with good clinical outcomes among patients with asthma and high PM2.5 and ozone exposures. As such, the query should provide clinical insight into treatment options for asthma, particularly for patients who are difficult to treat. The query also should further efforts to delineate asthma ‘endotypes’.

## Data Types, Sources, and Routes:
Patient Data: Green Team HuSH+ Patient Data

Exposure Data: PM2.5 and ozone exposure estimates from the Center for the Community Modeling and Assessment System (CMAS), UNC Institute for the Environment (raw sensor data from US EPA)

**Input:** Data on HuSH+ patients with <=2 or >2 ED visits over 12-month period after diagnosis for 'asthma-like phenotype'; patient latitude and longitude

1. List the date of ED visits for pediatric patients with an asthma-like phenotype
2. Identify patients in (1) with <=2 or >2 ED visits over the 12-month period after diagnosis*
3. List max daily PM2.5 exposure score per day for the 14-day period prior to each ED visit in (1)
4. List max daily ozone exposure score per day for the 14-day period prior to each ED visit in (1)
5. Calculate the 7- and 14-day PM2.5 and ozone exposure scores for each ED visit in (1)
6. Identify patients in (2) with high and low PM2.5 and ozone exposure scores**
7. List prescribed and administered medications for patients identified in (6) over the 12-month period after diagnosis of an asthma-like phenotype
8. Rank list in (7)

*Response to treatment defined as <=2 ED visits over 12-month period; 'diagnosis' refers to the diagnosis used in the CDWH query

**"High" and "low" exposure scores to be defined under (Green Team Q1)

**Output:** Ranked list of FDA-approved medications that are effective in patients with asthma and high levels of exposure to airborne pollutants
