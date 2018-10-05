import requests


class SimSearch(object):

    def __init__(self):
        self.sim_endpoint = 'http://owlsim3.monarchinitiative.org/api/'

    def phenotype_search(self, phenotype_set, matcher='phenodigm'):
        phenotype_set = SimSearch.filter_bl_phenotypes(phenotype_set)
        match = 'match/{}'.format(matcher)
        url = '{0}{1}'.format(self.sim_endpoint, match)
        params = {
            'id': phenotype_set
        }
        results = requests.get(url=url, params=params)
        package = results.json()
        return package

    @staticmethod
    def filter_bl_phenotypes(phenotype_list):
        phenotype_blacklist = ['HP:0025023']
        for elem in phenotype_blacklist:
            if elem in phenotype_list:
                phenotype_list.remove(elem)
        return phenotype_list


