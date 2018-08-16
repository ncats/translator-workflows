import requests
from pprint import pprint


class QueryMyGene(object):
    base_url = 'https://mygene.info/v3/query'

    def __init__(self, curie, taxon=None):
        self.curie = curie
        self.taxon = taxon
        self.package = ''

    def trimmed_curie(self):
        curie = ''
        if 'HGNC' in self.curie:
            curie = self.curie.replace('HGNC', 'hgnc')
        else:
            curie = self.curie.split(':')[1]

        return curie

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
            'fields': 'all',
        }

        hit = requests.get(url=QueryMyGene.base_url, params=q_params)
        hit = hit.json()

        if 'hits' in hit.keys() and len(hit['hits']) == 1:
            self.package = hit['hits'][0]
        else:
            print('No MyGene Record for {}'.format(self.curie))

    def parse_uniprot(self):
        if 'uniprot' in self.package.keys():
            uniprot = self.package['uniprot']
            if 'Swiss-Prot' in uniprot.keys():
                if isinstance(uniprot['Swiss-Prot'], list):
                    return uniprot['Swiss-Prot']
                elif isinstance(uniprot['Swiss-Prot'], str):
                    return [uniprot['Swiss-Prot']]
                else:
                    return None
        else:
            return None

    def ec2entrez(self):
        hits = []
        q_params = {
            'q': 'ec:{}'.format(self.curie),
            'fields': 'all',
        }
        results = requests.get(url=QueryMyGene.base_url, params=q_params)
        data = results
        for dat in data.json()['hits']:
            hits.append(QueryMyGene.add_prefix(prefix='NCBIGene', identifier=dat['entrezgene']))
        return hits

    @staticmethod
    def add_prefix(prefix, identifier):
        return '{0}:{1}'.format(prefix, identifier)

