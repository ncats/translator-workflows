# Orange Team Workflow II TIDBITS

## Overview

### Candidate drug target discovery
An important area of focus in any rare disease research is the investigation of candidate drug targets. One means of identifying novel genes for further experimentation is through identifying candidate genes through analysis based on curated and structured data attributes. These attributes could be functions, phenotypes, interactions, co-expression results, etc. The distinction is that this is not primary data but data that has been published, then curated in structured databases as knowledge in a machine readable format. The inderect connections that come from this data modeling are what drive these types of analysis.

### The existing way
Traditionally, candidates are identied by querying pubmed, reading relevant literature, and leveraging domain expertise to identify and construct new ideas from the bits of knowledge extracted from the free text. Those ideas are then tested in the laboratory and iterated upon. On the other end of the spectrum, experimental high throughput methods generate lists of candidates that are so massive they are difficult to prioritize. There has to be a better way!

### The Translator way
The following is an example analysis that leverages curated knowledge (extracted and structured by professional curators with expertise in the domain) that has been semantically modeled to support machine readability in advanced querying and semantic similarity search algorithms. Essentially, genes are identified as similar based not only on the attributes that have been assigned to those genes (e.g. functions, phenotypes, etc) but also a higher level of understanding of how those attributes relate to one another. For example, while 'interstrand cross-link repair' and 'DNA repair' are not identical terms, 'interstrand cross-link repair' is a type of 'DNA repair'. The similarity algorithm takes the structure of the Gene Ontology (a structured vocabulary that describes functions and how they relate to each other) into consideration when calculating similarity.

#### Module1 Gene Based Analysis
We have developed workflow modules representing a collection of algorithms designed to start a set of genes associated with a disease and find candidate genes for further research based on a variety of similarity criteria.

The initial step in this analysis is to provide a disease of interest as the input. The entire system relies on stable identifiers from structured vocabularies such as the Monarch Disease Ontology (MONDO), rather than simply providing the text name of a disease.

The workflow defined here has been initially applied to explore two candidate rare diseases.

## TIDBIT 1 -  Fanconi Anemia

### Background

Background Fanconi anemia is a rare genetic disease featuring characteristic developmental abnormalities, a progressive pancytopenia, genomic instability, and predisposition to cancer [1, 2]. The FA pathway contains a multiprotein core complex, including at least twelve proteins that are required for the monoubiquitylation of the FANCD2/FANCI protein complex and for other functions that are not well understood [3–6]. The core complex includes the Fanconi proteins FANCA, FANCB, FANCC, FANCE, FANCF, FANCG, FANCL, and FANCM. At least five additional proteins are associated with the FA core complex, including FAAP100, FAAP24, FAAP20, and the histone fold dimer MHF1/MHF2 [1, 4, 7–10]. The core complex proteins function together as an E3 ubiquitin ligase assembly to monoubiquitylate the heterodimeric FANCI/FANCD2 (ID) complex. The monoubiquitylation of FANCD2 is a surrogate marker for the function of the FA pathway [11]. USP1 and its binding partner UAF1 regulate the deubiquitination of FANCD2 [12]. The breast cancer susceptibility and Fanconi proteins FANCD1/BRCA2, the partner of BRCA2 (PALB2/FANCN), a helicase associated with BRCA1 (FANCJ/BACH1), and several newly identified components including FAN1, FANCO/RAD51C, and FANCP/SLX4 [13–17] participate in the pathway to respond to and repair DNA damage. (needs update with new refs)

### Results

Workflow 2 FA results to be summarized here...

## TIDBIT 2 -  Von Hippel Lindau Disease

### Background

Von [Hippel-Lindau syndrome (VHL)](http://omim.org/entry/193300) is a dominantly inherited familial cancer syndrome predisposing to a variety of malignant and benign neoplasms, most frequently retinal, cerebellar, and spinal hemangioblastoma, renal cell carcinoma (RCC), pheochromocytoma, and pancreatic tumors.

By positional cloning, Latif et al. (1993) identified the [VHL tumor suppressor gene](http://omim.org/entry/608537).

### Results

#### Disease-Associated Genes (retrieved from BioLink MONDO ids) 

|   | input_id      | input_symbol              | hit_id     | hit_symbol | relation                 | sources                     | modules |
|---|---------------|---------------------------|------------|------------|--------------------------|-----------------------------|---------|
| 0 | MONDO:0008667 | von Hippel-Lindau disease | HGNC:12687 | VHL        | pathogenic_for_condition | ctd, omim, orphane, clinvar | Mod0    |
| 1 | MONDO:0008667 | von Hippel-Lindau disease | HGNC:1582  | CCND1      | contributes to           | omim, ctd                   | Mod0    |
| 2 | MONDO:0008667 | von Hippel-Lindau disease | HGNC:23057 | BRK1       | pathogenic_for_condition | clinvar                     | Mod0    |

#### Mod1A Functional Similarity

##### Find similar genes based on GO functional annotations using OntoBio Jaccard similarity

|   | hit_id    | hit_symbol | input_id   | input_symbol | score    | module |
|---|-----------|------------|------------|--------------|----------|--------|
| 3 | HGNC:7666 | NCKAP1     | HGNC:23057 | BRK1         | 0.835714 | Mod1A  |

#### MOD1B Phenotype Similarity

##### Find similar genes based on OwlSim calculated Phenotype Similarity

|   | hit_id     | hit_symbol | input_id   | input_symbol | score    | module |
|---|------------|------------|------------|--------------|----------|--------|
| 7 | HGNC:5477  | IGH        | HGNC:1582  | CCND1        | 1.000000 | Mod1B  |
| 5 | HGNC:6913  | MAX        | HGNC:12687 | VHL          | 0.647482 | Mod1B  |
| 0 | HGNC:26034 | SDHAF2     | HGNC:12687 | VHL          | 0.629371 | Mod1B  |
| 4 | HGNC:6971  | MDH2       | HGNC:12687 | VHL          | 0.572727 | Mod1B  |
| 1 | HGNC:16636 | KIF1B      | HGNC:12687 | VHL          | 0.559557 | Mod1B  |

#### Mod1E Protein Interaction

No results?