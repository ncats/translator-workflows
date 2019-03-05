# Workflow 2 TIDBIT: Von Hippel Lindau (VHL)

## What genes are directly associated with VHL which could serve a basis for a deeper understanding of the disease and as targets for therapeutic intervention?

### Background

Von [Hippel-Lindau syndrome (VHL)](http://omim.org/entry/193300) is a dominantly inherited familial cancer syndrome predisposing to a variety of malignant and benign neoplasms, most frequently retinal, cerebellar, and spinal hemangioblastoma, renal cell carcinoma (RCC), pheochromocytoma, and pancreatic tumors.

### Current State of Knowledge

By positional cloning, Latif et al. (1993) identified the [VHL tumor suppressor gene](http://omim.org/entry/608537).  

The gene is now known to be a component of a regulatory component of the E3 ligase targeting proteolytic degradation of the Hypoxia Induced Factor 1 alpha (HIFa). Loss-of-function of VHL leads to prolonged expression of the HIFa stimulating excessive focal blood vessel and blood formation (see [KEGG pathway hsa04066](https://www.genome.jp/kegg-bin/show_pathway?hsa04066+N00079) below)


![KEGG VHL Pathway](./KEGG_hsa04066_HIF-1_Pathway.png  "KEGG VHL Pathway")

The [VHL patient community](https://www.vhl.org) are working to find a cure for VHL, with [some drug trials underway for specific pathologies](https://www.raredr.com/news/vhl-drug-phase-2-study-initiated) but no systemic cure is yet available for the disease.


### Existing versus Translator Method

Traditionally, candidate genes are identified by querying pubmed, reading relevant literature, and leveraging domain expertise to identify and construct new ideas from the bits of knowledge extracted from the free text. Those ideas are then tested in the laboratory and iterated upon. 

On the other end of the spectrum, experimental high throughput methods generate lists of candidates that are so massive they are difficult to prioritize. There has to be a better way!


The following is an example analysis that leverages curated knowledge (extracted and structured by professional curators with expertise in the domain) that has been semantically modeled to support machine readability in advanced querying and semantic similarity search algorithms.

Essentially, genes are identified as similar based not only on the attributes that have been assigned to those genes (e.g. functions, phenotypes, etc) but also a higher level of understanding of how those attributes relate to one another. For example, while 'interstrand cross-link repair' and 'DNA repair' are not identical terms, 'interstrand cross-link repair' is a type of 'DNA repair'. The similarity algorithm takes the structure of the Gene Ontology (a structured vocabulary that describes functions and how they relate to each other) into consideration when calculating similarity.

#### Translator Workflow

Workflow/modules diagram here?

### The Power of  Translator

### Results

#### Disease-Associated Genes (retrieved from BioLink MONDO ids) 

|   | input id      | input symbol              | hit id     | hit symbol | description            |  relation                | sources                     | modules |
|---|---------------|---------------------------|------------|------------|------------------------|--------------------------|-----------------------------|---------|
| 0 | MONDO:0008667 | von Hippel-Lindau disease | HGNC:12687 | VHL        | Von Hippel Lindau gene | pathogenic_for_condition | ctd, omim, orphane, clinvar | Mod0    |
| 1 | MONDO:0008667 | von Hippel-Lindau disease | HGNC:1582  | CCND1      | Cyclin D1              | contributes to           | omim, ctd                   | Mod0    |
| 2 | MONDO:0008667 | von Hippel-Lindau disease | HGNC:23057 | BRK1       | BRICK1 subunit of SCAR/WAVE actin nucleating complex | pathogenic_for_condition | clinvar                     | Mod0    |


Since VHL involved blood vessel proliferation, the contribution of a Cyclin seems meaningful.

The association of BRK1 with VHL is not initially obvious until one observes that the gene is immediately distal to the VHL locus and that ClinVar variants associated with BRK1 are often deletions which include the VHL locus. Also, clinical observations suggest the BRK1 deletion blocks the development of VHL-associated renal carcinoma. 

#### Mod1A Functional Similarity

##### Find similar genes based on GO functional annotations using OntoBio Jaccard similarity

|   | hit id    | hit symbol | description              | input id   | input symbol | score    | module |
|---|-----------|------------|--------------------------|------------|--------------|----------|--------|
| 3 | HGNC:7666 | NCKAP1     | NCK associated protein 1  (SCAR/WAVE complex) | HGNC:23057 | BRK1         | 0.835714 | Mod1A  |

This result is an association of limited likely clinical relevance to VHL.

#### MOD1B Phenotype Similarity

##### Find similar genes based on OwlSim calculated Phenotype Similarity

|   | hit id     | hit symbol | description | input id   | input symbol | score    | module |
|---|------------|------------|-------------|-----------|--------------|----------|--------|
| 7 | HGNC:5477  | IGH        | immunoglobulin heavy locus | HGNC:1582  | CCND1        | 1.000000 | Mod1B  |
| 5 | HGNC:6913  | MAX        | MYC associated factor X    | HGNC:12687 | VHL          | 0.647482 | Mod1B  |
| 0 | HGNC:26034 | SDHAF2     | succinate dehydrogenase complex assembly factor 2 | HGNC:12687 | VHL          | 0.629371 | Mod1B  |
| 4 | HGNC:6971  | MDH2       | malate dehydrogenase 2 | HGNC:12687 | VHL          | 0.572727 | Mod1B  |
| 1 | HGNC:16636 | KIF1B      | kinesin family member 1B | HGNC:12687 | VHL          | 0.559557 | Mod1B  |


Among the phenotypic similarity hits, one finds a gene associated with a known oncogene (MYC).  Another hit, SDHAF2, is associated with the SDH complex which may have involvement in a significant portion of cases of phaeochromocytoma (another phenotype expressed in VHL). The significance of the other hits is less clear.

#### Mod1E Protein Interaction

No results?