## Orange Team CQ#3.2

### Query: 
What is the frequency of signs and symptoms associated with a condition among EHR patient populations?

### Goal:
Discoveries made in one population may have limited success when applied to populations other than those that finding were made in. The goal for this competency question is to assess the representativeness of published estimates of the frequency of signs and symptoms among patients with a condition in EHR patient populations.

### Data Types, Sources, and Routes:
1. **EHR data** - from Synthetic data, [JHU Synthetic data API]
2. **Frequency of signs & symptoms for a condition** - from Orphanet?? GARD??,
3. **HPO & ICD9/ICD10 connection** - from UMLS, [UMLS API](https://documentation.uts.nlm.nih.gov/rest/home.html)

### Sub-Queries/Tasks:
**Input:** condition name (CUI) Set1a *NOTE: steps can be completed for Fanconi Anemia*

1. retrieve **signs and symptoms** in Set1a --> Set1b (condition | sign or symptom | cui), [GARD link for "Fanconi anemia"](https://rarediseases.info.nih.gov/diseases/6425/index)
2. retrieve **population frequency of sign or symptom** for each sign or symptom in Set1b --> Set1c (condition | sign or symptom | cui | orphanet or gard population frequency)
3. retrieve **patients** from EHR that have a diagnoses/conditions in Set1a -> Set2a (EHR id | patient id | condition | icd_code )
4. retrieve condition **signs and symptoms** for patients in Set2a -> Set2b (EHR id | patient id | condition | icd_code | sign or symptom | cui)
5. execute calculation of **population frequency** for the set of **signs and symptoms** in Set2b for each diagnosis in Set1a -> Set3 (EHR id | condition | sign or symptom | EHR population frequency)
6. execute comparison between published and EHR population frequencies -> Set4 (EHR id | condition | icd_code | sign or symptom | cui | EHR population frequency | orphanet or gard population frequency)

**Output:** Frequency of published signs and symptoms associated with a condition in EHR population

Frequencies can be used to assess the representativeness of published signs and symptoms in an EHR population.

--------

*Note that published signs and symptoms and population frequencies may require parsing. Synthetic dataset assumptions: FA diagnosis is captured with a CUI and FA signs and symptoms are represented as structured data (CUIs) - likely not true for EHR patient populations*
