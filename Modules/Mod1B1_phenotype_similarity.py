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
            group=self.input_object['parameters']['taxon'],
            ont='hp',
        )

    def load_gene_set(self):
        for gene in self.input_object['input']:
            mg = MyGeneInfo()
            gene_curie = ''
            sim_input_curie = ''
            symbol = ''
            if 'MGI' in gene:
                gene_curie =  gene
                sim_input_curie = gene.replace('MGI', 'MGI:MGI')
                symbol = None
            if 'HGNC' in gene:
                gene_curie = gene.replace('HGNC', 'hgnc')
                scope = 'HGNC'
                mg_hit = mg.query(gene_curie,
                                  scopes=scope,
                                  species=self.input_object['parameters']['taxon'],
                                  fields='uniprot, symbol, HGNC',
                                  entrezonly=True)
                try:
                    gene_curie = gene
                    sim_input_curie = gene
                    symbol = mg_hit['hits'][0]['symbol']

                except Exception as e:
                    print(gene, e)

            self.gene_set.append({
                'gene_curie': gene_curie,
                'sim_input_curie': sim_input_curie,
                'symbol': symbol
            })


    def compute_similarity(self):
        lower_bound = float(self.input_object['parameters']['threshold'])
        results = self.compute_jaccard(self.gene_set, lower_bound)
        for result in results:
            for ic in self.gene_set:
                if ic['sim_input_curie'] == result['input_curie']:
                    result['input_name'] = ic['symbol']
        return results


