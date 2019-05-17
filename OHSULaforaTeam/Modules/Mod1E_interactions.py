from BioLink.biolink_client import BioLinkWrapper
from pprint import pprint
from mygene import MyGeneInfo


class GeneInteractions(object):
    def __init__(self):
        self.blw = BioLinkWrapper()
        self.gene_set = []
        self.input_object = ''
        self.meta = {
            'input_type': {
                'complexity': 'set',
                'id_type': 'HGNC',
                'data_type': 'gene',
            },
            'output_type': {
                'complexity': 'set',
                'id_type': 'HGNC',
                'data_type': 'gene',
            },

            'source': 'Monarch Biolink',
            'predicate': ['blm:interacts with']
        }
        print("""Mod1E Interaction Network metadata:""")
        pprint(self.meta)

    def load_input_object(self, input_object):
        self.input_object = input_object

    def load_gene_set(self):
        for gene in self.input_object['input']:
            self.gene_set.append({
                'input_id': gene['hit_id'],
                'sim_input_curie': gene['hit_id'],
                'input_symbol': gene['hit_symbol']
            })

    def get_interactions(self):
        results = []
        for gene in self.gene_set:
            interactions = self.blw.gene_interactions(gene_curie=gene['sim_input_curie'])
            for assoc in interactions['associations']:
                interaction = self.blw.parse_association(input_id=gene['sim_input_curie'],
                                                          input_label=gene['input_symbol'],
                                                          association=assoc)
                results.append({
                    'input_id': interaction['input_id'],
                    'input_symbol': interaction['input_symbol'],
                    'hit_symbol': interaction['hit_symbol'],
                    'hit_id': interaction['hit_id'],
                    'score': 0,
                })
        return results

