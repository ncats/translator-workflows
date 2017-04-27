### Green Team Q1: Asthma Outcomes in Relation to PM2.5 and Ozone Exposures

## Query:

Among pediatric patients with an 'asthma-like phenotype', is exposure to particulate matter <=2.5 micrometers in diameter (PM2.5) and ozone associated with responsiveness to treatment? (In other words, are exposures higher in patients who are non-responsive to treatment than in patients who are responsive to treatment?)

## Goal:

Patients with asthma are sensitive to airborne pollutants such as PM2.5 and ozone, and exposure to high levels of airborne pollutants often triggers asthma exacerbations. This query should confirm our assertion and overall use case assumption that exposure to high levels of airborne pollutants is associated with poor clinical outcomes among patients with an 'asthma-like phenotype'. By so doing, the query should allow us to validate our exposure models and test the functionality of our system and approach.

## Data Types, Sources, and Routes:

Patient Data: Green Team HuSH+ Patient Data

Exposure Data: PM2.5 and ozone exposure estimates from the Center for the Community Modeling and Assessment System (CMAS), UNC Institute for the Environment (raw sensor data from US EPA)

**Input:** HuSH+ patients with <=2 or >2 ED visits over 12-month period after diagnosis for 'asthma-like phenotype'; patient latitude and longitude

1. List the date of ED and clinic* visits for pediatric patients with an asthma-like phenotype
2. Identify patients in (1) with <=2 and >2 ED visits over the 12-month period after diagnosis**
3. List the max daily PM2.5 exposure score*** per day for the 14-day period prior to each ED and clinic visit in (1)
4. List the max daily ozone exposure score per day for the 14-day period prior to each ED and clinic visit in (1)
5. Calculate the 7- and 14-day PM2.5 and ozone exposure scores for each ED and clinic visit in (1)
6. Calculate the mean 7- and 14-day PM2.5 and ozone exposure scores for ED and clinic visits for each group of patients (responsive/non-responsive) identified in (2)****
7. Calculate the median 7- and 14-day PM2.5 and ozone exposure scores for ED and clinic visits for each group of patients (responsive/non-responsive) identified in (2)****
8. Calculate the range of 7- and 14-day PM2.5 and ozone exposure scores for ED and clinic visits for each group of patients (responsive/non-responsive) identified in (2)****
9. Calculate the quartiles for 7- and 14-day PM2.5 and ozone exposure scores for ED and clinic visits for each group of patients (responsive/non-responsive) identified in (2)****


*Clinic visit = outpatient visit

**Responsiveness to treatment defined as <=2 (responsive) or >2 (non-responsive) ED visits over 12-month period after diagnosis for an 'asthma-like phenotype'

***Exposure scores are defined on a 5-point scale, with 1 indicating low and 5 indicating high; scores are based on established literature

****Data to be used to determine "high" and "low" exposure scores for subsequent queries

**Output:** PM2.5 and ozone exposure scores over the 7- and 14-day period prior to an ED visit for a respiratory event or a clinic visit among patients with an asthma-like phenotype who are or who are not responsive to treatment
