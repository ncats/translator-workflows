import urllib.request
import json
import requests
from collections import defaultdict

FA_genes_url = "https://raw.githubusercontent.com/NCATS-Tangerine/cq-notebooks/master/FA_gene_sets/FA_1_core_complex.txt"
FA_genes_all_url = "https://raw.githubusercontent.com/NCATS-Tangerine/cq-notebooks/master/FA_gene_sets/FA_4_all_genes.txt"
FA_geneset = []

with urllib.request.urlopen(FA_genes_all_url) as url:
     FA_geneset.append(url.read().decode().split('\n'))

starting_geneset = []
for gene in FA_geneset[0]:
        if not gene: # there was an empty ('') string in the input list of genes, we ignore those.
            continue
        else:
            gene = gene.split(None, 1)[0]
            gene = gene.lower()
            starting_geneset.append(gene)
print('here is the simplified FA_geneset:', starting_geneset)
print()

simple_starting_geneset = []            
simple_starting_geneset.append(starting_geneset[0])
simple_starting_geneset.append(starting_geneset[1])

print('here is the simplified FA_geneset:', simple_starting_geneset)
print()
bicluster_gene_url = 'https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_gene/'
cooccurrence_dict_all_genes = defaultdict(dict)

for gene_id in simple_starting_geneset:
    coocurrence_dict_each_gene = defaultdict(dict)
    print(gene_id)
    quick_url = bicluster_gene_url + gene_id + '/'

    response = requests.get(quick_url)
    response_json = response.json()
    coocurrence_dict_each_gene['number_of_coocurrences'] = len(response_json)
    for x in response_json:
        each_coocurrence_dict = defaultdict(dict)
       # each_coocurrence_dict[gene_id]['bicluster']
        print(x['bicluster'])
    print(gene_id)
    cooccurrence_dict_all_genes[gene_id] = dict(coocurrence_dict_each_gene)
    
print(cooccurrence_dict_all_genes)