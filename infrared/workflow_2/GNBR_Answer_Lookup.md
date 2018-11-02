
# GNBR Worflow Answer Lookup
This workbook shows how to use GNBR to lookup answers output by reasoners.  There are two basic functions being shown in this workbook that may be of use to SMEs evaulating the quality of answers returned by resoners.  

1. Synonym retrival. Curies are not human readable and symbols or names of genes, diseeases, and chemicals can also be difficult to interpret because SMEs might not recognize a particular synonym. 
2. Sentence annotation.  One way of defining a concept is by its attributes.  Another way, which can be equally or more informative is by its relationships to other concepts.  With sentence annotation we are find all related concepts, and then return sentences descibing those relationships.

## Provenance of Data/Exmples
The genes used here are from the output of the Gamma and Orange Team reasoners for the Fanoconi Workflow (#2); and can be found [in this linked spreadsheet](https://docs.google.com/spreadsheets/d/19xKibjf2wOuomlWlxnT94uwcQ-AhmzkWgclfCmYVeVA/edit#gid=1952644138). FAAP24 and EEPD1 were chosen as examples because they were consensus outputs with known (FAAP24) and unknown (EPPD1) associations with Fanconi genes. We encourage people to try out the other genes on the list.  Note the ASTE1 and INIP have been tested and are not in the current version of GNBR.

#### Package Imports
Here we are importing the GNBR client library as well as some helper functions.  Intallation instructions and documentation for the GNBR client library can be found in the [GitHub repository](https://github.com/NCATS-Infrared/gnbr-client-python).


```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
```

### EEPD1
EEPD1 was consensus output of the resoners and to the best of our knowledge has no currently recognized to be association with any of the Fanconi genes.
##### Concept Lookup


```python
gnbr_concepts = swagger_client.ConceptsApi()
keywords = ['EEPD1']
concepts = gnbr_concepts.get_concepts(keywords=keywords)
concept_details = [gnbr_concepts.get_concept_details(concept.id) for concept in concepts]
pprint(concept_details)
```

    [{'categories': ['Entity', 'Gene'],
     'description': None,
     'details': [{'tag': 'mentions', 'value': '1'}],
     'exact_matches': None,
     'id': 'ncbigene:80820',
     'name': 'EEPD1',
     'symbol': None,
     'synonyms': ['EEPD1'],
     'uri': 'ncbigene:80820'}]


##### Statement Lookup 


```python
gnbr_statements = swagger_client.StatementsApi()
s = [concept.id for concept in concepts]
statements = gnbr_statements.get_statements(s=s)
for statement in statements:
    print('***********************')
    print(statement.subject.name, statement.predicate.relation, statement.object.name)
    print('***********************')
    statement_id = statement.id
    details = gnbr_statements.get_statement_details(statement_id)
    for sentence in details.evidence[:3]:
        pprint(sentence)
    print('\n')
```

    ***********************
    ATR observed together with EEPD1
    ***********************
    {'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '26684013',
     'name': 'EEPD1 is also required for proper ATR and CHK1 phosphorylation , and '
             'formation of gamma-H2AX , RAD51 and phospho-RPA32 foci .',
     'uri': 'pmid:26684013'}
    
    
    ***********************
    EEPD1 binds ATR
    ***********************
    {'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '26684013',
     'name': 'EEPD1 is also required for proper ATR and CHK1 phosphorylation , and '
             'formation of gamma-H2AX , RAD51 and phospho-RPA32 foci .',
     'uri': 'pmid:26684013'}
    
    


### FAAP24
FAAP24 was also a consensus output of the reasoners and is known to be associated with one or more of the Fanconi genes.  Thus it is a "ground truth" answer.
#### Concept Lookup


```python
gnbr_concepts = swagger_client.ConceptsApi()
keywords = ['FAAP24']
concepts = gnbr_concepts.get_concepts(keywords=keywords)
concept_details = [gnbr_concepts.get_concept_details(concept.id) for concept in concepts]
pprint(concept_details)
```

    [{'categories': ['Entity', 'Gene'],
     'description': None,
     'details': [{'tag': 'mentions', 'value': '4'}],
     'exact_matches': None,
     'id': 'ncbigene:91442',
     'name': 'FAAP24',
     'symbol': None,
     'synonyms': ['FAAP24'],
     'uri': 'ncbigene:91442'}]


#### Statement Lookup


```python
gnbr_statements = swagger_client.StatementsApi()
s = [concept.id for concept in concepts]
statements = gnbr_statements.get_statements(s=s)
for statement in statements:
    print('***********************')
    print(statement.subject.name, statement.predicate.relation, statement.object.name)
    print('***********************')
    statement_id = statement.id
    details = gnbr_statements.get_statement_details(statement_id)
    for sentence in details.evidence[:3]:
        pprint(sentence)
    print('\n')
```

    ***********************
    FAAP24 regulates FANCM
    ***********************
    {'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '17317622',
     'name': 'FAAP24 , a new XPF endonuclease family member identified by in a '
             'recent issue of Molecular Cell , heterodimerizes with FANCM , binds '
             'unwound DNA , and reveals how the Fanconi_anemia core complex '
             'concentrates DNA repair proteins at stalled replication forks .',
     'uri': 'pmid:17317622'}
    {'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '17289582',
     'name': 'Here , we describe the identification of FAAP24 , a protein that '
             'targets FANCM to structures that mimic intermediates formed during '
             'the replication/repair of damaged DNA .',
     'uri': 'pmid:17289582'}
    {'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '18174376',
     'name': 'Moreover , depletion of the FANCM binding partner , FAAP24 , '
             'disrupted the chromatin association of FANCM and destabilized FANCM '
             ', leading to defective recruitment of the FA core complex to '
             'chromatin .',
     'uri': 'pmid:18174376'}
    
    
    ***********************
    FANCM regulates FAAP24
    ***********************
    {'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '17317622',
     'name': 'FAAP24 , a new XPF endonuclease family member identified by in a '
             'recent issue of Molecular Cell , heterodimerizes with FANCM , binds '
             'unwound DNA , and reveals how the Fanconi_anemia core complex '
             'concentrates DNA repair proteins at stalled replication forks .',
     'uri': 'pmid:17317622'}
    {'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '17289582',
     'name': 'Here , we describe the identification of FAAP24 , a protein that '
             'targets FANCM to structures that mimic intermediates formed during '
             'the replication/repair of damaged DNA .',
     'uri': 'pmid:17289582'}
    {'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '18174376',
     'name': 'Moreover , depletion of the FANCM binding partner , FAAP24 , '
             'disrupted the chromatin association of FANCM and destabilized FANCM '
             ', leading to defective recruitment of the FA core complex to '
             'chromatin .',
     'uri': 'pmid:18174376'}
    
    
    ***********************
    FAAP24 improper regulation associated with XPF-deficient
    ***********************
    {'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '17317622',
     'name': 'FAAP24 , a new XPF endonuclease family member identified by in a '
             'recent issue of Molecular Cell , heterodimerizes with FANCM , binds '
             'unwound DNA , and reveals how the Fanconi_anemia core complex '
             'concentrates DNA repair proteins at stalled replication forks .',
     'uri': 'pmid:17317622'}
    {'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '17289582',
     'name': 'FAAP24 shares homology with the XPF family of flap/fork '
             'endonucleases , associates with the C-terminal region of FANCM , and '
             'is a component of the FA core complex .',
     'uri': 'pmid:17289582'}
    
    


## Conclusion
This has been a very basic demo of how the GNBR API can be used to investigate the plausibility of answers return ed by the reasoner.  The primary contributions are (a) looking up synonyms, and (b) placing genes in the context of their relationships to other entities.  There are a few warts and some upgrades are already in process.  Planned upgrades include:
1. Putting everything into a single function or cell to make it easy for SMEs to run code
2. Adding "most informative sentence(s)" to concept details.
3. Deduplication of gene-gene associations.
4. Optimize name lookup to run faster.


```python

```
