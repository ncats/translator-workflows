## Orange Team CQ1.1

### Query:
What genes encode proteins that physically interact with proteins encoded by the 11 Fanconi Anemia core complex genes (set FA-core)? 

### Goal:
This simple query aims to expand the FA-core gene set based PPI network membership, in service of Task 1 in the St. Jude Life Demonstrator described [here](https://github.com/NCATS-Tangerine/cq-notebooks/wiki/St.-Judes-FA-Demonstrator).
  
### Possible Data Types, Sources, and Routes:
1. Gene-ortholog associations from [Panther](http://www.pantherdb.org/), via SciGraph (BioLink [/bioentity/gene/{id}/homologs/](https://api.monarchinitiative.org/api/#!/bioentity/get_gene_homolog_associations))
2. Protein-protein interactions from [BioGRID](https://thebiogrid.org/) and [STRING](http://string-db.org/), via SciGraph (BioLink [/bioentity/gene/{id}/interactions/](https://api.monarchinitiative.org/api/#!/bioentity/get_gene_interactions))

  
### Possible Sub-Queries/Tasks:
   
**Input:** NCBIGene identifiers for 11 FA-core genes
  1. Retrieve orthologes of FA-core genes and add to human FA-core set  
  2. Retrieve proteins encoded by this gene set  
  3. Retrieve proteins that interact with these proteins  
  4. Retrieve genes that encode these interacting proteins  
  5. Retrieve human orthologs of all non-human genes in this set    

**Output:** GeneSetQ1 (human genes encoding physical interactors with FA-core gene products)

*Note that the subqueries above can be parameterized in various ways in their implementation (e.g. faceting specific taxa for cross-species expansion, using different network-based metrics to define 'interactors', selecting different knowledge sources or routes to retrieve a particular data type). Different combinations of parameters can be explored using different notebooks in this directory.*

-----

### Stretch queries that include synthetic data
 
 **Input:** GeneSetQ1
  1. Retrieve patients all patients with variants in GeneSetQ1 at <5% frequency (check Gnomad, correct for racial/regional background)
  2. Filter patients for those with any of the following clinical variables:
  	a. Bone Marrow Failure
	b. Diagnosis of primary tumor of the type: HNSCC, Leukaemias (AML and acute monocytic leukaemia), Vulva, Brain, Esophagus, Breast, MDS, Skin SCC, Skin BCC, ovarian, pancreatic
	c. Childhood cancer diagnosis <15yrs
	d. Documented alcohol consumption
	e. 
	
	
 **Output:** Patients with candidate variants that are causal in combinations or with alcohol exposure that lead to more common cancers and other Fanconi-related phenotypes, such as bone marrow failure and HNSCC
 
-----

### Outcomes
(e.g. results of the analysis, challenges encountered, lessons learned)
