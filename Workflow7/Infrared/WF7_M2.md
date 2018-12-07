
# Workflow 7 - Module 2 (Ordered Pathway)
This notebook will focus on module 2 of workflow 7.  The objective is to take unordered lists of genes and metabolites and structure them into a pathway.  The first prototype use case for this workflow will focus on Codeine.

## Step 1. Query SMPDB API
For this one we're going to use the fully automated workflow.  


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

def all_neighbors(query):
    b = build(KnowledgeSource.SMPDB)
    concepts = get_concepts(query)
    query_ids = [i.id for i in concepts]
    related_concepts = b.get_statements(s=query_ids)
    related = [i.object.name for i in related_concepts]
    return concepts + get_concepts(query=related)

def all_associations(stuff):
    output = {}
    b = build(KnowledgeSource.SMPDB)
    ids = [i.id for i in stuff]
    for i in b.get_predicates():
        predicate = i.relation
        output[predicate] = b.get_statements(s=ids, relation=predicate, t=ids)
    return output
```

### Module Input
First we query SMPDB for unorganized lists of chemicals and genes in a pathway.


```python
related = all_neighbors(['Codeine'])
```


```python
genes = [i.name for i in related if 'protein' in i.categories]
genes = list(set(genes))
pprint(genes)
```

    ['Cytochrome P450 2D6',
     'UDP-glucuronosyltransferase 2B7',
     'Cytochrome P450 3A4']



```python
chems = [i.name for i in related if 'chemical substance' in i.categories]
mets = [i.name for i in related if 'metabolite' in i.categories]
metabolites = list(set(mets + chems))
pprint(metabolites)
```

    ['Uridine diphosphate glucuronic acid',
     'Norcodeine',
     "Uridine 5'-diphosphate",
     'Codeine-6-glucuronide',
     'Morphine',
     'Formaldehyde',
     'Codeine']


### Module Output
Then we query SMPDB for the rest of the pathway associations. 


```python
associations = all_associations(related)
```


```python
substrate_product = associations['used_to_produce']
pprint(substrate_product)
```

    [{'id': 'CHEBI:16714|related_to|used_to_produce|CHEBI:16842',
     'object': {'categories': ['metabolite'],
                'id': 'CHEBI:16842',
                'name': 'Formaldehyde'},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'used_to_produce'},
     'subject': {'categories': ['metabolite'],
                 'id': 'CHEBI:16714',
                 'name': 'Codeine'}},
     {'id': 'CHEBI:17200|related_to|used_to_produce|CHEBI:17659',
     'object': {'categories': ['metabolite'],
                'id': 'CHEBI:17659',
                'name': "Uridine 5'-diphosphate"},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'used_to_produce'},
     'subject': {'categories': ['metabolite'],
                 'id': 'CHEBI:17200',
                 'name': 'Uridine diphosphate glucuronic acid'}},
     {'id': 'CHEBI:16714|related_to|used_to_produce|CHEBI:17659',
     'object': {'categories': ['metabolite'],
                'id': 'CHEBI:17659',
                'name': "Uridine 5'-diphosphate"},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'used_to_produce'},
     'subject': {'categories': ['metabolite'],
                 'id': 'CHEBI:16714',
                 'name': 'Codeine'}},
     {'id': 'CHEBI:17303|related_to|used_to_produce|CHEBI:17659',
     'object': {'categories': ['metabolite'],
                'id': 'CHEBI:17659',
                'name': "Uridine 5'-diphosphate"},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'used_to_produce'},
     'subject': {'categories': ['metabolite'],
                 'id': 'CHEBI:17303',
                 'name': 'Morphine'}},
     {'id': 'CHEBI:16714|related_to|used_to_produce|HMDB:HMDB0060657',
     'object': {'categories': ['chemical substance'],
                'id': 'HMDB:HMDB0060657',
                'name': 'Norcodeine'},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'used_to_produce'},
     'subject': {'categories': ['metabolite'],
                 'id': 'CHEBI:16714',
                 'name': 'Codeine'}},
     {'id': 'CHEBI:17200|related_to|used_to_produce|HMDB:HMDB0060464',
     'object': {'categories': ['chemical substance'],
                'id': 'HMDB:HMDB0060464',
                'name': 'Codeine-6-glucuronide'},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'used_to_produce'},
     'subject': {'categories': ['metabolite'],
                 'id': 'CHEBI:17200',
                 'name': 'Uridine diphosphate glucuronic acid'}},
     {'id': 'CHEBI:16714|related_to|used_to_produce|HMDB:HMDB0060464',
     'object': {'categories': ['chemical substance'],
                'id': 'HMDB:HMDB0060464',
                'name': 'Codeine-6-glucuronide'},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'used_to_produce'},
     'subject': {'categories': ['metabolite'],
                 'id': 'CHEBI:16714',
                 'name': 'Codeine'}},
     {'id': 'CHEBI:16714|related_to|used_to_produce|CHEBI:17303',
     'object': {'categories': ['metabolite'],
                'id': 'CHEBI:17303',
                'name': 'Morphine'},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'used_to_produce'},
     'subject': {'categories': ['metabolite'],
                 'id': 'CHEBI:16714',
                 'name': 'Codeine'}}]



```python
substrate_gene = associations['consumption_controlled_by']
pprint(substrate_gene)
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
     {'id': 'CHEBI:17200|related_to|consumption_controlled_by|UNIPROT:P16662',
     'object': {'categories': ['protein'],
                'id': 'UNIPROT:P16662',
                'name': 'UDP-glucuronosyltransferase 2B7'},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'consumption_controlled_by'},
     'subject': {'categories': ['metabolite'],
                 'id': 'CHEBI:17200',
                 'name': 'Uridine diphosphate glucuronic acid'}},
     {'id': 'CHEBI:16714|related_to|consumption_controlled_by|UNIPROT:P16662',
     'object': {'categories': ['protein'],
                'id': 'UNIPROT:P16662',
                'name': 'UDP-glucuronosyltransferase 2B7'},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'consumption_controlled_by'},
     'subject': {'categories': ['metabolite'],
                 'id': 'CHEBI:16714',
                 'name': 'Codeine'}},
     {'id': 'CHEBI:17303|related_to|consumption_controlled_by|UNIPROT:P16662',
     'object': {'categories': ['protein'],
                'id': 'UNIPROT:P16662',
                'name': 'UDP-glucuronosyltransferase 2B7'},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'consumption_controlled_by'},
     'subject': {'categories': ['metabolite'],
                 'id': 'CHEBI:17303',
                 'name': 'Morphine'}}]



