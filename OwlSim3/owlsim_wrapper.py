import requests
from pprint import pprint


class SimSearch(object):

    def __init__(self):
        self.sim_endpoint = 'http://owlsim3.monarchinitiative.org/api/'
        self.staged_results = ''

    def phenotype_search(self, phenotype_set, matcher='phenodigm'):
        phenotype_set = SimSearch.filter_bl_phenotypes(phenotype_set)
        match = 'match/{}'.format(matcher)
        url = '{0}{1}'.format(self.sim_endpoint, match)
        params = {
            'id': phenotype_set
        }
        results = requests.get(url=url, params=params)
        package = results.json()
        self.staged_results = package

    def disease_results(self):
        diseases = []
        curies = []
        for match in self.staged_results['matches']:
            if 'NCBIGene' not in match['matchId']:
                diseases.append(match)
                curies.append(match['matchId'])

        return {'data': diseases,
                'disease_curies': curies,
                }

    def gene_results(self):
        genes = []
        curies = []
        for match in self.staged_results['matches']:
            if 'NCBIGene' in match['matchId']:
                genes.append(match)
                curies.append(match['matchId'])

        return {'data': genes,
                'disease_curies': curies,
                }

    @staticmethod
    def filter_bl_phenotypes(phenotype_list):
        phenotype_blacklist = ['HP:0025023']
        for elem in phenotype_blacklist:
            phenotype_list.remove(elem)
        return phenotype_list


