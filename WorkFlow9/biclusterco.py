import urllib.request
import json
import requests
import asyncio
import concurrent.futures
import requests
from collections import defaultdict

bicluster_gene_url = 'https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_gene/'
bicluster_bicluster_url = 'https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_bicluster/'
cooccurrence_dict_all_genes = defaultdict(dict)

class GetInput():
    def __init__(self):
        pass
    
    def get_geneset(self, geneset_url):
        with urllib.request.urlopen(geneset_url) as url:
            geneset = url.read().decode().split('\n')
        return geneset

    def curate_geneset(self, geneset):
        curated_geneset = []
        for gene in geneset:
            if not gene: # there was an empty ('') string in the input list of genes, we ignore those.
                continue
            else:
                gene = gene.split(None, 1)[0]
                gene = gene.lower()
                curated_geneset.append(gene)
        return curated_geneset
        
    def run_getinput(self, geneset_url):
        geneset = self.get_geneset(geneset_url)
        curated_geneset = self.curate_geneset(geneset)
        return curated_geneset

class GetBiclusters():
    def __init__(self):
        pass
    
    def find_related_biclusters(self, curated_geneset):
        for gene in curated_geneset: 
            request_1_url = bicluster_gene_url + gene + '/'
            response = requests.get(request_1_url)
            response_json = response.json()
            coocurrence_dict_each_gene = defaultdict(dict)
            coocurrence_dict_each_gene['related_biclusters'] = defaultdict(dict)
            coocurrence_dict_each_gene['number_of_related_biclusters'] = len(response_json)
            for x in response_json:
                bicluster_dict = defaultdict(dict)
                coocurrence_dict_each_gene['related_biclusters'][x['bicluster']] = []
                for related_bicluster in coocurrence_dict_each_gene['related_biclusters']:
                    request_2_url = bicluster_bicluster_url + related_bicluster + '/'
                    response_2 = requests.get(request_2_url)
                    response_2_json = response_2.json()
                    gene_in_each_bicluster_list = [bicluster['gene'] for bicluster in response_2_json]
                    coocurrence_dict_each_gene['related_biclusters'][related_bicluster] = gene_in_each_bicluster_list
            cooccurrence_dict_all_genes[gene] = dict(coocurrence_dict_each_gene)
        return cooccurrence_dict_all_genes

    async def find_related_biclusters_async(curated_geneset):
        bicluster_url_list = [bicluster_gene_url + gene + '/' for gene in curated_geneset]
        length_bicluster_url_list = len(bicluster_url_list)
        with concurrent.futures.ThreadPoolExecutor(max_workers=length_bicluster_url_list) as executor_1:
            loop_1 = asyncio.get_event_loop()
            futures_1 = [ loop_1.run_in_executor(executor_1, requests.get, request_1_url) for request_1_url in bicluster_url_list ]
            for response in await asyncio.gather(*futures_1):
                coocurrence_dict_each_gene = defaultdict(dict)
                coocurrence_dict_each_gene['related_biclusters'] = defaultdict(dict)
                response_json = response.json()
                length_response_json = len(response_json)
                coocurrence_dict_each_gene['number_of_related_biclusters'] = length_response_json
                if length_response_json > 0:
                    gene = response_json[0]['gene']
                    for x in response_json:
                        bicluster = x['bicluster']
                        coocurrence_dict_each_gene['related_biclusters'][x['bicluster']] = []         
                    related_biclusters = [x for x in coocurrence_dict_each_gene['related_biclusters']]
                    bicluster_bicluster_url_list = [bicluster_bicluster_url+related_bicluster+'/' for related_bicluster in related_biclusters]
                    with concurrent.futures.ThreadPoolExecutor(max_workers=coocurrence_dict_each_gene['number_of_related_biclusters']) as executor_2:
                        loop_2 = asyncio.get_event_loop()
                        futures_2 = [ loop_2.run_in_executor(executor_2, requests.get, request_2_url) for request_2_url in bicluster_bicluster_url_list]
                        for response_2 in await asyncio.gather(*futures_2):
                            response_2_json = response_2.json()     
                            genes_in_each_bicluster = [bicluster['gene'] for bicluster in response_2_json]
                            biclusterindex = [x['bicluster'] for x in response_2_json]
                            coocurrence_dict_each_gene['related_biclusters'][biclusterindex[0]] = genes_in_each_bicluster
                        cooccurrence_dict_all_genes[gene] = dict(coocurrence_dict_each_gene)
        return cooccurrence_dict_all_genes
# with open('FA_geneset_gene_coocurrences_from_bicluster_gene_enrichment_py.txt', 'w') as file:
#     file.write(json.dumps(cooccurrence_dict_all_genes))