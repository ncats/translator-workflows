## Orange Team CQ#2.7

### Query:
What drugs used in patients undergoing procedure X are seen significantly less often in an EHR sub-population with condition Y?

#### FA example:
What HSCT conditioning agents are seen significantly less often in EHR Fanconi Anemia (FA) populations?
  
#### Goal:
FA patients tolerate certain Hematopoietic Stem Cell Transplant (HCST) pre-conditioning drugs poorly. This set of queries aims to find drugs used to treat HCST, but that are used less often in FA patients. The output of this query might be used as input (i.e., potentially poor-tolerated drugs) for [CQ#2.4](https://github.com/NCATS-Tangerine/cq-notebooks/tree/master/Orange_Demonstrator_2_CQs/OrangeQ2.4_Drug_Gene_Pathway).
  
### Data Types, Sources, and Routes:
1. **Drugs indicated with procedure X** - from DrugBank.
2. **EHR data** - from EHR population co-occurence data.
3. **CUI-RxNorm and CUI-ICD connection** - from UMLS, [UMLS API](https://documentation.uts.nlm.nih.gov/rest/home.html)
  
### Sub-Queries/Tasks:
   
**Input:** procedure names in Set 1a and condition names in Set2a, *NOTE: steps can be completed for HCST procedures and Fanconi Anemia*
1. retrieve **drugs** used with **procedures** in Set1a --> Set1b
2. retrieve frequency of **patients** from EHR that have co-occurrence of **procedures** in Set1a and **drugs** in Set1b -> Set2b
3. retrieve frequency of **patients** from EHR that have co-occurrence of **conditions** in Set2a and **drugs** in Set1b -> Set2c
4. execute Fisher's exact test for **drugs** in Set1b to compare two independent patient subpopulation proportions (e.g., FA vs non-FA patients) --> Set3

**Output:** Set of drugs and their EHR subpopulation-specific p-values for the Fisher's exact test.
  
From here **drugs** that are seen significantly less often in patients with selected **condition** can be used as input for other analyses e.g., [CQ#2.4](https://github.com/NCATS-Tangerine/cq-notebooks/tree/master/Orange_Demonstrator_2_CQs/OrangeQ2.4_Drug_Gene_Pathway).

--------

*Note that two major assumptions are made: (a) conditions are captured with an ICD code, and (b) drug prescriptions for the treatment relevant to a procedure (e.g., HCST) occurs at the same point in time that the procedure is recorded in the EHR.*  
*Note #2: Some drugs may be used for patients undergoing procedure X with and without condition X.

