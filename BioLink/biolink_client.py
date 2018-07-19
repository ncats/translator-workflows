import requests
from pprint import pprint


class BioLinkWrapper(object):
    def __init__(self):
        self.endpoint = 'https://api.monarchinitiative.org/api/'
        self.params = {
            'fetch_objects': 'true',
        }

    def get_gene(self, gene_curie):
        params = {}
        url = '{0}bioentity/gene/{1}'.format(self.endpoint, gene_curie)
        response = requests.get(url, params)
        return response.json()

    def get_orthologs(self, gene_curie, orth_taxon_name=None):
        taxon_map = {
            'mouse': 'NCBITaxon:10090',
            'rat': 'NCBITaxon:10116',
            'zebrafish': 'NCBITaxon:7955',
        }
        params = {}
        if orth_taxon_name:
            params['homolog_taxon'] = taxon_map[orth_taxon_name]
        url = '{}bioentity/gene/{}/homologs/'.format(self.endpoint, gene_curie)
        response = requests.get(url, params)
        return "".join(response.json()['objects'])

    def get_phenotypes(self, gene_curie):
        url = '{}bioentity/gene/{}/phenotypes/'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def get_diseases(self, gene_curie):
        url = '{}bioentity/gene/{}/diseases/'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def get_interactions(self, gene_curie):
        url = '{}bioentity/gene/{}/interactions/'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def get_functions(self, gene_curie):
        url = '{}bioentity/gene/{}/function/'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def get_disease_models(self, disease_curie):
        url = '{}/bioentity/disease/{}/models/'.format(self.endpoint, disease_curie)
        response = requests.get(url)
        return response.json()

    def get_all_phenotypes_for_taxon(self, taxon_curie):
        # get phenotypes associated with taxid
        url = "mart/gene/phenotype/{}".format(self.endpoint, taxon_curie)
        response = requests.get(url)
        return response.json()

    def get_gene_function(self, gene_curie):
        # get function associated with gene
        url = "{}bioentity/gene/{}/function/".format(self.endpoint, gene_curie)
        response = requests.get(url, params=self.params)
        return response.json()

    def parse_gene_functions(self, curie):
        function_list = list()
        functions = self.get_gene_function(gene_curie=curie)
        if 'associations' in functions.keys():
            for assoc in functions['associations']:
                function_list.append(assoc['object']['label'])
        function_set = set(function_list)
        return ", ".join(function_set)

    def get_orthoglog_gene_set(self, gene_set, orth_taxon_name):
        orth_set = []
        for gene in gene_set:
            orth_set.append(self.get_orthologs(gene_curie=gene, orth_taxon_name=orth_taxon_name))
        return orth_set
