import urllib.request
import json
import requests
import asyncio
import concurrent.futures
from collections import defaultdict, Counter

base_disease_url = 'https://smartbag-hpotomondo.ncats.io/HPO_to_MONDO_mondo_list/'

class disease_to_phenotype():
    def __init__(self):
        pass
    
    def get_ID_list(self, ID_list_url):
        with urllib.request.urlopen(ID_list_url) as url:
            ID_list = url.read().decode().split('\n')
        return ID_list

    def curated_ID_list(self, ID_list):
        curated_ID_list = []
        for ID in ID_list:
            if not ID:
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

    async def disease_to_phenotype_biclusters_async(self, input_ID_list):
        bicluster_url_list = [base_disease_url + disease + '/' +'?include_similar=true' for disease in input_ID_list]
        all_biclusters_dict = defaultdict(dict)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor_1:
            all_phenotypes = []
            loop_1 = asyncio.get_event_loop()
            futures_1 = [ loop_1.run_in_executor(executor_1, requests.get, request_1_url) for request_1_url in bicluster_url_list ]
            for response in await asyncio.gather(*futures_1):
                response_json = response.json()
                for x in response_json:
                    phenotype = x['hpo']
                    all_phenotypes.append(phenotype)
            phenotypes_counted = Counter(all_phenotypes)
        return phenotypes_counted.most_common()