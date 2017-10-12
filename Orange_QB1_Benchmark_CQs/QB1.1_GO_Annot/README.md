## Orange QB1.1_GO_Annot

### Query:
What GO term annotations are made to FA core  genes?

### Goal:
A benchmarking query to assess information in the Translator system about GO annotations for human FA core, effector, and associated genes.

### Proposed Data Types, Sources, and Access Endpoints:
  1. Human GO annotations obtained from BioLink API.

**Input:** 
  1. List of FA core, effector, associated gene ids.
  2. GO annotations for all human genes.

**Output:**
  1. List of GO annotation descriptions for each gene.

 
 ### Stretch Queries
  1. Compute same for all FA gene isoforms.
  2. Report GO clusters which contain FA genes.
  3. Compute GO enrichment for FA genes.
  4. Report GO enrichments for clusters with FA genes.
  5. Similarly, for gene expression, gene fitness, protein interactions, ribosome profiling, etc.
