**Use the readme below for "Orange Team CQ1.1" as an examplar and template for creation of new CQ readme files.**

- **Required fields** inclue a query _Name_, and the _Query_ itself.  
- **Recommended fields** include the _Goal_ of the query and any context to help understand its utility and purpose, and _Proposed Data Types, Sources, and Access Endpoints_.
- **Optional fields**  include _Proposed Subqueries and Tasks_, and _Stretch Queries_. These are particularly useful in allowing a domain expert to suggest sources and workflows to the developer who will implement the notebook. 

--------------------------

## Orange Team CQ1.1

### Query:
What genes encode proteins that physically interact with proteins encoded by the 11 Fanconi Anemia core complex genes?

### Goal:
This simple query aims to expand the FA-core gene set based PPI network membership, in service of Task 1 in the St. Jude Life Demonstrator described [here](https://github.com/NCATS-Tangerine/cq-notebooks/wiki/St.-Judes-FA-Demonstrator).
  
### Proposed Data Types, Sources, and Access Endpoints:
1. Gene-ortholog associations from [Panther](http://www.pantherdb.org/), via SciGraph (BioLink [/bioentity/gene/{id}/homologs/](https://api.monarchinitiative.org/api/#!/bioentity/get_gene_homolog_associations)))
2. Protein-protein interactions from [BioGRID](https://thebiogrid.org/) and [STRING](http://string-db.org/), via SciGraph (BioLink [/bioentity/gene/{id}/interactions/](https://api.monarchinitiative.org/api/#!/bioentity/get_gene_interactions)))
  
### Proposed Sub-Queries/Tasks:
   
**Input:** NCBIGene identifiers for 11 FA-core genes
  1. Retrieve orthologes of FA-core genes and add to human FA-core set  
  2. Retrieve proteins encoded by this gene set  
  3. Retrieve proteins that interact with these proteins  
  4. Retrieve genes that encode these interacting proteins  
  5. Retrieve human orthologs of all non-human genes in this set    

**Output:** GeneSetQ1 (human genes encoding physical interactors with FA-core gene products)

*Note that the subqueries above can be parameterized in various ways in their implementation (e.g. faceting specific taxa for cross-species expansion, using different network-based metrics to define 'interactors', selecting different knowledge sources or routes to retrieve a particular data type). Different combinations of parameters can be explored using different notebooks in this directory.*

-----

### Stretch Queries
 
 **Input:** GeneSetQ1
  1. Retrieve patients all patients with variants in GeneSetQ1 at <5% frequency (check Gnomad, correct for racial/regional background)
  2. Filter patients for those with any of the following clinical variables:  
  	a. Bone Marrow Failure  
	b. Childhood cancer diagnosis <15yrs  
  	c. Documented alcohol consumption    
 
 **Output:** Patients with candidate variants that are causal in combinations or with alcohol exposure that lead to more common cancers and other Fanconi-related phenotypes, such as bone marrow failure and HNSCC
 
