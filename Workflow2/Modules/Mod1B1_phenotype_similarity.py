from mygene import MyGeneInfo
from ontobio.assocmodel import AssociationSet
from .generic_similarity import GenericSimilarity
from typing import List, Union, TextIO
from pprint import pprint

class PhenotypeSimilarity(GenericSimilarity):
    def __init__(self):
        GenericSimilarity.__init__(self)
        self.gene_set = []
        self.input_object = ''
        self.group = ''
        self.ont = ''
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

    def metadata(self):
        print("""Mod1B1 Phenotype Similarity metadata:""")
        pprint(self.meta)

    def load_input_object(self, input_object):
        self.input_object = input_object
        if self.input_object['parameters']['taxon'] == 'mouse':
            self.group = 'mouse'
            self.ont = 'mp'
        if self.input_object['parameters']['taxon'] == 'human':
            self.group = 'human'
            self.ont = 'hp'

    def load_associations(self):
        self.retrieve_associations(ont=self.ont, group=self.group)

    def load_gene_set(self):
        for gene in self.input_object['input']:
            mg = MyGeneInfo()
            gene_curie = ''
            sim_input_curie = ''
            symbol = ''
            if 'MGI' in gene['hit_id']:
                gene_curie = gene['hit_id']
                sim_input_curie = gene['hit_id']
                # if self.ont == 'go':
                #     sim_input_curie = gene.replace('MGI', 'MGI:MGI')
                # else:
                #
                symbol = None
            if 'HGNC' in gene['hit_id']:
                mgi_gene_curie = gene['hit_id'].replace('HGNC', 'hgnc')
                scope = 'HGNC'
                mg_hit = mg.query(mgi_gene_curie,
                                  scopes=scope,
                                  species=self.input_object['parameters']['taxon'],
                                  fields='uniprot, symbol, HGNC',
                                  entrezonly=True)
                try:
                    gene_curie = gene['hit_id']
                    sim_input_curie = gene['hit_id']
                    symbol = mg_hit['hits'][0]['symbol']

                except Exception as e:
                    print(gene, e)
            self.gene_set.append({
                'input_id': gene_curie,
                'sim_input_curie': sim_input_curie,
                'input_symbol': gene['hit_symbol']
            })

    def compute_similarity(self):
        lower_bound = float(self.input_object['parameters']['threshold'])
        results = self.compute_jaccard(self.gene_set, lower_bound)
        for result in results:
            for gene in self.gene_set:
                if gene['sim_input_curie'] == result['input_id']:
                    result['input_symbol'] = gene['input_symbol']
        return results



