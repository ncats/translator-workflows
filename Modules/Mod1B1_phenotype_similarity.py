from mygene import MyGeneInfo
from ontobio.assocmodel import AssociationSet
from .generic_similarity import GenericSimilarity
from typing import List, Union, TextIO
from pprint import pprint

class PhenotypeSimilarity(GenericSimilarity):
    def __init__(self, associations:AssociationSet=None):
        GenericSimilarity.__init__(self, associations=associations)
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
            'predicate': ['blm:has phenotype']
        }
        print("""Mod1B Phenotype Similarity metadata:""")
        pprint(self.meta)

    def load_input_object(self, input_object):
        self.input_object = input_object

    def load_associations(self,
                          ontology_name:str='hp',
                          subject_category: str = 'gene',
                          object_category: str = 'phenotype',
                          evidence=None,
                          taxon: str = None,
                          relation=None,
                          file: Union[str, TextIO] = None,
                          fmt: str = None,
                          skim: bool = False) -> None:
        GenericSimilarity.load_associations(
            self,
            group='human',
            ont='hp',
        )

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


    def compute_similarity(self):
        lower_bound = float(self.input_object['parameters']['threshold'])
        results = self.compute_jaccard(self.gene_set, lower_bound)
        return results


