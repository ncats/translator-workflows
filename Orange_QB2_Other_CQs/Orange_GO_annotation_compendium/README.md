## QB2.1 Human gene x GO term data compendium

### Query:  
Retrieve all data for human genes and their associated GO terms. Organize the data into a data compendium and output to a file ready for downstream analysis.

### Goal:
This query is to obtain all available data on human genes and their associated GO terms. The notebook code will organize the data into a data frame, label rows and columns, and output the result to a file for subsequent use in machine learning methods. The datasets are a bit large for Jupyter notebooks so the actual clustering is done in R (cluster_phenotype.R in this repo) and will explore adding the R code into the notebook itself.
  
### Data Types, Sources, and Routes:
1. **Gene-GO assignments** - via SciGraph (BioLink [/mart/gene/function/{taxon}](https://api.monarchinitiative.org/api/mart/gene/function/NCBITaxon:9606"))

### Sub-Queries/Tasks:
   
**Input:** Taxon 9606
  1. Retrieve all GO term assignments for all human geb=bes 
  2. Create data dictionary 
  3. Populate data frame from dictionary 
  4. Output text file
  5. Cluster data in R to produce diseases and phenotype clusters

**Output:** Genes x GO terms data compendium, Gene and GO term clusters

--------


### Stretch queries that include synthetic data
 
 **Input:**
	
	
 **Output:**


