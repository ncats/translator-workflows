import requests
from pprint import pprint


class QueryMyGene(object):
    mg_config = {
        'base_url': 'https://mygene.info/v3/query',
        'base_params': {
            'fields': 'all',
        }
    }

    def __init__(self, curie, taxon=None):
        self.curie = curie
        self.taxon = taxon
        self.package = ''

    def trimmed_curie(self):
        return self.curie.split(':')[1]

    def query_mygene(self):
        taxon_map = {
            'mouse': r'mgi:MGI\\:',
            'rat': 'rgd:',
            'zfin': 'zfin:',
        }
        curie = self.trimmed_curie()
        if self.taxon:
            curie = '{0}{1}'.format(taxon_map[self.taxon], self.trimmed_curie())
        q_params = {
            'q': curie,
        }
        QueryMyGene.mg_config['base_params'].update(q_params)
        hit = requests.get(url=QueryMyGene.mg_config['base_url'], params=QueryMyGene.mg_config['base_params'])
        hit = hit.json()

        if 'hits' in hit.keys() and len(hit['hits']) == 1:
            self.package = hit['hits'][0]
        else:
            print('No MyGene Record for {}'.format(self.curie))

    def parse_uniprot(self):
        uniprot = self.package['uniprot']
        if 'Swiss-Prot' in uniprot.keys():
            if isinstance(uniprot['Swiss-Prot'], list):
                return uniprot['Swiss-Prot']
            elif isinstance(uniprot['Swiss-Prot'], str):
                return [uniprot['Swiss-Prot']]
            else:
                return None


