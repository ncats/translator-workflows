
# Workflow Module 1A - Disease Associated Gene Lookup

## Stefano Rensi, Stanford University

This is a query workbook for module 1A workflow reasoning.  This one is for a "high specificity" look up, which returns  genes that are members of mechanistic cliques.  Will upgrade to KB_API Client if anyone thinks this type of thing is useful.  Using Mesh ID's for now because curie lookup currently outsourced to Biolink.

**Lookups for workflows 1 and 2 are in CSV files**
1. diabetes.csv
2. fanconi.csv

**Considerations**
1. Results are ordered by strength of gene-disease relationship
2. Relationships (edge weights) are unthresholded (low edge specificity)

Basically this means that there are some cliques with weak links in there that can't really be sorted out with the current implementation.  Can fix by returning all three edge weights from clique, but might be doing too much.


### Imports


```python
import math
from neo4j.v1 import GraphDatabase

# Fire up the 'ol bolt dirver
url="bolt://localhost:7687"
driver = GraphDatabase.driver(url, auth=('', ''))
```

### Functions
**get_name()** takes a curie and returns the most frequently used synonym in our literature base. 


```python
def get_name(tx, uri):
    query = """
    MATCH (e:Entity {uri: $uri})-[m:IN_SENTENCE]-(s:Sentence)
    WITH DISTINCT m.raw_string as name, count(m.raw_string) as vals
    RETURN name order by vals desc limit 1 
    """
    for record in tx.run(query, uri=uri):
        output = record['name']
    return output

with driver.session() as neo4j:
    name = neo4j.read_transaction(get_name, uri='ncbigene:9370')
    print('Top Mention:', name)
```

    Top Mention: adiponectin


**get_clique()** takes in a disease curie and returns a list of genes that are members of mechanistic cliques (chemical, gene, disease)


```python
def get_clique(tx, uri):
    query = """
    MATCH (d:Disease {uri: $uri})-[s:STATEMENT]-(g:Gene),
    (g)-[:STATEMENT]-(c:Chemical),
    (c)-[:STATEMENT]-(d)
    WITH DISTINCT g as gene, reduce(accumulator = 0.0, key IN keys(s) | accumulator + s[key]) as values
    RETURN gene, values order by values desc
    """
    output = []
    for record in tx.run(query, uri=uri):
        gene = record['gene']['uri']
        values = math.log(record['values'])
        output.append((gene, values))
    return output

with driver.session() as neo4j:
    genes = neo4j.read_transaction(get_clique, uri='MESH:D003924')
    print('%i Genes Returned' % len(genes))
    for gene, score in genes[:10]:
        name = neo4j.read_transaction(get_name, uri=gene)
        print(name, gene, math.ceil(score))
```

    563 Genes Returned
    insulin ncbigene:3630 15
    GLP-1 ncbigene:2641 12
    HNF1A ncbigene:6927 12
    PAI-1 ncbigene:5054 12
    TCF7L2 ncbigene:6934 12
    TNF-alpha ncbigene:7124 12
    CRP ncbigene:1401 12
    ET-1 ncbigene:1906 12
    adiponectin ncbigene:9370 12
    glucokinase ncbigene:2645 12


### Basic QC

Compare to query for without clique condition


```python
def get_genes(tx, uri):
    query = """
    MATCH (d:Disease {uri: $uri})-[s:STATEMENT]-(g:Gene)
    WITH DISTINCT g as gene, reduce(accumulator = 0.0, key IN keys(s) | accumulator + s[key]) as values
    RETURN gene, values order by values desc
    """
    output = []
    for record in tx.run(query, uri=uri):
        gene = record['gene']['uri']
        values = math.log(record['values'])
        output.append((gene, values))
    return output

with driver.session() as neo4j:
    genes = neo4j.read_transaction(get_genes, uri='MESH:D003924')
    print('%i Genes Returned' % len(genes))
    for gene, score in genes[:10]:
        name = neo4j.read_transaction(get_name, uri=gene)
        print(name, gene, math.ceil(score))
```

    605 Genes Returned
    insulin ncbigene:3630 15
    GLP-1 ncbigene:2641 12
    HNF1A ncbigene:6927 12
    PAI-1 ncbigene:5054 12
    TCF7L2 ncbigene:6934 12
    TNF-alpha ncbigene:7124 12
    CRP ncbigene:1401 12
    ET-1 ncbigene:1906 12
    adiponectin ncbigene:9370 12
    glucokinase ncbigene:2645 12


### Queries
Now we wrap in a function that spits out a csv, and run it on the mesh ids for type 2 diabetes (NDDM), and fanconi anemia.


```python
import csv

type_ii_diabetes = 'MESH:D003924'
fanconi_anemia = 'MESH:D005199'

def gene_disease_lookup(uri, filename):
    outfile = open(filename, 'w')
    csv_out = csv.writer( outfile )
    csv_out.writerow( ('name', 'uri', 'score') )
    with driver.session() as neo4j:
        genes = neo4j.read_transaction(get_clique, uri=uri)
        for gene, score in genes:
            name = neo4j.read_transaction(get_name, uri=gene)
            csv_out.writerow( (name, gene, math.ceil(score)) )
    outfile.close()
    return

gene_disease_lookup(type_ii_diabetes, 'diabetes.csv')
gene_disease_lookup(fanconi_anemia, 'fanconi.csv')
```

### Conclusion
Well first pass looks meh.  Filtering by clique in most naive manner filters about 40 genes.  Would like to enforce a little more specifity.

So... uhhh... what are we doing about QC on gene lists?  If you want to chat about that, or if you have any other comments, suggestions, or anything just shout me a holler on the Translator slack.

**@therightstef**
