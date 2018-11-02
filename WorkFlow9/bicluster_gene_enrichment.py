import urllib.request
import json
import requests
from collections import defaultdict

FA_genes_url = "https://raw.githubusercontent.com/NCATS-Tangerine/cq-notebooks/master/FA_gene_sets/FA_1_core_complex.txt"
FA_genes_all_url = "https://raw.githubusercontent.com/NCATS-Tangerine/cq-notebooks/master/FA_gene_sets/FA_4_all_genes.txt"
FA_geneset = []

with urllib.request.urlopen(FA_genes_all_url) as url:
     FA_geneset.append(url.read().decode().split('\n'))

# Here is the starting FA_geneset
FA_geneset_0 = []
for gene in FA_geneset[0]:
        if not gene: # there was an empty ('') string in the input list of genes, we ignore those.
            continue
        else:
            gene = gene.split(None, 1)[0]
            gene = gene.lower()
            FA_geneset_0.append(gene)
print()            
print('FA_geneset_0:', FA_geneset_0)
print()

# If you want to test the script on a small subset of genes, uncomment the four lines below and change the for loop which follows.
# reduced_FA_geneset_0 = []            
# reduced_FA_geneset_0.append(FA_geneset_0[0])
# reduced_FA_geneset_0.append(FA_geneset_0[1])
# print('the reduced_FA_geneset_0:', reduced_FA_geneset_0)
# print()

bicluster_gene_url = 'https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_gene/'
bicluster_bicluster_url = 'https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_bicluster/'
cooccurrence_dict_all_genes = defaultdict(dict)

for gene_id in FA_geneset_0:
    quick_url = bicluster_gene_url + gene_id + '/'
    response = requests.get(quick_url)
    response_json = response.json()
    coocurrence_dict_each_gene = defaultdict(dict)
    coocurrence_dict_each_gene['related_biclusters'] = defaultdict(dict)
    coocurrence_dict_each_gene['number_of_related_biclusters'] = len(response_json)
    for x in response_json:
        bicluster_dict = defaultdict(dict)
        coocurrence_dict_each_gene['related_biclusters'][x['bicluster']] = []
        for related_bicluster in coocurrence_dict_each_gene['related_biclusters']:
            quick_url_2 = bicluster_bicluster_url + related_bicluster + '/'
            response_2 = requests.get(quick_url_2)
            response_2_json = response_2.json()
            gene_in_each_bicluster_list = []
            for z in response_2_json:
                gene_in_each_bicluster_list.append(z['gene'])
            coocurrence_dict_each_gene['related_biclusters'][related_bicluster] = gene_in_each_bicluster_list
    cooccurrence_dict_all_genes[gene_id] = dict(coocurrence_dict_each_gene)
# print()
# print(cooccurrence_dict_all_genes)
# print()
with open('FA_geneset_gene_coocurrences_from_bicluster_gene_enrichment_py.txt', 'w') as file:
    file.write(json.dumps(cooccurrence_dict_all_genes))