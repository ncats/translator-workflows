import requests
from pprint import pprint


class SimSearch(object):

    def __init__(self):
        self.sim_endpoint = 'http://owlsim3.monarchinitiative.org/api/'

    def phenotypes2disease(self, phenotype_set, matcher='phenodigm'):
        match = 'match/{}'.format(matcher)
        url = '{0}{1}'.format(self.sim_endpoint, match)
        params = {
            'id': phenotype_set
        }
        results = requests.get(url=url, params=params)
        package = results.json()
        diseases = []
        curies = []
        for match in package['matches']:
            if 'NCBIGene' not in match['matchId']:
                diseases.append(match)
                curies.append(match['matchId'])

        return {'data': diseases,
                'disease_curies': curies,
                }


