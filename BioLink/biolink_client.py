import requests


class BioLinkWrapper(object):
    def __init__(self):
        self.endpoint = 'https://api.monarchinitiative.org/api/'
        self.params = {
            'fetch_objects': 'true',
        }

    def get_obj(self, obj_id):
        url = '{0}bioentity/{1}'.format(self.endpoint, obj_id)
        response = requests.get(url)
        return response.json()

    def disease2genes(self, disease_curie):
        params = {}
        url = '{0}bioentity/disease/{1}/genes'.format(self.endpoint, disease_curie)
        response = requests.get(url, params)
        return response.json()

    def disease2phenotypes(self, disease_curie):
        params = {}
        url = '{0}bioentity/disease/{1}/phenotypes'.format(self.endpoint, disease_curie)
        response = requests.get(url, params)
        return response.json()

    def gene(self, gene_curie):
        params = {}
        url = '{0}bioentity/gene/{1}'.format(self.endpoint, gene_curie)
        response = requests.get(url, params)
        return response.json()

    def gene2orthologs(self, gene_curie, orth_taxon_name=None):
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
        return response.json()

    def gene2phenotypes(self, gene_curie):
        url = '{}bioentity/gene/{}/phenotypes/'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def gene2diseases(self, gene_curie):
        url = '{}bioentity/gene/{}/diseases/'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def gene_interactions(self, gene_curie):
        url = '{}bioentity/gene/{}/interactions/'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def gene2functions(self, gene_curie):
        url = '{}bioentity/gene/{}/function/'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def disease_models(self, disease_curie):
        url = '{}/bioentity/disease/{}/models/'.format(self.endpoint, disease_curie)
        response = requests.get(url)
        return response.json()

    def taxon2phenotypes(self, taxon_curie):
        # get phenotypes associated with taxid
        url = "mart/gene/phenotype/{}".format(self.endpoint, taxon_curie)
        response = requests.get(url)
        return response.json()

    def parse_gene_functions(self, curie):
        function_list = list()
        functions = self.gene2functions(gene_curie=curie)
        if 'associations' in functions.keys():
            for assoc in functions['associations']:
                function_list.append(assoc['object']['label'])
        function_set = set(function_list)
        return ", ".join(function_set)

    def get_orthoglog_gene_set(self, gene_set, orth_taxon_name):
        orth_set = []
        for gene in gene_set:
            orth_set.append(self.gene2orthologs(gene_curie=gene, orth_taxon_name=orth_taxon_name))
        return orth_set

    @staticmethod
    def return_objects(assoc_package):
        return assoc_package['objects']
