## Orange QB1.2_FA_Gene_Pathogenic_Variants

### Query:
What core FA gene variants are pathogenic, and for what conditions? (i.e. cause or contribute to pathogenic outcomes)

### Goals:
1. A benchmarking query to assess information in the Translator system about pathogenicity of variants in human FA core genes.
2. This query is independently answerable using only CIViC data accessible via Wikidata, or ClinVar data accessible via Monarch/Biolink. This query will be used as a simple test case for aggregating results that are from different primary sources,  served different knowledge beacons, and may use differnet IRIs for equivalent concepts.  

### Proposed Data Types, Sources, and Access Endpoints:
1. ClinVar variant-disease associations (via Monarch/Biolink)
2. CIViC variant-disease associations (via Wikidata, and soon via Biolink))
  

### Proposed Sub-Queries/Tasks:
**Input:** FA Gene X  (used FANCC and BRCA2 as exemplars):
  
1. Retrieve all variants of Gene X  
    `Gene -[has_affected_feature]-> Variant (Monarch)`  
    `Gene-[biological variant of] -> Variant (Wikidata)`  

2. Retrieve all diseases caused by variants in set above  
 `Variant -[causes_or_contribues_to_condition*]-> Disease (Monarch)`  
`Variant-[positive diagnostic predictor] -> Variant (Wikidata)`  
   
**Output:** Set of diseases associated with variant in FA gene(s)
  
  
