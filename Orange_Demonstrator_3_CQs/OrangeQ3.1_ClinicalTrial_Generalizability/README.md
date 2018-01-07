## Orange Team CQ#3.1

### Query: 
How well do clinical trial populations generalize to EHR patient populations?
  
### Goal:
Discoveries made in one population may have limited success when applied to populations other than those that finding were made in. The goal of this competency question is to quantify the generalizability of findings from clinical trials to EHR patient populations. This CQ is part of the larger Representativeness and Generalizability Demonstrator described [here](https://github.com/NCATS-Tangerine/cq-notebooks/wiki/Demonstrator-3:-EHR-Population-Generalizability).
  
### Data Types, Sources, and Routes:
1. **Clinical Trials** - from ClinicalTrials.gov, [ClinicalTrials.gov API](https://aact-prod.herokuapp.com/connect)
2. **EHR data** - from Synthetic data, [Synthetic data API]? or from OHDSI data, [OHDSI API](https://github.com/OHDSI/CommonDataModel/blob/master/OMOP%20CDM%20v5.pdf)?
3. **MeSH term and ICD-9/ICD-10 connection** - from UMLS, [UMLS API](https://documentation.uts.nlm.nih.gov/rest/home.html)
  
### Sub-Queries/Tasks:
**Input:** condition names (MeSH terms are used in ClinicalTrials.gov) Set1a, *NOTE: steps can be completed for Fanconi Anemia*

1. retrieve **clinical trials** that recruit Set1a populations --> Set1b (clinical trial | condition | mesh_term), [CT.gov link for "Fanconi anemia"](https://www.clinicaltrials.gov/ct2/results?cond=%22Fanconi+anemia%22)
2. retrieve **age range** from eligibility criteria or study results in Set1b --> Set1c (clinical trial | condition | mesh_term | age range)
3. retrieve **patients** from EHR that have conditions in Set1a -> Set2a (EHR id | patient id | condition | icd_code )
4. retrieve **ages** for patients in Set2a -> Set2b (EHR id | patient id | condition | icd_code | age of diagnosis)
5. execute calculation of **age range** for the set of **ages** in Set2b for each diagnosis in Set1a -> Set3 (EHR id | condition | icd_code | age range)
6. execute calculation of **Generalizability Index for Study Traits (GIST) score** with Set1c and Set3 for an EHR population -> Set4 (clinical trial | EHR id | condition | icd_code | mesh_term | GIST score)

Citation for GIST score calculation: [PMC4081748](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4081748)

**Output:** Set of clinical trials and their EHR population-specific GIST scores
  
GIST scores can be used to rank clinical trials when considering study populations for secondary analysis that are similar to an EHR population.

--------

*Note that age range in ClinicalTrials.gov studies may require parsing. General approach can be expanded for other population measures, conditions, and EHR populations*
