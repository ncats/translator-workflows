from MyGene.mygene_client import QueryMyGene
from ontobio.ontol_factory import OntologyFactory
from ontobio.io.gafparser import GafParser
from ontobio.assoc_factory import AssociationSetFactory
from ontobio.assocmodel import AssociationSet
from .generic_similarity import GenericSimilarity
from pprint import pprint
from typing import List, Union, TextIO

class FunctionalSimilarity(GenericSimilarity):
    def __init__(self, associations:AssociationSet=None):
        GenericSimilarity.__init__(self, associations=associations)

        self.gene_set = []
        self.identifier_map = {}


    def load_associations(self,
                          ontology_name:str='go',
                          subject_category: str = 'gene',
                          object_category: str = 'function',
                          evidence=None,
                          taxon: str = None,
                          relation=None,
                          file: Union[str, TextIO] = None,
                          fmt: str = None,
                          skim: bool = False) -> None:
        GenericSimilarity.load_associations(
            self,
            group='human',
            ont='go',
        )

    def load_gene_set(self, gene_set:List[str], taxon:str=None):
        for gene in gene_set:
            mg = QueryMyGene()
            gene_dat = mg.query_mygene(curie=gene, taxon=taxon, fields='uniprot, symbol')
            uniprotkb = 'UniProtKB:{}'.format(gene_dat[0]['uniprot']['Swiss-Prot'])
            symbol = gene_dat[0]['symbol']
            self.gene_set.append({
                'gene_curie': gene,
                'uniprot_curie': uniprotkb,
                'symbol': symbol
            })


    def compute_similarity(self, lower_bound:float=0.7, upper_bound:float=1.0) -> List[dict]:
        results = self.compute_jaccard(self.gene_set, lower_bound, upper_bound)
        return results