```python
gene_product = associations['controls_production_of']
pprint(gene_product)
```

    [{'id': 'UNIPROT:P08684|related_to|controls_production_of|CHEBI:16842',
     'object': {'categories': ['metabolite'],
                'id': 'CHEBI:16842',
                'name': 'Formaldehyde'},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'controls_production_of'},
     'subject': {'categories': ['protein'],
                 'id': 'UNIPROT:P08684',
                 'name': 'Cytochrome P450 3A4'}},
     {'id': 'UNIPROT:P10635|related_to|controls_production_of|CHEBI:16842',
     'object': {'categories': ['metabolite'],
                'id': 'CHEBI:16842',
                'name': 'Formaldehyde'},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'controls_production_of'},
     'subject': {'categories': ['protein'],
                 'id': 'UNIPROT:P10635',
                 'name': 'Cytochrome P450 2D6'}},
     {'id': 'UNIPROT:P16662|related_to|controls_production_of|CHEBI:17659',
     'object': {'categories': ['metabolite'],
                'id': 'CHEBI:17659',
                'name': "Uridine 5'-diphosphate"},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'controls_production_of'},
     'subject': {'categories': ['protein'],
                 'id': 'UNIPROT:P16662',
                 'name': 'UDP-glucuronosyltransferase 2B7'}},
     {'id': 'UNIPROT:P08684|related_to|controls_production_of|HMDB:HMDB0060657',
     'object': {'categories': ['chemical substance'],
                'id': 'HMDB:HMDB0060657',
                'name': 'Norcodeine'},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'controls_production_of'},
     'subject': {'categories': ['protein'],
                 'id': 'UNIPROT:P08684',
                 'name': 'Cytochrome P450 3A4'}},
     {'id': 'UNIPROT:P16662|related_to|controls_production_of|HMDB:HMDB0060464',
     'object': {'categories': ['chemical substance'],
                'id': 'HMDB:HMDB0060464',
                'name': 'Codeine-6-glucuronide'},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'controls_production_of'},
     'subject': {'categories': ['protein'],
                 'id': 'UNIPROT:P16662',
                 'name': 'UDP-glucuronosyltransferase 2B7'}},
     {'id': 'UNIPROT:P10635|related_to|controls_production_of|CHEBI:17303',
     'object': {'categories': ['metabolite'],
                'id': 'CHEBI:17303',
                'name': 'Morphine'},
     'predicate': {'edge_label': 'related_to',
                   'negated': False,
                   'relation': 'controls_production_of'},
     'subject': {'categories': ['protein'],
                 'id': 'UNIPROT:P10635',
                 'name': 'Cytochrome P450 2D6'}}]


