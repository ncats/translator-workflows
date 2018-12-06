
# Workflow 7 - Module 1 (Unordered Pathway)
This notebook will focus on module 1 of workflow 7.  The objective is to return all the genes and metabolites in a pathway in no parituclar order.  The first prototype use case for this workflow will focus on Codeine.  We only try to return genes because GNBR does not have direct chemical-chemical associations.

## Step 1. Query SMPDB API
First we query statements endpoint of SMPDB for all genes related to Codeine to generate a set of "ground truth" answers for comparison to GNBR. This task requires two functions:
1. Map a concept into SMPDB using keyword search
2. Query all related genes (any type of relationship)

The lookup functions here are a starting point and will become more refined as we churn through more examples and figure out what does and doesn't work.


```python
from pprint import pprint
from __future__ import print_function
from tkbeacon import build, KnowledgeSource
from tkbeacon.rest import ApiException

def get_concepts(query):
    b = build(KnowledgeSource.SMPDB)
    terms = [i.lower() for i in query]
    concepts = b.get_concepts(keywords=terms)
    return [b.get_concept_details(i.id) for i in concepts if i.name.lower() in terms]

def get_genes(query):
    b = build(KnowledgeSource.SMPDB)
    concepts = get_concepts(query)
    query_ids = [i.id for i in concepts]
    statements = b.get_statements(s=query_ids, edge_label='related_to', t_categories=['protein'])
    return statements
```

### Chemical Lookup
First we lookup Codeine and see what information smpdb has about it.


```python
chemical = ['Codeine']
concepts = get_concepts(chemical)
pprint(concepts)
```

    [{'categories': ['metabolite'],
     'description': None,
     'details': None,
     'exact_matches': [],
     'id': 'CHEBI:16714',
     'name': 'Codeine',
     'symbol': None,
     'synonyms': None,
     'uri': 'https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:16714'}]


### Related Genes
Now we get all related genes, with the most generic definition of relatedness.


```python
smpdb_genes = get_genes(query=chemical)
pprint(smpdb_genes)
```

    [{'id': 'CHEBI:16714|related_to|consumption_controlled_by|UNIPROT:P08684',
     'object': {'categories': ['protein'],
                'id': 'UNIPROT:P08684',
                'name': 'Cytochrome P450 3A4'},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'consumption_controlled_by'},
     'subject': {'categories': ['metabolite'],
                 'id': 'CHEBI:16714',
                 'name': 'Codeine'}},
     {'id': 'CHEBI:16714|related_to|consumption_controlled_by|UNIPROT:P10635',
     'object': {'categories': ['protein'],
                'id': 'UNIPROT:P10635',
                'name': 'Cytochrome P450 2D6'},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'consumption_controlled_by'},
     'subject': {'categories': ['metabolite'],
                 'id': 'CHEBI:16714',
                 'name': 'Codeine'}},
     {'id': 'CHEBI:16714|related_to|consumption_controlled_by|UNIPROT:P16662',
     'object': {'categories': ['protein'],
                'id': 'UNIPROT:P16662',
                'name': 'UDP-glucuronosyltransferase 2B7'},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'consumption_controlled_by'},
     'subject': {'categories': ['metabolite'],
                 'id': 'CHEBI:16714',
                 'name': 'Codeine'}}]


