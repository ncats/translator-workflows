## QB2.3 Drug_Repurpose_By_Phenotype 

### Query:
For Drug X that treats Disease Y, find other diseases Drug X might be re-purposed for based on phenotype similarity with Disease Y.

### Goals:
1. This query requires traversing a  path of associations served by two different beacons (i.e. each beacon provides part of the knowledge graph required an answer).  Specifically, drug indication data from Wikidata, and disease-phenotype data from Monarch/Biolink.  It will test the ability of different approaches (traditional notebooks and k-beacons) to make the joins required to answer such a query.

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

