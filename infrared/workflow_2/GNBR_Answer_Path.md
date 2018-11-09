
# GNBR Answer Paths
This workbook uses a basic pathfinding algorithm to evaulate the goodness of similarity computation outputs from the Orange and Gamma team reasoners.  Given a query node and another "similar", it tries to find a set of parsimonious explanations for why they are similar or related.  These explanations come in the form of sentences that link entities together across documents and are meant to help SMEs interpret and evaluate the output of workflow modules.

Basic instructions and example of how this routine works can be found in this [markdown document](https://github.com/ncats/translator-workflows/blob/master/infrared/GNBR%20Path%20Lookup.md).  Keep in mind that som parts of this are not available via the live API, so you will need a local copy with bolt access to replicate this.  If there is demand, I can build this into a rest endpoint.

### GNBR Client Stuff
This first part looks up the uris for EEPD1, FANCC, FANCG.  Notice that multiple hits get returned for FANCC and FANCG.  Some of these are orthologs.  Some of them I haven't checked out.  This example will use the curies that have the most mentions.


```python
from __future__ import print_function
import swagger_client
from pprint import pprint

gnbr_concepts = swagger_client.ConceptsApi()
keywords = ['EEPD1','FANCC', 'FANCG']
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
     'uri': 'ncbigene:80820'},
     {'categories': ['Entity', 'Gene'],
     'description': None,
     'details': [{'tag': 'mentions', 'value': '336'}],
     'exact_matches': None,
     'id': 'ncbigene:2176',
     'name': 'FAC',
     'symbol': None,
     'synonyms': ['FANCC',
                  'FAC',
                  'FACC',
                  'FA-C',
                  'Fancc',
                  'Fac',
                  'fac',
                  'FA complementation group C',
                  'hFANCC',
                  'FancC',
                  'FA3',
                  'Fanconi anemia group C',
                  'Fanconi anemia group C protein',
                  'Fanconi anemia complementation group C'],
     'uri': 'ncbigene:2176'},
     {'categories': ['Entity', 'Gene'],
     'description': None,
     'details': [{'tag': 'mentions', 'value': '54'}],
     'exact_matches': None,
     'id': 'ncbigene:14088',
     'name': 'Facc',
     'symbol': None,
     'synonyms': ['Fancc', 'FANCC', 'FancC', 'fancc', 'FACC', 'Facc'],
     'uri': 'ncbigene:14088'},
     {'categories': ['Entity', 'Gene'],
     'description': None,
     'details': [{'tag': 'mentions', 'value': '3'}],
     'exact_matches': None,
     'id': 'ncbigene:427468',
     'name': 'FANCC',
     'symbol': None,
     'synonyms': ['FANCC'],
     'uri': 'ncbigene:427468'},
     {'categories': ['Entity', 'Gene'],
     'description': None,
     'details': [{'tag': 'mentions', 'value': '108'}],
     'exact_matches': None,
     'id': 'ncbigene:2189',
     'name': 'FANCG',
     'symbol': None,
     'synonyms': ['FANCG',
                  'FANC G',
                  'XRCC9',
                  'FancG',
                  'fancg',
                  'FA-G',
                  'Fancg',
                  'Fanconi anemia complementation group G'],
     'uri': 'ncbigene:2189'},
     {'categories': ['Entity', 'Gene'],
     'description': None,
     'details': [{'tag': 'mentions', 'value': '1'}],
     'exact_matches': None,
     'id': 'ncbigene:378893',
     'name': 'FANCG',
     'symbol': None,
     'synonyms': ['FANCG'],
     'uri': 'ncbigene:378893'}]


### Bolt Interface Stuff
This next part is not published on the API yet, so it is currently implemented locally using the bolt interface.  If it proves popular enough, I will implement it as an endpoint on a "reasoning" API, distinct from the knowledge beacon, that nevertheless runs over thre same neo4j instance.

#### Function Declarations


```python
from neo4j.v1 import GraphDatabase
import math

uri="bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=('', ''))

def get_paths(tx, source, sink):
    query = """
    MATCH (source :Entity {uri: $source}), (sink :Entity {uri : $sink}),
    p=allshortestpaths( (source)-[:STATEMENT *0..3]-(sink) )
    RETURN nodes(p) as n, relationships(p) as r
    """
    result = []
    for record in tx.run(query, source=source, sink=sink):
        result.append(record['r'])
    return result

def total_weight(path):
    total = 0
    for edge in path:
        weight = sum(edge.values())
        total = total + math.log(weight, 10)
    return total
```

#### EEPD1 and FANCC


```python
gnbr_statements = swagger_client.StatementsApi()
with driver.session() as neo4j:
    paths = neo4j.read_transaction(get_paths, source="ncbigene:80820", sink="ncbigene:2176")
    top_paths = sorted(paths, key=total_weight, reverse=True)[0:1]
    for top_path in top_paths:
        explanation = []
        print('                  Explanation                            ')
        print('---------------------------------------------------------')
        for relationship in top_path:
            uris = [i['uri'] for i in relationship.nodes]
            stmt = gnbr_statements.get_statements(s=uris[:1])
            statement = [i for i in stmt if i.subject.id == uris[1] or i.object.id == uris[1]]
            statement = statement[0]
            print('*********************************')
            print(statement.subject.name, statement.predicate.relation, statement.object.name)
            print('*********************************')
            sentences = gnbr_statements.get_statement_details(statement.id)
            pprint(sentences.evidence[:1])
        print('---------------------------------------------------------')
```

                      Explanation                            
    ---------------------------------------------------------
    *********************************
    ATR observed together with EEPD1
    *********************************
    [{'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '26684013',
     'name': 'EEPD1 is also required for proper ATR and CHK1 phosphorylation , and '
             'formation of gamma-H2AX , RAD51 and phospho-RPA32 foci .',
     'uri': 'pmid:26684013'}]
    *********************************
    ATM same protein or complex ATR
    *********************************
    [{'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '16909103',
     'name': 'Inhibition of ataxia_telangiectasia_mutated -LRB- ATM -RRB- protein '
             'and DNA-PK could not suppress the induction of bystander gammaH2AX '
             'foci whereas the mutation of ATM - _ and_rad3-related -LRB- ATR '
             '-RRB- abrogated bystander foci induction .',
     'uri': 'pmid:16909103'}]
    *********************************
    FAC observed together with ATM
    *********************************
    [{'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '26691941',
     'name': 'RESULTS : There were several deleterious -LRB- frame-shift/nonsense '
             '-RRB- mutations detected in ATM , BAP1 , FANCC , FANCI , PMS2 , SBDS '
             ', ERCC2 , RECQL4 genes .',
     'uri': 'pmid:26691941'}]
    ---------------------------------------------------------


#### EEPD1 and FANCG


```python
explanations = []
gnbr_statements = swagger_client.StatementsApi()
with driver.session() as neo4j:
    paths = neo4j.read_transaction(get_paths, source="ncbigene:80820", sink="ncbigene:2189")
    top_paths = sorted(paths, key=total_weight, reverse=True)[4:5]
    for top_path in top_paths:
        explanation = []
        print('                  Explanation                            ')
        print('---------------------------------------------------------')
        for relationship in top_path:
            max_key = sorted(relationship, key=lambda x: (relationship[x], x), reverse=True)[0]
            uris = [i['uri'] for i in relationship.nodes]
            stmt = gnbr_statements.get_statements(s=[uris[0]])
            statement = [i for i in stmt if i.subject.id == uris[1] or i.object.id == uris[1]]
            statement = statement[0]
            print('*********************************')
            print(statement.subject.name, statement.predicate.relation, statement.object.name)
            print('*********************************')
            sentences = gnbr_statements.get_statement_details(statement.id)
            pprint(sentences.evidence[:3])
        print('---------------------------------------------------------')
```

                      Explanation                            
    ---------------------------------------------------------
    *********************************
    ATR observed together with EEPD1
    *********************************
    [{'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '26684013',
     'name': 'EEPD1 is also required for proper ATR and CHK1 phosphorylation , and '
             'formation of gamma-H2AX , RAD51 and phospho-RPA32 foci .',
     'uri': 'pmid:26684013'}]
    *********************************
    FANCA observed together with ATR
    *********************************
    [{'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '19109555',
     'name': 'Serine 1449 is in a consensus ATM/ATR site , phosphorylation in vivo '
             'is dependent on ATR , and ATR phosphorylated FANCA on serine 1449 in '
             'vitro .',
     'uri': 'pmid:19109555'}]
    *********************************
    FANCG increases expression or production of FANCA
    *********************************
    [{'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '11181053',
     'name': 'FANCA was induced concurrently with FANCG , and the FANCA/FANCG '
             'complex was increased in the nucleus following TNF-alpha treatment .',
     'uri': 'pmid:11181053'},
     {'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '11093276',
     'name': 'A putative missense mutation , L71P , in a possible leucine zipper '
             'motif may affect FANCG binding of FANCA and seems to be associated '
             'with a milder clinical phenotype .',
     'uri': 'pmid:11093276'},
     {'date': None,
     'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
     'id': '27041517',
     'name': 'FANCA had the highest mutation frequency rate -LRB- 83 % -RRB- '
             'followed by FANCG -LRB- 10 % -RRB- , FANCD2 -LRB- 3 % -RRB- and '
             'FANCL -LRB- 3 % -RRB- .',
     'uri': 'pmid:27041517'}]
    ---------------------------------------------------------



```python

```
