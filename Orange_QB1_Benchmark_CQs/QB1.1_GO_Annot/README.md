## Orange QB1.1_GO_Annot

### Query:
What GO term annotations are made to FA core  genes?

### Goal:
A benchmarking query to assess information in the Translator system about GO annotations for human FA core genes.

### Proposed Data Types, Sources, and Access Endpoints:
  1. Human GO annotations obtained from BioLink API.
  
### Proposed Sub-Queries/Tasks:
  1. BioLink API REST query for GO annotations
  https://api.monarchinitiative.org/api/bioentity/gene/NCBIGene%3A675/function/?fetch_objects=true
  2. Monarch SciGraph query
  "MATCH path=(subject:gene)-[relation:RO:0002331]->(object:`biological process`)
  RETURN DISTINCT subject, object
  UNION
  MATCH path=(subject:gene)-[relation:RO:0002327]->(object:`molecular function`)
  RETURN DISTINCT subject, object
  UNION
  MATCH path=(subject:gene)-[relation:BFO:0000050]->(object:`cellular component`)
  RETURN DISTINCT subject, object
  "
**Input:** 
  1. List of FA core gene ids.
  2. List of all FA core gene isoform ids.
  3. GO annotations for all human genes.

**Output:**
  1. List of GO annotations for each gene or gene isoform id.

 
 ### Stretch Queries
  1. Report GO clusters which contain FA genes.
  2. Compute GO enrichment for FA genes.
  3. Report GO enrichments for clusters with FA genes.
  4. Similarly, for gene expression, gene fitness, protein interactions, ribosome profiling, etc.
