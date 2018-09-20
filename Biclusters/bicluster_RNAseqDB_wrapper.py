import requests
from pprint import pprint


class BiclusterSearch(object):

    def __init__(self):
        self.sim_endpoint = 'https://bicluster.renci.org/apidocs/'

    def get_by_DOID_enrich(self, obj_id):
        url = 'Bicluster_column_enrich_DOID/{0}'.format(self.endpoint, obj_id)
        response = requests.get(url)
        return response.json()

    def get_by_MONDO_enrich(self, obj_id):
        url = 'Bicluster_column_enrich_MONDO/{0}'.format(self.endpoint, obj_id)
        response = requests.get(url)
        return response.json()

    def get_by_NCIT_enrich(self, obj_id):
        url = 'Bicluster_column_enrich_NCIT/{0}'.format(self.endpoint, obj_id)
        response = requests.get(url)
        return response.json()

    def get_by_UBERON_enrich(self, obj_id):
        url = 'Bicluster_column_enrich_UBERON/{0}'.format(self.endpoint, obj_id)
        response = requests.get(url)
        return response.json()

    def get_by_gene(self, obj_id):
        url = 'Bicluster_gene/{0}'.format(self.endpoint, obj_id)
        response = requests.get(url)
        return response.json()

    def get_by_rank(self, obj_id):
        url = 'Bicluster_rank/{0}'.format(self.endpoint, obj_id)
        response = requests.get(url)
        return response.json()

    def get_by_mean(self, obj_id):
        url = 'Bicluster_mean/{0}'.format(self.endpoint, obj_id)
        response = requests.get(url)
        return response.json()

    def get_by_score(self, obj_id):
        url = 'Bicluster_score/{0}'.format(self.endpoint, obj_id)
        response = requests.get(url)
        return response.json()

    def get_by_gene_to_bicluster_cor(self, obj_id):
        url = 'Bicluster_correlation/{0}'.format(self.endpoint, obj_id)
        response = requests.get(url)
        return response.json()