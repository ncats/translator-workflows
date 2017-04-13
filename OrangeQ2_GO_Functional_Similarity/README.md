### Orange CQ #2

**Query:**  What genes express proteins that are functionally similar to the primary Fanconi anemia genes (set FA-core), based on GO annotations?

**Goal:** This query aims to expand the FA-core gene set based on GO functional similarity, in service of Task 1 in the St. Jude Life Cohort Demonstrator described [here](https://github.com/NCATS-Tangerine/cq-notebooks/wiki/St.-Judes-FA-Demonstrator).
  
**Data Types and Sources:**
1. Gene-ortholog associations from Panther via BioLink API
2. Gene-protein associations from Ensembl via BioLink API
3. Functional annotations from GO via  Biolink API
  
**SubQueries/Tasks:**  
1. Retrieve gene ids of orthologes of FA-core genes  
2. Retrieve ids for proteins encoded by genes in this cross-species set  
3. Retrieve GO terms annotated to these protein ids  
4. Execute similarity analysis that returns the set of similar proteins/genes across species  
5. Retrieve ids for genes that encode proteins in this set  
6. Retrieve list of human orthologs of all non-human genes --> store as gene set Q2  
  
--------
	
**Formal Queries**
1. *(URL of BioLink API call to return FA-core orthologs)*
2. *(URL of BioLink API call to return proteins encoded by these genes)*

