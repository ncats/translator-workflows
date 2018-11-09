## Orange Team CQ#3.2

### Query: 
What is the representativeness of condition-specific signs and symptoms among EHR patient populations?

### Goal:
One heuristic used in clinical decision-making is representativeness (a patient's similarity to a particular known condition). The goal for this competency question is to assess the representativeness of published estimates of the frequency of signs and symptoms among patients with a condition in EHR patient populations. This CQ is part of the larger Representativeness and Generalizability Demonstrator described [here](https://github.com/NCATS-Tangerine/cq-notebooks/wiki/Demonstrator-3:-EHR-Population-Generalizability).

### Data Types, Sources, and Routes:
1. **EHR data** - from Synthetic data, [Synthetic data API]
2. **Frequency of signs and symptoms for a condition** - from Orphanet?? GARD??, via SciGraph ([BioLink API](https://api.monarchinitiative.org/api/) call or [Monarch API cypher query](https://scigraph-data-dev.monarchinitiative.org/scigraph/docs/#!/cypher/execute)?)
3. **HPO and ICD9/ICD10 connection** - from UMLS, [UMLS API](https://documentation.uts.nlm.nih.gov/rest/home.html)

### Sub-Queries/Tasks:
**Input:** condition name (CUI) Set1a, *NOTE: steps can be completed for Fanconi Anemia*

1. retrieve **signs and symptoms** for condition(s) in Set1a --> Set1b (condition | cui | sign or symptom | hp_term), [GARD link for "Fanconi anemia"](https://rarediseases.info.nih.gov/diseases/6425/index)
2. retrieve **population frequency** for each sign or symptom in Set1b --> Set1c (condition | cui | sign or symptom | hp_term | orphanet or gard population frequency)
3. retrieve **patients** from EHR that have condition(s) in Set1a -> Set2a (EHR id | patient id | condition | icd_code )
4. retrieve condition **signs and symptoms** in Set1b for patients in Set2a -> Set2b (EHR id | patient id | condition | icd_code | sign or symptom | hp_term)
5. execute calculation of **population frequency** for condition-specific **signs and symptoms** in Set2b -> Set3 (EHR id | condition | icd_code | sign or symptom | hp_term | EHR population frequency)
6. execute comparison between published and EHR population frequencies -> Set4 (EHR id | condition | icd_code | sign or symptom | hp_term | EHR population frequency | orphanet or gard population frequency | difference in population frequencies)

**Output:** Difference between published frequencies of condition-specific signs and symptoms and frequencies occurring in an EHR population.

This is a simple representativeness heuristic calculation with potential to be used to make first diagnostic impressions under simulated scenarios. Incremental adjustments can be made with synthetic data sets (e.g., changes in quantity of missing data), which can be used as an education tool to better understand cognitive biases in clinical decision-making.

--------

*Note that published signs and symptoms and population frequencies may require parsing. Two major assumptions are made with the synthetic dataset: (a) conditions are captured with ICD codes, and (b) signs and symptoms are captured as structured data - this is not always true in EHR patient populations*
