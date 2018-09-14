import requests


class CTDWrapper(object):
    def __init__(self):
        self.url = 'https://ctdapi.renci.org/'

    def gene2chem(self, gene_curie, params=None):
        call = '{0}CTD_chem_gene_ixns_GeneID/{1}/'.format(self.url, gene_curie)
        results = requests.get(call, params)
        return results.json()

    def chem2gene(self, chem_curie, params=None):
        call = '{0}CTD_chem_gene_ixns_ChemicalID/{1}/'.format(self.url, chem_curie)
        results = requests.get(call, params)
        return results.json()