## GNBR Queries
Neither of the GNBR APIs currently has endpoints that provide the functionality we need.  So for now we will use custom queries via the bolt interface with the intention of promoting them to live API if they work.


```python
import math
import gnbr_beacon
from neo4j import GraphDatabase

gnbr_concepts = gnbr_beacon.ConceptsApi()
gnbr_statements = gnbr_beacon.StatementsApi()

driver = GraphDatabase.driver("bolt://localhost:7687", auth=('',''))

def pk_motif(tx, source, target):
    query = """
    MATCH p=(:Chemical {uri: $source})-[s:STATEMENT]->(:Gene)<-[t:STATEMENT]-(:Chemical {uri: $target})
    RETURN nodes(p) as n, relationships(p) as r
    """
    result = []
    for record in tx.run(query, source=source, target=target):
        result.append(record)
    return result

def geometric_mean(path):
    total = []
    p = path['r']
    for edge in p:
        weight = max(edge.values())
        total.append(math.log(weight))
        geo_mean = math.exp(sum(total)/len(total))
    return geo_mean
```

### Harmonize Concepts
First we need to map concepts from SMPDB into GNBR.  We might imagine doing the reverse mapping, but for now we are keeping it as simple as possible.  We map concepts using simple keyword lookup.


```python
mapped_chems = gnbr_concepts.get_concepts(keywords=[i.lower() for i in metabolites])
pprint(mapped_chems)
```

    [{'categories': ['Entity', 'Chemical'],
     'description': None,
     'id': 'MESH:D014535',
     'name': 'UDPGA'},
     {'categories': ['Entity', 'Chemical'],
     'description': None,
     'id': 'MESH:C010414',
     'name': 'norcodeine'},
     {'categories': ['Entity', 'Chemical'],
     'description': None,
     'id': 'MESH:D009020',
     'name': 'morphine'},
     {'categories': ['Entity', 'Chemical'],
     'description': None,
     'id': 'MESH:D005557',
     'name': 'formalin'},
     {'categories': ['Entity', 'Chemical'],
     'description': None,
     'id': 'MESH:D003061',
     'name': 'codeine'}]



```python
mapped_genes = gnbr_concepts.get_concepts(keywords=[i for i in genes])
pprint(mapped_genes)
```

    [{'categories': ['Entity', 'Gene'],
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
     'name': 'UGT2B7'},
     {'categories': ['Entity', 'Gene'],
     'description': None,
     'id': 'NCBIGENE:1576',
     'name': 'CYP3A4'}]



```python
import itertools
chem_ids = [i.id for i in mapped_chems]
gene_ids = [i.id for i in mapped_genes]
all_motifs = []
with driver.session() as neo4j:
    for source, target in itertools.combinations(chem_ids, 2):
        motifs = neo4j.read_transaction(pk_motif, source=source, target=target)
        all_motifs.extend(motifs)
```


```python
all_motifs = sorted(all_motifs, key=geometric_mean, reverse=True)
for motif in all_motifs:
    nodes = motif['n']
    node_ids = [n['uri'] for n in nodes]
    if 'MESH:D005557' in node_ids:
        continue
    if node_ids[1] not in gene_ids:
        continue
    pprint([i['name'] for i in nodes])
```

    ['UDPGA', 'UGT2B7', 'morphine']
    ['UDPGA', 'UGT2B7', 'codeine']
    ['morphine', 'UGT2B7', 'codeine']
    ['norcodeine', 'CYP3A4', 'codeine']
    ['morphine', 'CYP2D6', 'codeine']
    ['morphine', 'CYP3A4', 'codeine']
    ['norcodeine', 'CYP3A4', 'morphine']


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

### Further Investigation

#### Right Answers

#### Wrong Answers

## Conclusion


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

```
