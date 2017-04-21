## Orange Team CQ#2.4

### Query: 
What genes and pathways are uniquely targeted by HSCT conditioning drugs that are well- vs poorly- tolerated by FA patients?
  
### Goal:
FA patients tolerate certain Hematopoietic Stem Cell Transplant (HCST) pre-conditioning drugs poorly (e.g. fludarabine), while they tolerate others well (e.g. cyclophosphamide, busulfan). This set of queries aims to find genes/pathways that are differentially targeted by well- vs poorly- tolerated conditioning drugs. This results can help identify correlations between drug targets and HSCT treatment outcomes that may provide mechanistic insight into this phenomenon, and inform selection of better therapeutic regimens for FA patients. This CQ serves the larger HSCT Pre-Conditioning Demonstrator described [here](https://github.com/NCATS-Tangerine/cq-notebooks/wiki/HSCT-Pre-Conditioning-FA-Demonstrator).

  
### Data Types, Sources, and Routes:
1. **Drug-Target Interactions** - from DGIdb, via [DGIdb API](http://dgidb.genome.wustl.edu/api)
2. **Protein-Gene Associations** - from Ensembl, via SciGraph ([BioLink API](https://api.monarchinitiative.org/api/) call or [Monarch API cypher query](https://scigraph-data-dev.monarchinitiative.org/scigraph/docs/#!/cypher/execute)?)
2. **Gene-Pathway Membership** - from Reactome, via SciGraph ([BioLink API](https://api.monarchinitiative.org/api/) call or [Monarch API cypher query](https://scigraph-data-dev.monarchinitiative.org/scigraph/docs/#!/cypher/execute)?)
  
### Sub-Queries/Tasks:
   
**Input:** Two HSCT conditioning drug sets: **(1)** well-tolerated by FA patients (Set1d); **(2)** poorly-tolerated by FA patients (Set2d)

  1. Retrieve **proteins** targeted by set of well-tolerated HSCT conditioning drugs --> Set1p 
  2. Retrieve **proteins** targeted by set of well-tolerated HSCT conditioning drugs --> Set2p  
  3. Retrieve **genes** encoding proteins in Set1p vs Set2p --> Set1g, Set2g
  4. Retrieve **pathways** associated with genes in Set1g vs Set2g --> Set1pw, Set2pw
  5. Retreive other **genes** involved in pathways in Set1pw vs Set2pw --> Set1g', Set2g'
  6. Execute set comparison analysis to return the set of **genes** that is uniquely targetd by poorly tolerated drugs
  (i.e. effected directly or indirectly by poorly tolerated drugs, but not affected by well-tolerated drugs)

**Output:** Set of genes that may be uniquely targeted by pre-conditioning drugs that are poorly tolerated by FA patients.
  
From here a number of follow up analyses are possible - e.g. GO term enrichment analysis to identify processes/functions uniquely affected under each condition, and correlating this with pathways/functions that are compromised in FA.

--------

*Note that the subqueries above can be parameterized in any number of ways in their implementation (e.g. select subsets of specific pathways to expand on, or specific subset of genes within each pathway to expand to, or different sources or routes for data used in the queries). Different combinations of parameters can be explored using different notebooks in this directory.*
