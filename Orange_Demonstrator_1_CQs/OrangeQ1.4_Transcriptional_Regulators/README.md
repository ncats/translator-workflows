## Orange Team CQ1.4

### Query:
What genes/proteins are (putative) transcriptional regulators of genes in set FA-core?

### Goal:
This  query aims to expand the FA-core gene set to include genes for putative transcriptional regulators of FA genes (based on computational or experimental evidence). This query is in service of Task 1 in the St. Jude Life Demonstrator described [here](https://github.com/NCATS-Tangerine/cq-notebooks/wiki/St.-Judes-FA-Demonstrator).
  
### Data Types, Sources, and Routes:
1. Regulatory Region Predictions from [Ensembl FuncGen API](http://www.ensembl.org/info/docs/api/funcgen/index.html)
2. Predicted JASPAR motif binding sites from [Ensembl FuncGen API](http://www.ensembl.org/info/docs/api/funcgen/index.html)
3. Experimentally validated tx factor  binding sites [Ensembl FuncGen API](http://www.ensembl.org/info/docs/api/funcgen/index.html)

  
### Sub-Queries/Tasks:

**Workflow #1: Computationally-predicted factor binding (JASPAR)**  
  
**Input:** Ensembl identifiers for FA-core genes
1. retrieve TSS (tx start site) coordiantes for FA-core genes from Ensembl API
2. retrieve Ensembl 'regualtory features' within X kb of FA-core gene TSSs
3. retrieve list of transcription factors with putatuve binding sites (JASPAR motifs) within these regions
4. retrieve gene ids for these tx factors  

**Output:** list of genes, GeneSet1.4a expressing tx factors predicted to bind Ensembl regulatory regions adjacent to FA core genes


-----

**Workflow #2: Experimentally-validated factor binding (ENCODE/Chip-Seq)**  
  
**Input:** Ensembl identifiers for FAcore genes
1. retrieve all tx factor binding site annotations within 5kb of  FA-core gene TSS (along with evidence/provenance metadata, e.g. cell lines in which regulatory region demonstrated to be active, etc)
2. (optional) filter for those predicted to be active in particular cell or tissue types of interest
3. retrieve list of gene ids for  these  tx factors  

**Output:** list of genes expressing tx factors experimentally validated to bind near to FA core genes, GeneSet1.4b

-----

### Stretch queries that include synthetic data
 
 **Input:** GeneSet1.4a or GeneSet1.4b
  1. Retrieve patients all patients with variants in genes in GeneSet1.4a or GeneSet1.4b at <5% frequency (check Gnomad, correct for racial/regional background)
  2. Filter patients for those with any of the following clinical variables:
  	a. Bone Marrow Failure
	b. Diagnosis of primary tumor of the type: HNSCC, Leukaemias (AML and acute monocytic leukaemia), Vulva, Brain, Esophagus, Breast, MDS, Skin SCC, Skin BCC, ovarian, pancreatic
	c. Childhood cancer diagnosis <15yrs
	d. Documented alcohol consumption
	e. 
	
	
 **Output:** Patients with candidate variants that are causal in combinations or with alcohol exposure that lead to more common cancers and other Fanconi-related phenotypes, such as bone marrow failure and HNSCC	
