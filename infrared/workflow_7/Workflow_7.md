
# Notebook for Workflow 7
This notebook will focus on completion of modules 1,2 and 3 of workflow 7 (pharmacogenomics).  The first prototype use case for this workflow will focus on Codeine metabolism.

## Module 0: SMPDB Mapping
The first order of business is to query the SMPDB API for a list of chemicals and genes that can serve as both ground truth for module 1 and as inputs to modules 2 and 3.  Another non-trivial task is mapping concepts from the SMPDB ID space into GNBR.  Chemicals in SMPDB are generally referenced by CHEBI, KEGG, or HMDB identifiers, while most of GNBR uses MESH.  Our first try at this non-trivial task will attempt to map concepts by name.

### Query SMPDB API
First we query statements endpoint of SMPDB with the ID for the codeine metabolism pathway.  This returns a list of genes and chemicals in the pathway, which we then sort out.


```python
import requests

codeine_metabolism_url = 'https://kba.ncats.io/beacon/smpdb/statements?s=SMP:0000621'
response = requests.get(codeine_metabolism_url)

genes, chemicals = [], []
for relation in response.json():
        if 'protein' in relation['subject']['categories']:
            genes.append(relation['subject']['name'])
        elif 'metabolite' in relation['subject']['categories']:
            chemicals.append(relation['subject']['name'])
        else:
            print(relation['subject']['name'])
```


```python
genes
```




    ['Mu-type opioid receptor',
     'UDP-glucuronosyltransferase 2B7',
     'Cytochrome P450 3A4',
     'Cytochrome P450 2D6']




```python
chemicals
```




    ['Codeine',
     'Morphine',
     'Uridine diphosphate glucuronic acid',
     'Codeine-6-glucuronide',
     "Uridine 5'-diphosphate",
     'Oxygen',
     'NADH',
     'Norcodeine',
     'Water',
     'Formaldehyde',
     'NAD',
     'Heme']



### Map Chemicals and Genes into GNBR
Now we use the concepts endpoint on the GNBR API to lookup the names and retreive the internal IDs of the genes and chemicals returned by SMPDB.


```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

gnbr_concepts = swagger_client.ConceptsApi()
```

#### Genes
We don't do any normalization or filtering for genes.  Technically, mOR isn't a metabolism gene, but it's not such a big deal at this stage of prototyping.


```python
# genes = [i.lower() for i in genes]
genes_in_gnbr = gnbr_concepts.get_concepts(keywords=genes)
pprint(genes_in_gnbr)
```

    [{'categories': ['Entity', 'Gene'],
     'description': None,
     'id': 'ncbigene:7364',
     'name': 'UGT2B7'},
     {'categories': ['Entity', 'Gene'],
     'description': None,
     'id': 'ncbigene:1576',
     'name': 'CYP3A4'},
     {'categories': ['Entity', 'Gene'],
     'description': None,
     'id': 'ncbigene:1565',
     'name': 'CYP2D6'},
     {'categories': ['Entity', 'Gene'],
     'description': None,
     'id': 'ncbigene:107987479',
     'name': 'cytochrome_P450_2D6'}]


#### Chemicals
We do filter out "uninteresting" chemicals, some of which are sure to return hits.  These are generally ubiquitous endogenous agents that will add tons of noise.  Basically, the biochemical equivalent of stop words.


```python
blacklist = ['Oxygen','Water','Formaldehyde','NAD','NADH','Heme']
chemicals = [i.lower() for i in chemicals if i not in blacklist]
chems_in_gnbr = gnbr_concepts.get_concepts(keywords=chemicals)
pprint(chems_in_gnbr)
```

    [{'categories': ['Chemical', 'Entity'],
     'description': None,
     'id': 'MESH:D003061',
     'name': 'codeine'},
     {'categories': ['Chemical', 'Entity'],
     'description': None,
     'id': 'MESH:D009020',
     'name': 'morphine'},
     {'categories': ['Chemical', 'Entity'],
     'description': None,
     'id': 'MESH:D014535',
     'name': 'UDPGA'},
     {'categories': ['Chemical', 'Entity'],
     'description': None,
     'id': 'MESH:C010414',
     'name': 'norcodeine'}]


Because text search is exact and case sensitive there is a question of whether we should normalize strings.  Here we do it for chemicals, but not for genes.  The decision was made on the basis of what returned the best looking results.  However, we do not expect this to be our final approach.  A notable mapping failure is the mu-opiod receptor, which is present in GNBR.

## Module 1
Module 1 asks the question, "what chemicals and genes are in metabolic pathways (or mechanism of action pathways) with some query chemical X.  The first pass at this module will attempt to use GNBR, though it is likely not well suited for this problem because it does not contain pathway objects or chemical-chemical predicates.

#### Concept Lookup
First we lookup codeine in GNBR.  Hitting the details enpoint is probably unecessary, but we do it anyway just because.


```python
gnbr_concepts = swagger_client.ConceptsApi()
keywords = ['Codeine']
concepts = gnbr_concepts.get_concepts(keywords=keywords)
pprint(concepts)
```

    [{'categories': ['Chemical', 'Entity'],
     'description': None,
     'id': 'MESH:D003061',
     'name': 'codeine'}]



