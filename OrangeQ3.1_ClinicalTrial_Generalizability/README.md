## Orange Team CQ#3.1

### Query: 
How well do clinical trial populations generalize to EHR patient populations? (i.e., Compare the target population to the synthetic patient population)
  
### Goal:
Discoveries made in one population may have limited success when applied to populations other than those that finding were made in. Thus, there is a need to quantify the generalizability of findings from clinical trials to EHR patient populations.
  
### Data Types, Sources, and Routes:
1. **Clinical Trials** - from ClinicalTrials.gov [ClinicalTrials.gov API](https://aact-prod.herokuapp.com/connect)
2. **EHR data** - from Synthetic data [JHU Synthetic data API]
  
### Sub-Queries/Tasks:
**Input:** condition names (MeSH_terms) Set1a 

1. retrieve **clinical trials** that recruit Set1a populations --> Set1b (clinical trial | condition)
2. retrieve **age range** from eligibility criteria or study results in Set1b --> Set1c (clinical trial | condition | age range)
3. retrieve **patients** from EHR that have a diagnoses/conditions in Set1a -> Set2a (EHR id | patient id | condition )
4. retrieve **ages** for patients in Set2a -> Set2b (EHR id | patient id | condition | age of diagnosis)
5. execute calculation of age range for the set of **ages** in Set2b for each diagnosis in Set1a -> Set3 (EHR id | condition | age range)
6. execute calculation of Generalizability Index for Study Traits (GIST) score with Set1c and Set3 for an EHR population -> Set4 (clinical trial | EHR id | condition | GIST score)

**Output:** Set of clinical trials and their EHR population-specific GIST scores
  
GIST scores can be used to rank clinical trials when considering study populations for secondary analysis that are similar to an EHR population.

--------

*Note that age range in ClinicalTrials.gov studies may require parsing.*