Looks like we get all the standard metabolic genes.  Compared with the [PharmGKB pathway](https://www.pharmgkb.org/pathway/PA146123006) it seems that we are missing the morphine arm, but that is ok for now.

## Step 2. Query GNBR API
We will start off with very basic usage of the GNBR API to query genes associated with Codeine.


```python
import gnbr_beacon

gnbr_concepts = gnbr_beacon.ConceptsApi()
gnbr_statements = gnbr_beacon.StatementsApi()
```

### Chemical  Lookup


```python
chemical = ['Codeine']
concepts = gnbr_concepts.get_concepts(keywords=chemical)
details = [gnbr_concepts.get_concept_details(i.id) for i in concepts]
pprint(details)
```

    [{'categories': ['Entity', 'Chemical'],
     'description': 'A confirmative method was developed for determining five '
                    'poppy alkaloids including morphine , codeine , papaverine , '
                    'tibane , noscapine in chafing dish ingredients by high '
                    'performance liquid chromatography coupled with triple '
                    'quadrupole linear ion trap mass spectrometry -LRB- HPLC-Q '
                    'Trap MS -RRB- . Keywords used were '
                    'glucose-6-phosphate_dehydrogenase -LRB- G6PD -RRB- deficiency '
                    ', anesthesia , analgesia , anxiolysis , management , favism , '
                    'hemolytic_anemia , benzodiazepines , codeine , codeine '
                    'derivatives , ketamine , barbiturates , propofol , opioids , '
                    'fentanyl , and inhalation anesthetics . OBJECTIVE : To '
                    'compare the performance of ibuprofen vs codeine for '
                    'postoperative_pain management after tonsillectomy as measured '
                    'by need for emergency_department -LRB- ED -RRB- treatment for '
                    'pain_and / or_dehydration .',
     'details': [{'tag': 'mentions', 'value': '835'}],
     'exact_matches': None,
     'id': 'MESH:D003061',
     'name': 'codeine',
     'symbol': None,
     'synonyms': ['codeine',
                  'Codeine',
                  'codeine phosphate',
                  'N-methylmorphine',
                  'Codeine phosphate',
                  'N-methyl morphine',
                  'codeine/dextropropoxyphen'],
     'uri': 'MESH:D003061'}]


### Related Genes


```python
ids = [i.id for i in concepts]
gnbr_genes = gnbr_statements.get_statements(s=ids, t_categories=['Gene'])
pprint(gnbr_genes)
```

    [{'id': '33560061',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'NCBIGENE:6580',
                'name': 'OCT1'},
     'predicate': {'edge_label': 'disrupts',
                   'negated': None,
                   'relation': 'inhibits'},
     'subject': {'categories': ['Entity', 'Chemical'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '33560063',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'NCBIGENE:7363',
                'name': 'UGT2B4'},
     'predicate': {'edge_label': 'affects abundance of',
                   'negated': None,
                   'relation': 'desreases expression or production of'},
     'subject': {'categories': ['Entity', 'Chemical'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '33560059',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'NCBIGENE:2539',
                'name': 'G6PD'},
     'predicate': {'edge_label': 'affects activity of',
                   'negated': None,
                   'relation': 'activates'},
     'subject': {'categories': ['Entity', 'Chemical'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '33560058',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'NCBIGENE:1576',
                'name': 'CYP3A4'},
     'predicate': {'edge_label': 'disrupts',
                   'negated': None,
                   'relation': 'inhibits'},
     'subject': {'categories': ['Entity', 'Chemical'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '33560062',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'NCBIGENE:717',
                'name': 'CO2'},
     'predicate': {'edge_label': 'affects activity of',
                   'negated': None,
                   'relation': 'activates'},
     'subject': {'categories': ['Entity', 'Chemical'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '33560056',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'NCBIGENE:1564',
                'name': 'CYP2D'},
     'predicate': {'edge_label': 'affects abundance of',
                   'negated': None,
                   'relation': 'desreases expression or production of'},
     'subject': {'categories': ['Entity', 'Chemical'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '33560060',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'NCBIGENE:5730',
                'name': 'PGD2'},
     'predicate': {'edge_label': 'affects molecular modification of',
                   'negated': None,
                   'relation': 'metabolized by'},
     'subject': {'categories': ['Entity', 'Chemical'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '33560064',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'NCBIGENE:7364',
                'name': 'UGT2B7'},
     'predicate': {'edge_label': 'affects activity of',
                   'negated': None,
                   'relation': 'blocks activation of'},
     'subject': {'categories': ['Entity', 'Chemical'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '33560057',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'NCBIGENE:1565',
                'name': 'CYP2D6'},
     'predicate': {'edge_label': 'disrupts',
                   'negated': None,
                   'relation': 'inhibits'},
     'subject': {'categories': ['Entity', 'Chemical'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '33560065',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'NCBIGENE:81668',
                'name': 'GH'},
     'predicate': {'edge_label': 'affects abundance of',
                   'negated': None,
                   'relation': 'affects expression or production of'},
     'subject': {'categories': ['Entity', 'Chemical'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}}]


## Step 3. Validation
Validation happens in two steps.
1. Harmonize concepts across knowledge sources.
2. Compute performance metrics
3. Investigate "wrong" answers

### Harmonize Concepts
First we need to map concepts from SMPDB into GNBR.  We might imagine doing the reverse mapping, but for now we are keeping it as simple as possible.  We map concepts using simple keyword lookup.


```python
mapped_genes = gnbr_concepts.get_concepts(keywords=[i.object.name for i in smpdb_genes])
pprint(mapped_genes)
```

    [{'categories': ['Entity', 'Gene'],
     'description': None,
     'id': 'NCBIGENE:1576',
     'name': 'CYP3A4'},
     {'categories': ['Entity', 'Gene'],
     'description': None,
     'id': 'NCBIGENE:107987479',
     'name': 'cytochrome P450 2D6'},
     {'categories': ['Entity', 'Gene'],
     'description': None,
     'id': 'NCBIGENE:1565',
     'name': 'CYP2D6'},
     {'categories': ['Entity', 'Gene'],
     'description': None,
     'id': 'NCBIGENE:7364',
     'name': 'UGT2B7'}]


We can see a problem with the mapping here - we end up pulling in synonyms (orthologs).  Species tags are not currently supported on the GNBR API, though they are in the underlying neo4j.  Future versions of the API will species info for genes.

### Metrics
The metrics we will compute for this module are Jaccard similarity and Average Precision.  Jaccard similarity doesn't explicitly take the ordering of the answers into account, but it is affected by the number of returned answers.

Average precision explicitly considers rankings and is less sensitive to the total number of results returned. Thus it is generally preferred for search algorithms that return long lists of results, where the top results should be the most relevant.


```python
def jaccard_index(query_results, ground_truths):
    numerator = len(set(query_results) & set(ground_truths))
    demoninator = len(set(query_results + ground_truths))
    jc = 1.0*numerator/demoninator
    return jc

def avg_prec(query_results, ground_truths):
    hits, precision = 0, 0
    for n, result in enumerate(query_results):
        if result in ground_truths:
            hits += 1
            precision += hits/(n+1)
    avg_precision = precision/len(ground_truths)
    return avg_precision
```


```python
ap = avg_prec( [i.object.id for i in gnbr_genes], [i.id for i in mapped_genes] )
jc = jaccard_index( [i.object.id for i in gnbr_genes], [i.id for i in mapped_genes] )
print('Jaccard: %0.2f'%jc)
print('Average Precision: %0.2f'%ap)
```

    Jaccard: 0.27
    Average Precision: 0.21


### Further Investigation

#### Right Answers
Frist we see what we got right.  It looks like we did get all of the metabolism genes from smpdb, just not as the top of the results.


```python
mapped_ids = [i.id for i in mapped_genes]
pprint([i.object.name for i in gnbr_genes if i.object.id in mapped_ids])
```

    ['CYP3A4', 'UGT2B7', 'CYP2D6']


#### Wrong Answers
Now we see what we got "wrong".  It looks GNBR returnins a number of additional off target and metabolism genes, and these are what is dragging the score down.


```python
mapped_ids = [i.id for i in mapped_genes]
pprint([i for i in gnbr_genes if i.object.id not in mapped_ids])
```

    [{'id': '33560061',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'NCBIGENE:6580',
                'name': 'OCT1'},
     'predicate': {'edge_label': 'disrupts',
                   'negated': None,
                   'relation': 'inhibits'},
     'subject': {'categories': ['Entity', 'Chemical'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '33560063',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'NCBIGENE:7363',
                'name': 'UGT2B4'},
     'predicate': {'edge_label': 'affects abundance of',
                   'negated': None,
                   'relation': 'desreases expression or production of'},
     'subject': {'categories': ['Entity', 'Chemical'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '33560059',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'NCBIGENE:2539',
                'name': 'G6PD'},
     'predicate': {'edge_label': 'affects activity of',
                   'negated': None,
                   'relation': 'activates'},
     'subject': {'categories': ['Entity', 'Chemical'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '33560062',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'NCBIGENE:717',
                'name': 'CO2'},
     'predicate': {'edge_label': 'affects activity of',
                   'negated': None,
                   'relation': 'activates'},
     'subject': {'categories': ['Entity', 'Chemical'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '33560056',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'NCBIGENE:1564',
                'name': 'CYP2D'},
     'predicate': {'edge_label': 'affects abundance of',
                   'negated': None,
                   'relation': 'desreases expression or production of'},
     'subject': {'categories': ['Entity', 'Chemical'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '33560060',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'NCBIGENE:5730',
                'name': 'PGD2'},
     'predicate': {'edge_label': 'affects molecular modification of',
                   'negated': None,
                   'relation': 'metabolized by'},
     'subject': {'categories': ['Entity', 'Chemical'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '33560065',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'NCBIGENE:81668',
                'name': 'GH'},
     'predicate': {'edge_label': 'affects abundance of',
                   'negated': None,
                   'relation': 'affects expression or production of'},
     'subject': {'categories': ['Entity', 'Chemical'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}}]


#### Or Promising Leads?

Let's look into a couple of these.  As a point of comparison, we can check out some of the [clincial annotations from PharmGKB](https://www.pharmgkb.org/chemical/PA449088/clinicalAnnotation).

##### UGT2B4
This is not currently listed as a PK Gene in pharmGKB and has been flagged by the curators as a potential candidate for experimental follow up.


```python
evidence = gnbr_statements.get_statement_details(statement_id=33560063)
pprint(evidence)
```

    {'annotation': None,
     'evidence': [{'date': None,
                   'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
                   'id': 'PUBMED:12920168',
                   'name': 'Codeine is not a useful UGT2B7 probe substrate because '
                           'of significant glucuronidation by UGT2B4 .',
                   'uri': 'https://www.ncbi.nlm.nih.gov/pubmed/12920168'},
                  {'date': None,
                   'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
                   'id': 'PUBMED:12920168',
                   'name': 'Codeine was glucuronidated equally well by UGT2B4 and '
                           'UGT2B7 .',
                   'uri': 'https://www.ncbi.nlm.nih.gov/pubmed/12920168'}],
     'id': '33560063',
     'is_defined_by': None,
     'provided_by': None,
     'qualifiers': None}


#### CDP2D7
This one was removed from PharmGKB after it was shown to be a psuedogene that did not replicate after the initial studies identifying it as a PK Gene. However, this is not uncontroversial. A recent study in drisophila suggests the existence of pseudo-psuedogenes, which are only expressed in neural tissues.


```python
evidence = gnbr_statements.get_statement_details(statement_id=33560056)
pprint(evidence)
```

    {'annotation': None,
     'evidence': [{'date': None,
                   'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
                   'id': 'PUBMED:28837793',
                   'name': 'Brain CYP2D metabolizes codeine to morphine , a '
                           'bioactivation step required for codeine analgesia .',
                   'uri': 'https://www.ncbi.nlm.nih.gov/pubmed/28837793'},
                  {'date': None,
                   'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
                   'id': 'PUBMED:17017525',
                   'name': 'Genotyping revealed the presence of the frame-shift '
                           'mutation 138delT only in those subjects who expressed '
                           'the brain variant CYP2D7 , which metabolizes codeine '
                           'exclusively to morphine unlike hepatic CYP2D6 that '
                           'metabolizes codeine to nor codeine and morphine .',
                   'uri': 'https://www.ncbi.nlm.nih.gov/pubmed/17017525'},
                  {'date': None,
                   'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
                   'id': 'PUBMED:25630571',
                   'name': 'Rats received 7-day nicotine -LRB- 1 mg/kg '
                           'subcutaneously -RRB- and/or a single propranolol -LRB- '
                           'CYP2D mechanism-based inhibitor ; 20 g '
                           'intracerebroventricularly -RRB- pretreatment , and '
                           'then were tested for analgesia and drug levels '
                           'following codeine -LRB- 20 mg/kg intraperitoneally '
                           '-RRB- or morphine -LRB- 3.5 mg/kg intraperitoneally '
                           '-RRB- , matched for peak analgesia .',
                   'uri': 'https://www.ncbi.nlm.nih.gov/pubmed/25630571'},
                  {'date': None,
                   'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
                   'id': 'PUBMED:25630571',
                   'name': 'The role of nicotine-induced rat brain CYP2D in the '
                           'central metabolic activation of peripherally '
                           'administered codeine and resulting analgesia was '
                           'investigated .',
                   'uri': 'https://www.ncbi.nlm.nih.gov/pubmed/25630571'},
                  {'date': None,
                   'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
                   'id': 'PUBMED:15051713',
                   'name': 'In contrast , when expressed in Neuro2a cells , brain '
                           'variant CYP2D7 metabolized codeine to morphine with '
                           'greater efficiency compared with the corresponding '
                           'activity in cells expressing CYP2D6 .',
                   'uri': 'https://www.ncbi.nlm.nih.gov/pubmed/15051713'},
                  {'date': None,
                   'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
                   'id': 'PUBMED:25630571',
                   'name': 'UNASSIGNED : CYP2D metabolically activates codeine to '
                           'morphine , which is required for codeine analgesia .',
                   'uri': 'https://www.ncbi.nlm.nih.gov/pubmed/25630571'},
                  {'date': None,
                   'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
                   'id': 'PUBMED:18838503',
                   'name': 'Furthermore , CYP2D7 did not produce any morphine from '
                           'codeine .',
                   'uri': 'https://www.ncbi.nlm.nih.gov/pubmed/18838503'}],
     'id': '33560056',
     'is_defined_by': None,
     'provided_by': None,
     'qualifiers': None}


##### OCT1


```python
evidence = gnbr_statements.get_statement_details(statement_id=33560061)
pprint(evidence)
```

    {'annotation': None,
     'evidence': [{'date': None,
                   'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
                   'id': 'PUBMED:27128732',
                   'name': 'Increased odds ratio of early discontinuation of '
                           'metformin was only associated with codeine , an '
                           'inhibitor of organic_cation_transporter_1 in both '
                           'cohorts -LSB- adjusted odds ratio -LRB- OR -RRB- in '
                           'Danish cohort -LRB- 95 % CI -RRB- : 1.13 -LRB- '
                           '1.02-1.26 -RRB- , adjusted OR in American cohort -LRB- '
                           '95 % CI -RRB- : 1.32 -LRB- 1.19-1.47 -RRB- -RSB- .',
                   'uri': 'https://www.ncbi.nlm.nih.gov/pubmed/27128732'}],
     'id': '33560061',
     'is_defined_by': None,
     'provided_by': None,
     'qualifiers': None}


## Conclusion
Not a bad start.  We see that GNBR does return all of the correct genes, but they are not all ranked highly.  We also get back a number of results that are valid, but not necessarily the stuff of curated databases.  In this particular case, we see off targets, as well as some obscure and contraversial results, and a couple of true errors.  Being able to inspect the sentences makes it pretty easy to follow up and sort these out.  However, this taks might be daunting for larger, more complex pathways.

#### Post Script
Below is some prototype code using the neo4j bolt interface for an alternative method of querying.  It doesn't seem to do much better.


```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=('',''))

def pk_gene(tx, source):
    query = """
    MATCH p=(:Chemical {uri: $source})-[:STATEMENT]->(:Gene)
    RETURN nodes(p) as n, relationships(p) as r
    """
    result = []
    for record in tx.run(query, source=source):
        result.extend(record['r'])
    return result



def pk_score(relationship):
    score = max( [relationship[i] for i in ['O','X','Z']] )
    return score

def max_score(relationship):
    score = max(relationship.values())
    return score
```


```python
with driver.session() as neo4j:
    pk_genes = neo4j.read_transaction(pk_gene, source=ids[0])

pk_genes = sorted(pk_genes, key=pk_score, reverse=True)
for association in pk_genes:
    pprint([x['name'] for x in association.nodes])
```

    ['codeine', 'OCT1']
    ['codeine', 'UGT2B4']
    ['codeine', 'CYP2D']
    ['codeine', 'CYP2D6']
    ['codeine', 'GH']
    ['codeine', 'UGT2B7']
    ['codeine', 'CO2']
    ['codeine', 'PGD2']
    ['codeine', 'G6PD']
    ['codeine', 'CYP3A4']



```python

```
