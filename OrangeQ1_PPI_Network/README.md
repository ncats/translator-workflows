### Orange CQ#1

**Query:**  What genes encode proteins that physically interact with proteins encoded by the 11 Fanconi Anemia core complex genes (set FA-core)? 

**Goal:** This query aims to expand the FA-core gene set based PPI network membership, in service of Task 1 in the St. Jude Life Cohort Demonstrator described [here](https://github.com/NCATS-Tangerine/cq-notebooks/wiki/St.-Judes-FA-Demonstrator).
  
**Data Types, Sources, and Routes:**
1. Gene-ortholog associations from [Panther](http://www.pantherdb.org/), via SciGraph (BioLink [/bioentity/gene/{id}/homologs/](https://api.monarchinitiative.org/api/#!/bioentity/get_gene_homolog_associations))
2. Protein-protein interactions from [BioGRID](https://thebiogrid.org/) and [STRING](http://string-db.org/), via SciGraph (BioLink [/bioentity/gene/{id}/interactions/](https://api.monarchinitiative.org/api/#!/bioentity/get_gene_interactions))

  
**Sub-Queries/Tasks:**  
   
Input: NCBIGene identifiers for 11 FA-core genes
  1. Retrieve orthologes of FA-core genes  
  2. Retrieve proteins encoded by these genes
  3. Retrieve proteins that interact with these proteins
  4. Retrieve genes that encode these interacting proteins
  5. Retrieve human orthologs of all non-human genes in this set  

Output: GeneSetQ1 (human genes encoding physical interactors with FA-core gene products)

-----

*Note that the subqueries above can be parameterized in various ways in their implementation (e.g. faceting specific taxa for cross-species expansion, using different network-based metrics to define 'interactors', selecting different knowledge sources or routes to retrieve a particular data type). Different combinations of parameters can be explored using different notebooks in this directory.*

	