```python
concept_details = [gnbr_concepts.get_concept_details(concept.id) for concept in concepts]
pprint(concept_details)
```

    [{'categories': ['Chemical', 'Entity'],
     'description': None,
     'details': [{'tag': 'mentions', 'value': '803'}],
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


#### Statements Lookup
Now we lookup genes related to codeine (any relation).  Here we probably don't need to hit the statement details endpoint, but we do anyway.  The relations being returned by the GNBR endpoint are still a little wonky, but can possibly be fixed by normalization. Also, some means of filtering by confidence would be helpful.


```python
gnbr_statements = swagger_client.StatementsApi()
s = [concept.id for concept in concepts]
categories=['Gene']
statements = gnbr_statements.get_statements(s=s, t_categories=categories)
pprint(statements)
```

    [{'id': '37476030',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'ncbigene:1565',
                'name': 'CYP2D6'},
     'predicate': {'edge_label': 'affects abundance of',
                   'negated': None,
                   'relation': 'affects expression or production of'},
     'subject': {'categories': ['Chemical', 'Entity'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '37476035',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'ncbigene:7363',
                'name': 'hyodeoxycholic_acid'},
     'predicate': {'edge_label': 'disrupts',
                   'negated': None,
                   'relation': 'inhibits'},
     'subject': {'categories': ['Chemical', 'Entity'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '37476031',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'ncbigene:1576',
                'name': 'CYP3A4'},
     'predicate': {'edge_label': 'disrupts',
                   'negated': None,
                   'relation': 'inhibits'},
     'subject': {'categories': ['Chemical', 'Entity'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '37476029',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'ncbigene:1564',
                'name': 'CYP2D'},
     'predicate': {'edge_label': 'affects abundance of',
                   'negated': None,
                   'relation': 'affects expression or production of'},
     'subject': {'categories': ['Chemical', 'Entity'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '37476034',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'ncbigene:5730',
                'name': 'PGD2'},
     'predicate': {'edge_label': 'affects molecular modification of',
                   'negated': None,
                   'relation': 'metabolized by'},
     'subject': {'categories': ['Chemical', 'Entity'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '37476032',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'ncbigene:2539',
                'name': 'glucose_6-phosphate_dehydrogenase'},
     'predicate': {'edge_label': 'interacts with',
                   'negated': None,
                   'relation': 'binds'},
     'subject': {'categories': ['Chemical', 'Entity'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '37580296',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'ncbigene:81668',
                'name': 'growth_hormone'},
     'predicate': {'edge_label': 'affects abundance of',
                   'negated': None,
                   'relation': 'affects expression or production of'},
     'subject': {'categories': ['Chemical', 'Entity'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '37476028',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'ncbigene:717',
                'name': 'CO2'},
     'predicate': {'edge_label': 'disrupts',
                   'negated': None,
                   'relation': 'inhibits'},
     'subject': {'categories': ['Chemical', 'Entity'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}},
     {'id': '37476033',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'ncbigene:7364',
                'name': 'UGT2B7'},
     'predicate': {'edge_label': 'affects abundance of',
                   'negated': None,
                   'relation': 'desreases expression or production of'},
     'subject': {'categories': ['Chemical', 'Entity'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}}]



```python
for statement in statements[:5]:
    print('***********************')
    print(statement.subject.name, statement.predicate.relation, statement.object.name)
    print('***********************')
    statement_id = statement.id
    details = gnbr_statements.get_statement_details(statement_id)
    for sentence in details.evidence[:1]:
        pprint(sentence)
    print('\n')
```

    ***********************
    codeine affects expression or production of CYP2D6
    ***********************
    {'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '22092298',
     'name': 'Methadone inhibits CYP2D6 and UGT2B7/2B4 in vivo : a study using '
             'codeine in methadone - and buprenorphine-maintained subjects .',
     'uri': 'pmid:22092298'}
    
    
    ***********************
    codeine inhibits hyodeoxycholic_acid
    ***********************
    {'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '12920168',
     'name': 'Codeine is not a useful UGT2B7 probe substrate because of '
             'significant glucuronidation by UGT2B4 .',
     'uri': 'pmid:12920168'}
    
    
    ***********************
    codeine inhibits CYP3A4
    ***********************
    {'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '8818573',
     'name': 'Coadministration of codeine with selective inhibitors of CYP3A4 may '
             'result in increased morphine production and enhanced pharmacodynamic '
             'effects due to shunting down the CYP2D6 pathway .',
     'uri': 'pmid:8818573'}
    
    
    ***********************
    codeine affects expression or production of CYP2D
    ***********************
    {'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '17017525',
     'name': 'Genotyping revealed the presence of the frame-shift mutation 138delT '
             'only in those subjects who expressed the brain variant CYP2D7 , '
             'which metabolizes codeine exclusively to morphine unlike hepatic '
             'CYP2D6 that metabolizes codeine to nor codeine and morphine .',
     'uri': 'pmid:17017525'}
    
    
    ***********************
    codeine metabolized by PGD2
    ***********************
    {'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '23320562',
     'name': 'Codeine , but not PAF or histamine , caused a small but '
             'statistically significant release of PGD2 .',
     'uri': 'pmid:23320562'}
    
    


At First glance, these results don't look bad.  Generally the top results from the statements endpoint agree with the genes in the codeine metbolism pathway from SMPDB.  We do get some noise toward the end of the results.  Next order of business here is to come up with a suitable ranking metric.  Jaccard is ok, but doesn't give any credit for ranking correct answers highly.  Maybe Average Precision (AP)?  

## Module 3
TODO


```python

```
