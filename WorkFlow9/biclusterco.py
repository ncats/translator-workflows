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

class CuratedGenesetBicluster():
    def __init__(self):
        pass
    
    def find_related_biclusters(self, curated_geneset):
        for gene in curated_geneset: 
            quick_url = bicluster_gene_url + gene + '/'
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
                    for bicluster in response_2_json:
                        gene_in_each_bicluster_list.append(bicluster['gene'])
                    coocurrence_dict_each_gene['related_biclusters'][related_bicluster] = gene_in_each_bicluster_list
            cooccurrence_dict_all_genes[gene] = dict(coocurrence_dict_each_gene)
        return cooccurrence_dict_all_genes
    
# with open('FA_geneset_gene_coocurrences_from_bicluster_gene_enrichment_py.txt', 'w') as file:
#     file.write(json.dumps(cooccurrence_dict_all_genes))

    async def find_related_biclusters_async(self, curated_geneset):
        workers = len(curated_geneset)
        url_list = [bicluster_gene_url + gene + '/' for gene in curated_geneset]
        print(url_list)
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:

            loop = asyncio.get_event_loop()
            responses = [
                loop.run_in_executor(
                    executor, 
                    requests.get, 
                    url
            )
           
            for url in url_list
        ]
        for x in await asyncio.gather(*responses):
            bicluster_dict = defaultdict(dict)
            coocurrence_dict_each_gene['related_biclusters'][x['bicluster']] = []
            for related_bicluster in coocurrence_dict_each_gene['related_biclusters']:
                quick_url_2 = bicluster_bicluster_url + related_bicluster + '/'
                response_2 = requests.get(quick_url_2)
                response_2_json = response_2.json()
                gene_in_each_bicluster_list = []
                for bicluster in response_2_json:
                    gene_in_each_bicluster_list.append(bicluster['gene'])
                coocurrence_dict_each_gene['related_biclusters'][related_bicluster] = gene_in_each_bicluster_list
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())





if __name__ == '__main__':
    pass

