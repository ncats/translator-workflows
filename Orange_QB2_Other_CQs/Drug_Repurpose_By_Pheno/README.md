## QB2.3 Drug_Repurpose_By_Phenotype 

### Query:
For Drug X, find other diseases it might be re-purposed for based on phenotype similarity with the drugs primary indication.

### Proposed Data Types, Sources, and Access Endpoints:
1. Wikidata (Drug indications)
2. Monarch/BioLink (Disease-Phenotype associations)
  
### Proposed Sub-Queries/Tasks:
   
**Input:** Drug X  
  
**1. Traversal:** Retreive diseases that are indictions for Drug X   
`Drug -[drug_used_for_treatement] -> Disease (Wikidata)`  

**2. Traversal:** Retreive all phenotypes for each disease in this set   
`Disease -[has_phenotype]-> Phenotype (Monarch)`  

**3. Computation:** Find most phenotypically similar diseases based on profile of primary indication    

**Output:** Set of diseases ranked by their phenotypic similarity to the primry indications for input Drug X

