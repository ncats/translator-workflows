
## OrangeQ1.5 Regulatory_Motif_Signature: 

### Query:
What genes show similar regulatory motif signatures as FA-core genes?

### Goal:
This query aims to expand the FA-core gene set based on upstream TF binding site motif patterns.

### Data Types, Sources, and Routes:
1. Motifs from [JASPAR](http://jaspar.genereg.net/html/DOWNLOAD/bed_files/)
2. Gene upstream regions from [UCSC](http://hgdownload.cse.ucsc.edu/goldenPath/hg19/bigZips/) 
3. Gene-Gene associations generated from upstream motifs via __TBD__  rsn  
    (1M RDF statements)
  
### Sub-Queries/Tasks:
   
**Input:** NCBIGene identifiers for 26 FA-core genes (three symbols unresolved)  
  1. Assemble Jaspar Motif BED dataset  
  2. Assemble upstream region BED files for three extents [1k,2k,5k]  
  3. Collapse RefSeq based upstream regions into NCBI Gene based regions    
  4. Intersect Motif and NCBI regions to get ordered motifs associated with gene_start_regions  
  5. Reduce ordered sequence of motifs per gene_start_site to partial ordered set of dimotifs per region
  6. Pairwise compare and score all gene's sets of dimotifs
  7. Semanticly model gene->region->motifset->motif and pairwise scoreing
  8. Generate RDF for knowlege store
  9. Load datastore and query

**Output:** GeneSetQ1.5 (human genes with similar affinities for TF's as FA-core genes)
  
     currently ~380 genes showing GO enrichment for
        cytoplasm|organelle
        metabolic process
        protein binding  

Goals for the hackathon could include

- to reduce this number of hits
- make it tunable.  
-----

#### Running questions  

If motifs (avg length 14bp) overlap, how should they be considered?

 a. same strand, different strand. partial over lap full overlap
 b. as logical OR?  what about when the strands are split?  both motifs could be available.
 c. is there a minimal working distance between motifs (binding sites) a TF needs to bind?


How little may regions have in common and still warrent an association?

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
