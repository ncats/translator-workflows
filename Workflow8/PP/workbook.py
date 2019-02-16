## Hello

name = "Theo"
print(name)

## Getting many DOI IDs
import json
from pprint import pprint

with open('./data/doid.json') as f:
    data = json.load(f)

pprint(data)


#%% Playing around with workflow 8 functionality

from biggim_tak16jan2019  import doid_to_genes, call_biggim
genes = doid_to_genes("117")

print(genes)
print(len(genes))

