## QB2.2 Disease x phenotype compendium


### Query:  
Retrieve all data for human diseases and their associated phenotypes. Organize the data into a data compendium and output to a file ready for downstream analysis.

### Goal:
This query is to obtain all available data on human diseases and their associated phenotypes. The notebook code will organize the data into a data frame, label rows and columns, and output the result to a file for subsequent use in machine learning methods. The datasets are a bit large for Jupyter notebooks so the actual clustering is done in R (cluster_phenotype.R in this repo) and will explore adding the R code into the notebook itself.
  
### Data Types, Sources, and Routes:
1. **Disease-phenotype associations** - via SciGraph (BioLink [/mart/disease/{object_category}/{taxon}](https://api.monarchinitiative.org/api/mart/disease/phenotype/NCBITaxon%3A9606"))
  
### Sub-Queries/Tasks:
   
**Input:** Taxon 9606
  1. Retrieve all phenotype associations for all human diseases 
  2. Create data dictionary 
  3. Populate data frame from dictionary 
  4. Output text file
  5. Cluster data in R to produce diseases and phenotype clusters

**Output:** Disease x phenotype data compendium, disease and phenotype clusters

--------


### Stretch queries that include synthetic data

	
 **Output:**


