
## Basic Pathfinding and Literature Annotation in GNBR

This notebook was generated during development of the Pharmacogenomics workflow for NCATS Biomedical Data Translator.  The code does a "knowledge graph lookup" on GNBR to find the most parsimonious explanation of a relationship between two entities (chemical, gene, or disease). 

In terms of the underlying operations it works in two steps:
1. Find the top 3 scoring shortest paths between the two nodes of interest
2. Annotate each statement (or relationship) in each path with its strongest supporting sentences

Essentially, what you end up with a bunch of little mini paragraphs that you can evaluate to see if you think the relationship is plausible or not.  Here, I am using it as a tool to decide whether one could reasonably infer that Thioguanine acts through RAC1, if they did not know this a priori.  The actual active metabolite is Thioguanine Triphosphate, but there is no record for it in GNBR, so I am using the next best thing (Thioguanine).  There is no direct association between thioguanine and RAC1 on GNBR.

##### Imports
Networkx is bloatware here.  I was initially thinking about doing the pathfinding using some fancy graph algorithmm (like Sheng's Max flow), but was not worth the work at this early stage.


```python
from neo4j.v1 import GraphDatabase
import math
import pandas as pd
import networkx as nx
```

    /Users/srensi/virtual-environments/neo4j-bolt/lib/python3.6/importlib/_bootstrap.py:219: RuntimeWarning: numpy.dtype size changed, may indicate binary incompatibility. Expected 96, got 88
      return f(*args, **kwds)
    /Users/srensi/virtual-environments/neo4j-bolt/lib/python3.6/importlib/_bootstrap.py:219: RuntimeWarning: numpy.dtype size changed, may indicate binary incompatibility. Expected 96, got 88
      return f(*args, **kwds)


##### Neo4j Driver Setup
I'm using my local Neo4j instance.  An online instance can be found at `http://gnbr.ncats.io:7687`.  Shhhh! It's a secret. 


```python
uri="bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=('', ''))
```

##### Cypher Queries (Pathfinding using statments edges)

The `get_paths` query simply returns all the shortest paths, up to length 3, between two nodes.  Length could easily be 4 or 5, but I kind of feel like any path of more than 2 or 3 hops is starting to get convoluted and sketchy.

The `get_subnetwork` query does something similar, but returns the subnetwork containing all the shortest paths.  I limited the query to returning 25 patterns to cut down on runtime during prototyping because I decided it was a waste of time to import into networkx for fancier stuff at this point in time.  I limited to shortest paths, rather than all paths, because the query was blowing up most likely due to extremely high degree nodes.

Statament edges, in my neo4j model, are aggregate predicate distributions computed over all sentences that mention to entities.  I use them so I don't have to sum over all sentences every time I want to evaluate the serentgh of some relationship. 


```python
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
    
def get_subgraph(tx, source, sink):
    query = """
    MATCH (source :Entity {uri: $source}), (sink :Entity {uri : $sink}),
    p=allshortestpaths( (source)-[:STATEMENT *0..3]-(sink) )
    with p
    unwind nodes(p) as n1 unwind nodes(p) as n1
    match p=(n1)-[:STATEMENT]-(n2)
    return distinct p limit 25
    """
    result = []
    for record in tx.run(query, source=source, sink=sink):
        result.append(record['r'])
    return result
```

Here I am spinning up a session and running the query for Thioguanine and RAC1.  I should probably try Mercaptopurine at some point, since I also believe that it is a metabolite of Thioguanine.  But honestly, it would take a lot to go from Thioguanine to Mercaptopurine to RAC1.  Especially not kowing that RAC1 was the answer beforehand.


```python
with driver.session() as neo4j:
    paths = neo4j.read_transaction(get_paths, source="MESH:D013866", sink="ncbigene:5879")
```

##### Parse Cypher Query Result (Sort Shortest Paths)

This is a pretty rudimentary scoring function for ordering paths returned by the query.  Essentially, I am taking the sum of predicate weights as the score for each edge, and taking the sum of the logs of the edge scores.  The sketchy part is the edge scores.  I should probably be using only the max predicate weight, and definitely normalizing be each edge by the max scoring edge (pooled over the two nodes).  But for rough guestimation it's not that serious.  Also, Sheng already has an alorithm that does this, so why reinvent the wheel?


```python
def total_weight(path):
    total = 0
    for edge in path:
        weight = sum(edge.values())
        total = total + math.log(weight, 10)
    return total
```

Here I'm executing the function.  Look at how ridiculous I am for using the "reverse" parameter instead of just slicing off the end of the list!


```python
top_paths = sorted(paths, key=total_weight, reverse=True)[0:3]
```

##### Cypher Queries (Retreiving strongest sentences)
The `top_sentence` query takes in two entities (chemical, gene, or disease) and a predicate (or relationship) code, and returns the strongest sentences asserting the specified predicate.


```python
def top_sentence(tx, node1, node2, code):
    query = """
    MATCH (m:Entity {uri: $node1})-[:IN_SENTENCE]-(s:Sentence)-[:IN_SENTENCE]-(n:Entity {uri: $node2})
    WITH DISTINCT s
    MATCH (s)-[:HAS_THEME]-(t)
    RETURN s.text as text, s.pmid as pmid, sum(t[$code]) as theme
    ORDER BY theme DESC LIMIT 5
    """
    result = []
    for record in tx.run(query, node1=node1, node2=node2, code=code):
        result.append(record)
    return result
```

##### Annotate Paths

Here I am looping over the top paths from before, and then looping over the statements in each path, querying the strongest sentences supporting each statement.  The one little bit of black magic in here is the max_key line, which uses an anonymous function to pull out the top predicate code for each statement.  Remember that each statement is a distribution over a set of predicates.


```python
explanations = []
with driver.session() as neo4j:
    for top_path in top_paths:
        explanation = []
        for relationship in top_path:
            max_key = sorted(relationship, key=lambda x: (relationship[x], x), reverse=True)[0]
            uris = [i['uri'] for i in relationship.nodes]
            sentences = neo4j.read_transaction(top_sentence, node1=uris[0], node2=uris[1], code=max_key)
            explanation.append(sentences)
        explanations.append(explanation)
```

##### Display Annotated Paths
Here you can inspect the chain of reasoning.  My opinion... looks plausible, but not espcially convincing. I might be convinced to google some stuff, but not necessarily run any benchtop experiments.  And cetainly not strong enough that it would stand out if this were an open ended query (i.e. RAC1 unknown in advance).


```python
print('\n***********************\n')
for explanation in explanations:
    for statement in explanation:
        print('\n'.join([sentence['text'] for sentence in statement]))
        print('\n')
    print('\n***********************\n')
```

    
    ***********************
    
    Phase II evaluation and plasma pharmacokinetics of high-dose intravenous 6-thioguanine in patients with colorectal_carcinoma .
    Fifteen patients with advanced measurable colorectal_carcinoma were treated with intravenous 6-thioguanine -LRB- 6-TG -RRB- at a dosage of 55 mg/m2 for 5 consecutive days every 5 weeks .
    A phase II study of intravenous 6-thioguanine -LRB- NSC-752 -RRB- in advanced colorectal_carcinoma .
    
    
    However , very little is currently known about the expression of Rac1 in colorectal_cancer cells and the roles of Rac1 in the cell cycle progression and cell survival of human colorectal_cancer cells .
    A critical role for Rac1 in tumor progression of human colorectal_adenocarcinoma cells .
    We have investigated the role of Rac1 in colorectal_tumor progression by genetic modification of the human colorectal_adenocarcinoma cell line SW620 to either overexpress Rac1 or lack Rac1 expression .
    METHODS : Rac1 protein of all selected human colorectal_cancer cells and in human colorectal tissue was detected by Western blotting , Rac1-shRNA was used to silence the Rac1 to reduce its expression specifically in Lovo cells .
    Conclusively , our results demonstrate that miR-320a functions as a tumour-suppressive miRNA through targeting Rac1 in CRC .
    
    
    
    ***********************
    
    Mercaptopurine vs thioguanine for the treatment of acute_lymphoblastic_leukemia .
    Portal_hypertension develops in a subset of children with standard risk acute_lymphoblastic_leukemia treated with oral 6-thioguanine during maintenance therapy .
    BACKGROUND/AIMS : The United Kingdom -LRB- UK -RRB- acute lymphoblastic_leukaemia -LRB- ALL -RRB- 97/99 clinical trial compared 6-mercaptopurine -LRB- 6MP -RRB- with 6-thioguanine -LRB- 6TG -RRB- as maintenance therapy for childhood ALL .
    Chronic_hepatotoxicity following 6-thioguanine therapy for childhood acute_lymphoblastic_leukaemia .
    BACKGROUND : 6-Thioguanine treatment in childhood acute_lymphoblastic_leukaemia -LRB- ALL -RRB- has been shown to cause hepatic_veno-occlusive_disease , but this usually resolved with drug withdrawal .
    
    
    Transfection of ALL cells with dominant-negative Rac1 mutant significantly prolonged their chemotactic response to SDF-1a , and this effect was associated with an alteration of CXCR4 internalization .
    These data suggest a regulatory role for Rac1 in the chemotactic response of ALL cells to SDF-1a via receptor processing .
    
    
    
    ***********************
    
    Murine 4T1 cells -LRB- Murine mammary cancer cell line developed from 6-thioguanine resistant tumor -RRB- provide an excellent research tool for metastasis related studies because these cells are highly aggressive and readily metastasize to the lungs .
    6-Thioguanine -LRB- 6TG -RRB- a cytostatic antimetabolite is currently used to treat patients with cancer , in particular leukemias .
    Resistance to 6-thioguanine in mismatch repair-deficient human cancer cell lines correlates with an increase in induced mutations at the HPRT locus .
    DNA mismatch repair -LRB- MMR -RRB- deficiency_in_human_cancers is associated with resistance to a spectrum of clinically active chemotherapy drugs , including 6-thioguanine -LRB- 6-TG -RRB- .
    Intravenous 6-thioguanine or cisplatin , fluorouracil and leucovorin for advanced non-small_cell_lung_cancer : a randomized phase II study of the cancer and leukemia group B .
    
    
    MG132 , an inhibitor of the ubiquitin proteasome pathway , increased the amount of non-phosphorylated IkBa , but not serine-phosphorylated IkBa , indicating that IkBa degradation by Rac1 in starved cancer cells is independent of IkBa serine phosphorylation by IKK .
    Thus , the present study aimed to investigate the mechanism involved in the regulation of G1/S phase transition by Rac1 in cancer cells .
    Although a number of investigations have established the significance of Rho-family GTPases in several human tumors , there is still little information available on the clinical significance of Rac1 expression in non-small_cell_lung_cancer -LRB- NSCLC -RRB- .
    Using the GST-PAK and GST-Rho binding protein pull-down assays for GTP-bound Rac1 , Cdc42 , and RhoA , we showed that treatment of MDA-MB-231 tumor cells with recombinant maspin for a short time period significantly inhibited the activity of Rac1 and Cdc42 , but not RhoA .
    The expression levels of RhoA , active RhoA , Rac1 , and active Rac1 in tumor tissues were higher than in normal tissues .
    
    
    
    ***********************
    


## To Be Continued (maybe)
This last one is some scratch paper where I am normalizing edge weights.  Nothing to see here folks.


```python
"""
match p=(n1:Chemical {uri: "MESH:D013866"})-[:STATEMENT]-(:Entity)
with n1, count(p) as c1
match p=allshortestpaths( (n1)-[:STATEMENT* 0..2]-(n2:Chemical) )
with c1, n2, count(p) as c12
match p=(n2)-[:STATEMENT]-(:Entity)
with n2, c12, c1, count(p) as c2
return n2, (1.0*c12)/(case when c1 > c2 then c1 else c2 end) as score order by score desc limit 10"""
```
