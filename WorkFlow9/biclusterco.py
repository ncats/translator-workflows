###NOTE: DEPRECATED IN FAVOR OF bicluster_YYY_to_ZZZ.py modules
### no longer being updated as of March 7, 2019

import urllib.request
import json
import requests
import asyncio
import concurrent.futures
import requests
from collections import defaultdict

import aiohttp

bicluster_gene_url = 'https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_v3_gene/'

bicluster_tissue_url = 'https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_v3_all_col_labels/' # Marcin will create a new API endpoint for inputting all_tissue_IDs to replace this ... this will also be the endpoints for when we do gene --> tissues and tissues --> tissues
bicluster_bicluster_url = 'https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_v3_bicluster/'
related_biclusters_and_genes_for_each_input_gene = defaultdict(dict)
related_biclusters_and_tissues_for_each_input_tissue = defaultdict(dict)
related_biclusters_and_genes_for_each_input_tissue = defaultdict(dict)

class CoocurrenceByBicluster():
    def __init__(self):
        pass
    
    def get_ID_list(self, ID_list_url):
        with urllib.request.urlopen(ID_list_url) as url:
            ID_list = url.read().decode().split('\n')
        return ID_list

    def curated_ID_list(self, ID_list):
        curated_ID_list = []
        for ID in ID_list:
            if not ID: # there was an empty ('') string in the input list of genes, we ignore those.
                continue
            else:
                ID = ID.split(None, 1)[0]
                ID = ID.lower()
                curated_ID_list.append(ID)
        return curated_ID_list
        
    def run_getinput(self, ID_list_url):
        ID_list = self.get_ID_list(ID_list_url)
        curated_ID_list = self.curated_ID_list(ID_list)
        return curated_ID_list

    ### !!! this is the non-async version of the code... it works but it is slow. kept for reference. !!!
    # def find_related_biclusters(self, curated_ID_list):
    #     #this function is an artifact... a way to understand 'find_related_biclusters_async', below
    #     for gene in curated_ID_list: 
    #         request_1_url = bicluster_gene_url + gene + '/'
    #         response = requests.get(request_1_url)
    #         response_json = response.json()
    #         coocurrence_dict_each_gene = defaultdict(dict)
    #         coocurrence_dict_each_gene['related_biclusters'] = defaultdict(dict)
    #         coocurrence_dict_each_gene['number_of_related_biclusters'] = len(response_json)
    #         for x in response_json:
    #             bicluster_dict = defaultdict(dict)
    #             coocurrence_dict_each_gene['related_biclusters'][x['bicluster']] = []
    #             for related_bicluster in coocurrence_dict_each_gene['related_biclusters']:
    #                 request_2_url = bicluster_bicluster_url + related_bicluster + '/'
    #                 response_2 = requests.get(request_2_url)
    #                 response_2_json = response_2.json()
    #                 gene_in_each_bicluster_list = [bicluster['gene'] for bicluster in response_2_json]
    #                 coocurrence_dict_each_gene['related_biclusters'][related_bicluster] = gene_in_each_bicluster_list
    #         related_biclusters_and_genes_for_each_input_gene[gene] = dict(coocurrence_dict_each_gene)
    #     return related_biclusters_and_genes_for_each_input_gene

    async def gene_to_gene_biclusters_async(self, curated_ID_list):
        bicluster_url_list = [bicluster_gene_url + gene + '/' +'?include_similar=true' for gene in curated_ID_list]
        length_bicluster_url_list = len(bicluster_url_list)
        #with concurrent.futures.ThreadPoolExecutor(max_workers=length_bicluster_url_list/4) as executor_1:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor_1:
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
                    #with concurrent.futures.ThreadPoolExecutor(max_workers=coocurrence_dict_each_gene['number_of_related_biclusters']/4) as executor_2:
                    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor_2:
                        
                        loop_2 = asyncio.get_event_loop()
                        futures_2 = [ loop_2.run_in_executor(executor_2, requests.get, request_2_url) for request_2_url in bicluster_bicluster_url_list]
                        for response_2 in await asyncio.gather(*futures_2):
                            response_2_json = response_2.json()     
                            genes_in_each_bicluster = [bicluster['gene'] for bicluster in response_2_json]
                            biclusterindex = [x['bicluster'] for x in response_2_json]
                            coocurrence_dict_each_gene['related_biclusters'][biclusterindex[0]] = genes_in_each_bicluster
                        related_biclusters_and_genes_for_each_input_gene[gene] = dict(coocurrence_dict_each_gene)
        return related_biclusters_and_genes_for_each_input_gene

    # not yet completed
    async def gene_to_tissue_biclusters_async(self, curated_ID_list):
        bicluster_url_list = [bicluster_gene_url + gene + '/' +'?include_similar=true' for gene in curated_ID_list]
        length_bicluster_url_list = len(bicluster_url_list)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor_1:
            loop_1 = asyncio.get_event_loop()
            futures_1 = [ loop_1.run_in_executor(executor_1, requests.get, request_1_url) for request_1_url in bicluster_url_list ]
            for response in await asyncio.gather(*futures_1):
                coocurrence_dict_each_gene = defaultdict(dict)
                coocurrence_dict_each_gene['related_biclusters'] = defaultdict(dict)
                response_json = response.json()
                print(response_json)
                print()
                length_response_json = len(response_json)
                coocurrence_dict_each_gene['number_of_related_biclusters'] = length_response_json
                if length_response_json > 0:
                    gene = response_json[0]['gene']
                    for x in response_json:         
                        bicluster = x['bicluster']
                        coocurrence_dict_each_gene['related_biclusters'][x['bicluster']] = []         
                    related_biclusters = [x for x in coocurrence_dict_each_gene['related_biclusters']]
                    bicluster_bicluster_url_list = [bicluster_bicluster_url+related_bicluster+'/' for related_bicluster in related_biclusters]
                    with concurrent.futures.ThreadPoolExecutor(max_workers=coocurrence_dict_each_gene['number_of_related_biclusters']/2) as executor_2:
                        loop_2 = asyncio.get_event_loop()
                        futures_2 = [ loop_2.run_in_executor(executor_2, requests.get, request_2_url) for request_2_url in bicluster_bicluster_url_list]
                        for response_2 in await asyncio.gather(*futures_2):
                            response_2_json = response_2.json()     
                            tissues_in_each_bicluster = [bicluster['all_col_labels'] for bicluster in response_2_json]
                            biclusterindex = [x['bicluster'] for x in response_2_json]
                            coocurrence_dict_each_gene['related_biclusters'][biclusterindex[0]] = tissues_in_each_bicluster
                        related_biclusters_and_tissues_for_each_input_gene[gene] = dict(coocurrence_dict_each_gene)
        return related_biclusters_and_tissues_for_each_input_gene

    async def tissue_to_gene_biclusters_async(self, curated_ID_list):
        bicluster_url_list = [bicluster_tissue_url + tissue + '/' + '?include_similar=true' for tissue in curated_ID_list]
        length_bicluster_url_list = len(bicluster_url_list)
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor_1:
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
                    
                    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor_2:
                        loop_2 = asyncio.get_event_loop()
                        futures_2 = [ loop_2.run_in_executor(executor_2, requests.get, request_2_url) for request_2_url in bicluster_bicluster_url_list]
                        for response_2 in await asyncio.gather(*futures_2): 
                            response_2_json = response_2.json()     
                            genes_in_each_bicluster = [bicluster['gene'] for bicluster in response_2_json]
                            biclusterindex = [x['bicluster'] for x in response_2_json]
                            coocurrence_dict_each_gene['related_biclusters'][biclusterindex[0]] = genes_in_each_bicluster
                        related_biclusters_and_genes_for_each_input_tissue[gene] = dict(coocurrence_dict_each_gene)
        return related_biclusters_and_genes_for_each_input_tissue
    
    # not yet completed
    async def tissue_to_tissue_biclusters_async(self, curated_ID_list):
        bicluster_url_list = [bicluster_tissue_url + tissue + '/' + '?include_similar=true' for tissue in curated_ID_list]
        length_bicluster_url_list = len(bicluster_url_list)
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor_1:
            loop_1 = asyncio.get_event_loop()
            futures_1 = [ loop_1.run_in_executor(executor_1, requests.get, request_1_url) for request_1_url in bicluster_url_list ]
            for response in await asyncio.gather(*futures_1):
                coocurrence_dict_each_tissue = defaultdict(dict)
                coocurrence_dict_each_tissue['related_biclusters'] = defaultdict(dict)
                response_json = response.json()
                length_response_json = len(response_json)
                coocurrence_dict_each_tissue['number_of_related_biclusters'] = length_response_json
                if length_response_json > 0:
                    tissue = response_json[0]['all_col_labels']
                    for x in response_json:         
                        bicluster = x['bicluster']
                        coocurrence_dict_each_tissue['related_biclusters'][x['bicluster']] = []         
                    related_biclusters = [x for x in coocurrence_dict_each_tissue['related_biclusters']]
                    bicluster_bicluster_url_list = [bicluster_bicluster_url+related_bicluster+'/' for related_bicluster in related_biclusters]
                    
                    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor_2:
                        loop_2 = asyncio.get_event_loop()
                        futures_2 = [ loop_2.run_in_executor(executor_2, requests.get, request_2_url) for request_2_url in bicluster_bicluster_url_list]
                        for response_2 in await asyncio.gather(*futures_2): 
                            response_2_json = response_2.json()     
                            tissues_in_each_bicluster = [bicluster['all_col_labels'] for bicluster in response_2_json]
                            biclusterindex = [x['bicluster'] for x in response_2_json]
                            coocurrence_dict_each_tissue['related_biclusters'][biclusterindex[0]] = tissues_in_each_bicluster
                        related_biclusters_and_tissues_for_each_input_tissue[tissue] = dict(coocurrence_dict_each_tissue)
        return related_biclusters_and_tissues_for_each_input_tissue
        
    # the function below returns a dictionary listing all biclusters which occur in the input with a count of how many times each bicluster occurs
    def bicluster_occurences_dict(self, related_biclusters_and_genes_for_each_input_gene):
        bicluster_occurences_dict = defaultdict(dict)
        for key, value in related_biclusters_and_genes_for_each_input_gene.items():
            for key, value in value.items():
                if key == 'related_biclusters':
                    for key, value in value.items():
                        if bicluster_occurences_dict[key]:
                            bicluster_occurences_dict[key] += 1
                        else:
                            bicluster_occurences_dict[key] = 1
        return bicluster_occurences_dict

    def bicluster_occurences_dict_gene_to_tissue(self, related_biclusters_and_tissues_for_each_input_gene):
        bicluster_occurences_dict = defaultdict(dict)
        for key, value in related_biclusters_and_tissues_for_each_input_gene.items():
            for key, value in value.items():
                if key == 'related_biclusters':
                    for key, value in value.items():
                        if bicluster_occurences_dict[key]:
                            bicluster_occurences_dict[key] += 1
                        else:
                            bicluster_occurences_dict[key] = 1
        return bicluster_occurences_dict

    def unique_biclusters(self, bicluster_occurences_dict):
        list_of_unique_biclusters = []
        for key, value in bicluster_occurences_dict.items():
            if value == 1:
                list_of_unique_biclusters.append(key)
        return list_of_unique_biclusters

    # the method below lends itself to async ... reprogram it
    def genes_in_unique_biclusters(self, list_of_unique_biclusters, related_biclusters_and_genes_for_each_input_gene):
        dict_of_genes_in_unique_biclusters = defaultdict(dict)
        for key, value in related_biclusters_and_genes_for_each_input_gene.items():
            for key, value in value.items():
                if key == 'related_biclusters':
                    for key, value in value.items():
                        dict_of_genes_in_unique_biclusters[key] = []
                        if key in list_of_unique_biclusters:
                            dict_of_genes_in_unique_biclusters[key].append(value)
        return dict_of_genes_in_unique_biclusters

    def tissues_in_unique_biclusters(self, list_of_unique_biclusters, related_biclusters_and_tissues_for_each_input_gene):
        dict_of_tissues_in_unique_biclusters = defaultdict(dict)
        for key, value in related_biclusters_and_genes_for_each_input_gene.items():
            for key, value in value.items():
                if key == 'related_biclusters':
                    for key, value in value.items():
                        dict_of_tissues_in_unique_biclusters[key] = []
                        if key in list_of_unique_biclusters:
                            dict_of_tissues_in_unique_biclusters[key].append(value)
        return dict_of_tissues_in_unique_biclusters

    def genes_in_unique_biclusters_not_in_input_gene_list(self, curated_ID_list, dict_of_genes_in_unique_biclusters):
        dict_of_genes_in_unique_biclusters_not_in_inputs = defaultdict(dict)
        for key, value in dict_of_genes_in_unique_biclusters.items():
            if value:
                for gene in value[0]:
                    if gene in curated_ID_list:
                        continue
                    if not dict_of_genes_in_unique_biclusters_not_in_inputs[gene]:
                        dict_of_genes_in_unique_biclusters_not_in_inputs[gene] = 1
                    else:
                        dict_of_genes_in_unique_biclusters_not_in_inputs[gene] += 1
        return dict_of_genes_in_unique_biclusters_not_in_inputs

    def sorted_list_of_output_genes(self, dict_of_genes_in_unique_biclusters_not_in_inputs):
        sorted_list_of_output_genes = sorted((value,key) for (key,value) in dict_of_genes_in_unique_biclusters_not_in_inputs.items())
        sorted_list_of_output_genes.reverse()
        return sorted_list_of_output_genes

    def ids_in_unique_biclusters(self, list_of_unique_biclusters, related_biclusters_and_ids_for_each_input_id):
        dict_of_ids_in_unique_biclusters = defaultdict(dict)
        for key, value in related_biclusters_and_ids_for_each_input_id.items():
            for key, value in value.items():
                if key == 'related_biclusters':
                    for key, value in value.items():
                        dict_of_ids_in_unique_biclusters[key] = []
                        if key in list_of_unique_biclusters:
                            dict_of_ids_in_unique_biclusters[key].append(value)
        return dict_of_ids_in_unique_biclusters

    def ids_in_unique_biclusters_not_in_input_ID_list(self, curated_ID_list, dict_of_ids_in_unique_biclusters):
        dict_of_ids_in_unique_biclusters_not_in_inputs = defaultdict(dict)
        for key, value in dict_of_ids_in_unique_biclusters.items():
            if value:
                for ID in value[0]:
                    # try inserting a split fcn here and basically making a dictionary where every gene gets split and counted, etc, idk...
                    if ID in curated_ID_list:
                        continue
                    if not dict_of_ids_in_unique_biclusters_not_in_inputs[ID]:
                        dict_of_ids_in_unique_biclusters_not_in_inputs[ID] = 1
                    else:
                        dict_of_ids_in_unique_biclusters_not_in_inputs[ID] += 1
        return dict_of_ids_in_unique_biclusters_not_in_inputs

    def sorted_list_of_output_tissues(self, dict_of_ids_in_unique_biclusters_not_in_inputs):
        sorted_list_of_output_tissues = sorted((value,key) for (key,value) in dict_of_ids_in_unique_biclusters_not_in_inputs.items())
        sorted_list_of_output_tissues.reverse()
        return sorted_list_of_output_tissues