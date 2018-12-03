
# GNBR Reasoner Demo
This notebook shows a brief demonstration of the GNBR Reasoner API.  This notebook is a work in progess and will be updated as development progresses.  


### Table of Contents
1. Version and Documentation Info
2. Installation Instructions
3. Pathfinding Demo
4. Current Limitations
5. Future Work

## 1. Version Info
The current version of the API is implemented using the [NCATS-Reasoner API version 0.8.0 specification](https://github.com/NCATS-Tangerine/NCATS-ReasonerStdAPI/blob/master/API/0.8.0/README.md).  Detailed documentation for the client can be found in the [GNBR Reasoner github repository](https://github.com/NCATS-Infrared/gnbr_resoner_client).

## 2. Installation
The GNBR python library can be installed using the python package manager (pypi). Python 3+ is recommended. These instructions assume you are using a unix shell.  If you are using Windows syntax may differ.  It is highly recommended to install in a virtual environemnt to avoid any package conflicts. 

To set up a virtual environment you must have the `virtualenv` package installed.  Type the following commands into your command console.

#### Set Up Virtual Environment
```bash
virtualenv gnbr-resoner
cd gnbr-reasoner
source bin/activate
```

#### Install Client Library
```bash
pip install --upgrade pip
pip install git+https://github.com/NCATS-Infrared/gnbr-client-python.git
```

#### Update Client Library
If you already have an existing installation, you can update it by typing the following command into your console.  It is highly recommended that you regularly update this library as it will be subject to frequent changes during development. 
```bash
pip install --upgrade git+https://github.com/NCATS-Infrared/gnbr-client-python.git
```

## 3. Pathfinding Demo
The GNBR Reaonser pathfinding service takes in a source concept and target endpoint, and finds a set of parsimonious natural language explanations of how they relate to each other, ordered by epistemplogical strength with references.  In other words literature paths between biomedical concepts annotated with relevant sentences and pubmed ids.  Path length is currently capped at 3 hops.

#### Package Imports
The "swagger_client" import is the only statement that is truly needed for operation.  The others are for debugging and display.  The generic name "swagger_client" may cause conflicts with other Open API clients using the same name.  Future versions will have a unqiue name.


```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
```

#### Set Up Query
The current version of the endpoint takes requires only two peices of information:
1. Source Node (specified by name)
2. Target Node (specified by name)

Currently, it is unclear where this will fit into the specification with respect to answers output by other reasoners, so I am using the "query_terms" fields.


```python
api_instance = swagger_client.QueryApi()
body = swagger_client.Query() # Query | Query information to be submitted
body.terms = swagger_client.QueryTerms(source='malaria', target='ibuprofen')
body.max_results = 100
pprint(body)
```

    {'asynchronous': None,
     'bypass_cache': None,
     'known_query_type_id': None,
     'max_results': 100,
     'message': None,
     'options': None,
     'original_question': None,
     'page_number': None,
     'page_size': None,
     'query_plan': None,
     'query_type_id': None,
     'reasoner_ids': None,
     'restated_question': None,
     'terms': {'anatomical_entity': None,
               'chemical_substance': None,
               'metabolite': None,
               'source': 'malaria',
               'target': 'ibuprofen'}}


#### Query API Endpoint
The example query here generates a lot a of results.  This notebook only shows only one cherry picked example for purposes of readability.


```python
try:
    # Query using a predefined query type
    api_response_json = api_instance.query(body)
    pprint(api_response_json)
except ApiException as e:
    print("Exception when calling QueryApi->query: %s\n" % e)
```

    {'context': None,
     'datetime': None,
     'id': None,
     'known_query_type_id': None,
     'message': None,
     'n_results': 1,
     'original_question_text': None,
     'query_type_id': None,
     'reasoner_id': 'GNBR',
     'response_code': 'OK',
     'restated_question_text': None,
     'result_code': None,
     'result_list': [{'confidence': None,
                      'description': None,
                      'essence': None,
                      'id': None,
                      'reasoner_id': 'GNBR',
                      'result_graph': {'edge_list': [{'attribute_list': [{'name': 'Because '
                                                                                  'some '
                                                                                  'febrile '
                                                                                  'patients '
                                                                                  'are '
                                                                                  'unable '
                                                                                  'to '
                                                                                  'swallow '
                                                                                  'or '
                                                                                  'retain '
                                                                                  'oral '
                                                                                  'antipyretic '
                                                                                  'drugs '
                                                                                  ', '
                                                                                  'we '
                                                                                  'carried '
                                                                                  'out '
                                                                                  'a '
                                                                                  'double-blind '
                                                                                  ', '
                                                                                  'placebo-controlled '
                                                                                  'trial '
                                                                                  'in '
                                                                                  'which '
                                                                                  'intravenous '
                                                                                  'ibuprofen '
                                                                                  '-LRB- '
                                                                                  'IV-ibuprofen '
                                                                                  '-RRB- '
                                                                                  'was '
                                                                                  'given '
                                                                                  'to '
                                                                                  'adults '
                                                                                  'hospitalized '
                                                                                  'with '
                                                                                  'fever '
                                                                                  'associated '
                                                                                  'with '
                                                                                  'acute '
                                                                                  'uncomplicated '
                                                                                  'falciparum '
                                                                                  'malaria '
                                                                                  'treated '
                                                                                  'with '
                                                                                  'oral '
                                                                                  'artesunate '
                                                                                  'plus '
                                                                                  'mefloquine '
                                                                                  '.',
                                                                          'type': 'sentence',
                                                                          'url': 'https://www.ncbi.nlm.nih.gov/pubmed/20595477',
                                                                          'value': '110630'},
                                                                         {'name': 'Ibuprofen '
                                                                                  'does '
                                                                                  'not '
                                                                                  'affect '
                                                                                  'levels '
                                                                                  'of '
                                                                                  'tumor_necrosis_factor_alpha '
                                                                                  'and '
                                                                                  'soluble '
                                                                                  'tumor_necrosis_factor_receptor_types_I_and_II '
                                                                                  'in '
                                                                                  'Gabonese '
                                                                                  'children '
                                                                                  'with '
                                                                                  'uncomplicated '
                                                                                  'Plasmodium_falciparum '
                                                                                  'malaria '
                                                                                  '.',
                                                                          'type': 'sentence',
                                                                          'url': 'https://www.ncbi.nlm.nih.gov/pubmed/17964975',
                                                                          'value': '647'},
                                                                         {'name': 'We '
                                                                                  'assessed '
                                                                                  'the '
                                                                                  'ability '
                                                                                  'of '
                                                                                  'ibuprofen '
                                                                                  'to '
                                                                                  'modulate '
                                                                                  'tumor_necrosis_factor_alpha '
                                                                                  '-LRB- '
                                                                                  'TNF-alpha '
                                                                                  '-RRB- '
                                                                                  ', '
                                                                                  'soluble '
                                                                                  'tumor '
                                                                                  'necrosis '
                                                                                  'factor '
                                                                                  'receptor '
                                                                                  'type '
                                                                                  'I '
                                                                                  '-LRB- '
                                                                                  'sTNFR-I '
                                                                                  '-RRB- '
                                                                                  ', '
                                                                                  'and '
                                                                                  'soluble '
                                                                                  'tumor_necrosis_factor_receptor_type_II '
                                                                                  '-LRB- '
                                                                                  'sTNFR-II '
                                                                                  '-RRB- '
                                                                                  'responses '
                                                                                  'during '
                                                                                  'the '
                                                                                  'treatment '
                                                                                  'of '
                                                                                  'fever '
                                                                                  'in '
                                                                                  'uncomplicated '
                                                                                  'Plasmodium_falciparum '
                                                                                  'malaria '
                                                                                  ', '
                                                                                  'in '
                                                                                  'a '
                                                                                  'placebo-controlled '
                                                                                  ', '
                                                                                  'randomized '
                                                                                  ', '
                                                                                  'double-blind '
                                                                                  'study '
                                                                                  'of '
                                                                                  '50 '
                                                                                  'pediatric '
                                                                                  'patients '
                                                                                  'in '
                                                                                  'Lambar '
                                                                                  'n '
                                                                                  ', '
                                                                                  'Gabon '
                                                                                  '.',
                                                                          'type': 'sentence',
                                                                          'url': 'https://www.ncbi.nlm.nih.gov/pubmed/17964975',
                                                                          'value': '7'},
                                                                         {'name': 'Intravenous '
                                                                                  'ibuprofen '
                                                                                  '-LRB- '
                                                                                  'IV-ibuprofen '
                                                                                  '-RRB- '
                                                                                  'controls '
                                                                                  'fever '
                                                                                  'effectively '
                                                                                  'in '
                                                                                  'adults '
                                                                                  'with '
                                                                                  'acute '
                                                                                  'uncomplicated '
                                                                                  'Plasmodium_falciparum '
                                                                                  'malaria '
                                                                                  'but '
                                                                                  'prolongs '
                                                                                  'parasitemia '
                                                                                  '.',
                                                                          'type': 'sentence',
                                                                          'url': 'https://www.ncbi.nlm.nih.gov/pubmed/20595477',
                                                                          'value': '0'}],
                                                      'confidence': 647.0,
                                                      'evidence_type': None,
                                                      'is_defined_by': 'Infrared',
                                                      'negated': None,
                                                      'provided_by': 'GNBR',
                                                      'publications': None,
                                                      'qualifiers': None,
                                                      'relation': 'associated with '
                                                                  'treatment or '
                                                                  'therapy for',
                                                      'source_id': 'MESH:D007052',
                                                      'target_id': 'MESH:D008288',
                                                      'type': 'treats'}],
                                       'node_list': [{'description': None,
                                                      'id': '165149',
                                                      'name': 'ibuprofen',
                                                      'node_attributes': None,
                                                      'symbol': None,
                                                      'type': None,
                                                      'uri': 'MESH:D007052'},
                                                     {'description': None,
                                                      'id': '249150',
                                                      'name': 'malaria',
                                                      'node_attributes': None,
                                                      'symbol': None,
                                                      'type': None,
                                                      'uri': 'MESH:D008288'}]},
                      'result_group': None,
                      'result_group_similarity_score': None,
                      'result_type': None,
                      'row_data': None,
                      'score': 3.200850498091077,
                      'score_direction': 'higher_is_better',
                      'score_name': None,
                      'text': None}],
     'schema_version': '0.8.0',
     'table_column_names': None,
     'terms': {'source': 'malaria', 'target': 'ibuprofen'},
     'tool_version': None,
     'type': None}


## 4. Limitations
#### Lookup Performance
Name lookup is extremely slow - on the order of 10s of seconds.  Pathway and sentence lookups are not blazing fast either.  This can cause the client to timeout. How are other teams caching results?
#### Missing Concepts
A number of concepts present in the Orange and Gamma reasoner outputs are not present in GNBR. In particular, concepts and associations from recent publications (i.e. 2018) are missing. This is a pretty hard limitation of its utiliy because chains of reasoning that rely on these new results are often more interesting to SMEs.
#### Edge Weights and Theme Scores
Confidence scores for statement edges and sentence themes have two related problems they are not interpetable and can result in erroneous edge labeling.  Without going into too much detail the underlying causes are (1) how statement scores are computed, and lack of score normalization.

## 5. Upgrades
In the future the GNBR Reasoner "kanban board" will reside in the issues section of the server repository.
### In Progress
#### Neo4J Data Model
I have revised the underlying neo4j data model to support faster lookup by name.  Speedup is roughly 10,000x.  
#### GNBR Update
The old version of GNBR (3.0) was released in Jan 2018 and only included publications through 2017.  The most recent version of GNBR (4.0) was released May 2018, and includes more recent publications.  A new realease is planned for Q1 2019.  I have also fully refactored the neo4j build pipeline into a single executable module that can support more frequent updating.
#### Statement Scores
Before we computed the statement score for a pair of entities as the aggregate sum of the theme scores taken over the sentences relating them to each other. Now we use the arithmatic mean as our aggregation function.  This has the effect of downweighting scores for entities that are frequently mentioned together.
#### Score Normalization
Before scores were innormalized. We now normalize by mapping each theme score to its percentile rank.  This makes scores more interpretable and also helps smooth out some of the distributional effects arising from subtle, systematic differences in way closely related themes are expressed in writing.
### Proposed
#### Synonym Service
Takes in the name of a chemical, gene, or disease and returns all synonyms used in the literature.
#### Upgrade to Reasoner API 0.9.0
Coordinate with other Reasoner groups.  When are they plannning to make the change?
#### Knowledge Graph Annotation Service
Takes in a knowledge graph and returns with pubmed sentence annotations for edges.
#### Refine of Pathfinding Endpoint
Support contraints on min path length?  Types of nodes in path?  Path scoring?  Edge score theshold?


```python

```
