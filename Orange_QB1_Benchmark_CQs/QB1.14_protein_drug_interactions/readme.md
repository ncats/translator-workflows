## Orange QB1.14

### Query:

Return all known protein-drug interactions 

### Refined Query:

What drugs are known to interact with FA proteins (e.g. BRCA2)

### Goal:

A benchmarking query to assess information in the Translator system about protein-drug interactions


### Proposed Data Types, Sources, and Access Endpoints:
1. IUPHAR (through wikidata)
2. 


### Proposed Sub-Queries/Tasks:
**Input:** FA Gene X  (used FANCC and BRCA2 as exemplars):
   
**Output:** Set of drugs interacting with FA gene(s) and the type of interaction (inhibitor/activator/etc)

### Outcomes:
No interactors found using IUPHAR.

### To Do:
Explore other resources, including: 
1. [Drugbank](https://www.drugbank.ca) ([example](https://www.drugbank.ca/biodb/bio_entities/BE0000123)) (in [mychem.info](http://mychem.info/v1/metadata))
2. [DGIdb](http://dgidb.org/)
3. [BindingDB](https://www.bindingdb.org/bind/index.jsp)
  
