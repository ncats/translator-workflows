## Orange Team CQ#1.7

### Query: 
What genes show high phenotypic similarity to the 11 Fanconi Anemia core complex genes (set FA-core)?

### Goal:
This query aims to expand the FA-core gene set based on phenotype similarity, in service of Task 1 in the St. Jude Life Demonstrator described [here](https://github.com/NCATS-Tangerine/cq-notebooks/wiki/St.-Judes-FA-Demonstrator).
  
### Data Types, Sources, and Routes:
1. **Gene-ortholog associations** - from Panther, via SciGraph (BioLink [/bioentity/gene/{id}/homologs/](https://api.monarchinitiative.org/api/#!/bioentity/get_gene_homolog_associations))
2. **Gene-phenotype associations** - from various sources integrated by Monarch, via SciGraph (BioLink [/bioentity/gene/{id}/phenotypes/](https://api.monarchinitiative.org/api/#!/bioentity/get_gene_phenotype_associations))
  
### Sub-Queries/Tasks:
   
**Input:** NCBIGene identifiers for 11 human FA-core genes
  1. Retrieve orthologes of FA-core genes and add to human FA-core set  
  2. Retrieve phenotype terms associated genes in this set  
  3. Execute PhenoSim analysis to return ranked list of phenotypically similar genes  
  4. Select subset of genes meeting some defined threshhold  
  5. Retrieve human orthologs of all non-human genes in this set   

**Output:** GeneSetQ7 (phenotypically similar human genes based on cross-species PhenoSim analysis)

--------

*Note that the subqueries above can be parameterized in any number of ways in their implementation (e.g. select specific taxa for cross-species expansion, use of different PhenoSim similarity algorithms/metrics, different inclusion threshholds for phenotype similarity, selecting different knowledge sources or routes to retrieve a particular data type). Different combinations of parameters can be explored using different notebooks in this directory.*
