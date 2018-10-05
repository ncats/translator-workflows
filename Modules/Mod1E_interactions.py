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
            mg = MyGeneInfo()
            mg_hit = mg.query(gene.replace('hgnc:', ''),
                              scopes='HGNC',
                              species=self.input_object['parameters']['taxon'],
                              fields='uniprot, symbol')
            try:
                symbol = mg_hit['hits'][0]['symbol']
                self.gene_set.append({
                    'sim_input_curie': gene,
                    'symbol': symbol
                })
            except Exception as e:
                print(gene, e)

    def get_interactions(self):
        results = []
        for gene in self.gene_set:
            interactions = self.blw.gene_interactions(gene_curie=gene['sim_input_curie'])
            for assoc in interactions['associations']:
                interaction = self.blw.parse_association(input_id=gene['sim_input_curie'],
                                                          input_label=gene['symbol'],
                                                          association=assoc)
                results.append({
                    'input_curie': interaction['input_id'],
                    'input_label': interaction['input_label'],
                    'hit_name': interaction['hit_label'],
                    'hit_curie': interaction['hit_id'],
                    'hit_score': None,
                })


        return results


