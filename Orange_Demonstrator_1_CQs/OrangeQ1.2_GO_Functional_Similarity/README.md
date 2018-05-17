## Orange Team CQ1.2

### Query:  
What genes express proteins that are functionally similar to the 11 Fanconi Anemia core complex genes (set FA-core), based on GO annotations?

### Goal:
This query aims to expand the FA-core gene set based on GO functional similarity, in service of Task 1 in the St. Jude Life Demonstrator described [here](https://github.com/NCATS-Tangerine/cq-notebooks/wiki/St.-Judes-FA-Demonstrator).
  
### Data Types, Sources, and Routes:
1. **Gene-ortholog associations** - from Panther, via SciGraph (BioLink [/bioentity/gene/{id}/homologs/](https://api.monarchinitiative.org/api/#!/bioentity/get_gene_homolog_associations))
2. **Gene-protein associations** -  from Ensembl, via SciGraph ([BioLink API](https://api.monarchinitiative.org/api/) call or [Monarch API cypher query](https://scigraph-data-dev.monarchinitiative.org/scigraph/docs/#!/cypher/execute)?)
3. **Functional annotations** - from GO, via SciGraph ([BioLink API](https://api.monarchinitiative.org/api/) or via Wikidata (SPARQL API)
  
### Sub-Queries/Tasks:
   
**Input:** NCBIGene identifiers for 11 FA-core genes
  1. Retrieve orthologs of FA-core genes and add to human FA-core set  
  2. Retrieve proteins encoded by genes in this cross-species set   
  3. Retrieve GO terms annotated to these proteins  
  4. Execute analysis to return ranked list of functionally similar proteins 
  5. Select subset of proteins meeting some defined threshhold  
  6. Retrieve genes that encode these proteins  
  7. Retrieve human orthologs of all non-human genes in this set  

**Output:** GeneSetQ2 (functionally similar human genes based on cross-species GO-similarity analysis)

*Note that the subqueries above can be parameterized in any number of ways in their implementation (e.g. select specific taxa  for cross-species expansion, facet on a MF or BP or CC subset of GO annotations, different inclusion threshholds for GO-based similarity, selecting different knowledge sources or routes to retrieve a particular data type). Different combinations of parameters can be explored using different notebooks in this directory.*

--------


### Stretch queries that include synthetic data
 
 **Input:** GeneSetQ2
  1. Retrieve patients all patients with variants in GeneSetQ2 at <5% frequency (check Gnomad, correct for racial/regional background)
  2. Filter patients for those with any of the following clinical variables:
  	a. Bone Marrow Failure
	b. Diagnosis of primary tumor of the type: HNSCC, Leukaemias (AML and acute monocytic leukaemia), Vulva, Brain, Esophagus, Breast, MDS, Skin SCC, Skin BCC, ovarian, pancreatic
	c. Childhood cancer diagnosis <15yrs
	d. Documented alcohol consumption
	e. 
	
	
 **Output:** Patients with candidate variants that are causal in combinations or with alcohol exposure that lead to more common cancers and other Fanconi-related phenotypes, such as bone marrow failure and HNSCC	


