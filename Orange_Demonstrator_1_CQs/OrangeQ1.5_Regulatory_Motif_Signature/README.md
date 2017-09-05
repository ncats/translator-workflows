
## OrangeQ1.5 Regulatory_Motif_Signature: 

### Query:
What genes show similar regulatory motif signatures as FA-core genes?

### Goal:
This query aims to expand the FA-core gene set based on upstream TF binding site motif patterns.

### Data Types, Sources, and Routes:
1. Motifs from [JASPAR](http://jaspar.genereg.net/html/DOWNLOAD/bed_files/)
2. Transcript upstream regions from [UCSC](http://hgdownload.cse.ucsc.edu/goldenPath/hg19/bigZips/)
3. Transcript Gene associations from [NCBI](ftp://ftp.ncbi.nih.gov/gene/DATA/gene2refseq.gz)  
4. Gene-Gene associations generated from the above sources  
(about a million RDF statements)
  
### Sub-Queries/Tasks:
   
**Input:** NCBIGene identifiers for 26 FA-core genes (three symbols unresolved)  
  1. Assemble/merge Jaspar Motif BED dataset from constituent files    
  2. Assemble upstream region BED files for three extents [1k,2k,5k] (from fasta deflines)  
  3. Collapse RefSeq based upstream regions into NCBI Gene based upstream regions    
  4. Intersect Motif and NCBI regions to get ordered motifs within gene start regions  
  5. Reduce ordered sequence of motifs per gene start site to a partial ordered set of 'dimotifs' per region  
  6. Pairwise compare and score all gene's start regions sets of dimotifs  
  7. Semantically model gene->region->motifset->motif and pairwise scoring  
  8. Format resulting data as RDF in the shape of the model for loading into a knowledge store  
  9. Load (blazegraph) knowlage store and query for genes associations with FA genes.  
 10. Send resulting gene set to wet lab for experimentation
 
**Output:** GeneSetQ1.5 (human genes with similar affinities for TF's as FA-core genes)
  
Initial foray surfaced several hundred genes showing GO enrichment for  
 - cytoplasm|organelle  
 - metabolic process  
 - protein binding  

And enough BioMedical Researcher 'spot check' enthusiasm to warrant continuing.


-----
### At the Hackathon
At the hackathon a machine to run blazegraph exposing the [dataset](file://translator.ncats.io/translator/Orange/jaspar.nt)
only almost appeared so the basics for getting a local blazegraph up as a http accessible
SPARQL endpoint are outlined in [LocalBlazeGraph.ipynb](https://github.com/NCATS-Tangerine/cq-notebooks/blob/master/Orange_Demonstrator_1_CQs/OrangeQ1.5_Regulatory_Motif_Signature/LocalBlazeGraph.ipynb)

_A persistent endpoint will appear on either NCATS or Monarch servers in the very near future._
 

The very messy details on how the dataset was generated may be found [here](https://github.com/TomConlin/Jaspar_FA/blob/master/README.FA_genes_take2) but briefly,  
motifs within gene start regions are considered as adjacent ordered pairs.  
Sets of ordered pairs from different start regions are scored for similarity
by considering the proportion of ordered pairs two regions have in common compared with the total number of order pairs the regions have together.  
To avoid having too many associations I have arbitrarily discarded any which do not have at least one part in five in common.

Our input is sets of gene symbols, some of which are historical or alternative
names so the [MyGene](http://mygene.info/) api was called to return NCBIGene identifiers for the names.
The sets of input genes and their current symbols are found [here](https://github.com/NCATS-Tangerine/cq-notebooks/tree/master/FA_gene_sets).
 
This questions python notebook [CQ1.5.ipynb](https://github.com/NCATS-Tangerine/cq-notebooks/blob/master/OrangeQ1.5_Regulatory_Motif_Signature/CQ1.5.ipynb)
includes the scored set of genes with HGNC symols associated with each of the input FA genes.
 







---
#### Running questions  

If motifs (avg length 14bp) overlap, how should they be considered?

 a. same strand, different strand. partial over lap full overlap
 b. as logical OR?  what about when the strands are split?  both motifs could be available.
 c. is there a minimal working distance between motifs (binding sites) a TF needs to bind?


How little may regions have in common and still warrant an association?

  a. Current using a part in five (20%)
  b. At 20%  similarity half the FA gene set report no associations.

-----
The original Question is here:    
https://github.com/NCATS-Tangerine/ncats-ingest/issues/21


```
We need a gene set based upon any upstream transcriptional regulators
of our FA primary genes (some may have alternate primary symbols):

    FANCA, FANCB, FANCC, FANCE, FANCF, FANCG, FANCL, FANCM,
    FANCD2, FANCI, UBE2T, FANCD1 (BRCA2), FANCJ, FANCN, FANCO,
    FANCP, FANCQ, FANCR, FANCS, FANCV, FANCU, FAAP100, FAAP24,
    FAAP20, FAAP16 (MHF1), FAAP10 (MHF2)

    Favored resource is JASPAR
    http://jaspar.genereg.net/
    as [it is] open source and provisioned Wyeth's lab
```
