from BioLink.biolink_client import BioLinkWrapper
from pprint import pprint
from mygene import MyGeneInfo


class OwlsimSimilarity(object):
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
            'predicate': ['blm:similar_to']
        }
        print("""Mod1B OwlSim Phenotype Similarity metadata:""")
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

    def calculate_similarity(self):
        results = []
        for index, gene in enumerate(self.gene_set):
            try:
                owlsim = self.blw.compute_owlsim(gene['sim_input_curie'])
                for match in owlsim['matches']:
                    if match['type'] == 'gene':
                        results.append({
                            'input_id': gene['input_id'],
                            'input_symbol': gene['input_symbol'],
                            'hit_symbol': match['label'],
                            'hit_id': match['id'],
                            'score': match['score'],
                        })
            except Exception as e:
                print(match['id'], e)
        return results
