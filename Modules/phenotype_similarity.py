from functools import reduce
import pandas as pd
from BioLink import biolink_client
from SimSearch.simsearch_client import SimSearchWrapper
from Modules.generic_similarity import GenericSimilarity
from typing import List, Union, TextIO

class PhenotypeSimilarity(GenericSimilarity):
    """
    Input: a list of human genes, a taxon to compute phenotypic similarity across (curies)
    step1: get phenotypes for each gene
    step2: for each gene's phenotypes, get phenotypically similar genes from taxon `taxon`
    step3: sum the score across all phenotypically similar genes
    """
    taxon_map = {
        'mouse': '10090',
        'rat': '10116',
        'zebrafish': '7955',
        'fly': '7227',
        'worm': '6239'
    }

    def __init__(self, **args) -> None:
        super(PhenotypeSimilarity, self).__init__(**args)
        self.b = biolink_client.BioLinkWrapper()
        self.ssw = SimSearchWrapper()
        self.gene_set = None
        self.taxon = None

    def load_gene_set(self, gene_set:List[str], taxon:str=None):
        """
        Load a gene set and taxon
        """
        self.gene_set = gene_set
        self.taxon = taxon

    def load_associations(self, ontology_name:str=None, subject_category:str='gene', object_category:str='phenotype', evidence=None, taxon:str=None, relation=None, file:Union[str, TextIO]=None, fmt:str=None, skim:bool=False):
        """
        Load gene to phenotype associations
        """
        # calling BioLink API to fetch gene to phenotype associations
        self.gene2phenotype_associations = {gene: PhenotypeSimilarity.ids_as_list(self.b.gene2phenotypes(gene)) for gene in self.gene_set}

    def similarity_search(self):
        """
        Perform similarity search and calculate score
        """
        self.ssr = {gene: self.ssw.get_phenotypically_similar_genes(phenotypes, taxon=self.taxon) for gene, phenotypes in self.gene2phenotype_associations.items()}
        self.results = [ssr.get_results() for ssr in self.ssr.values()]
        self.phenogene_score = reduce(lambda x, y: pd.merge(x, y, on='id').set_index('id').sum(axis=1), self.results)

    def explain_phenotypically_similar_gene(self, gene_curie):
        """
        Why did this gene come back?
        gene_curie had matching phenotypes with these genes (from the input gene list)
        """
        matching_input_genes = {gene for gene, ssr in self.ssr.items() if gene_curie in {m.get_id() for m in ssr.matches}}
        df = pd.DataFrame()
        for gene in matching_input_genes:
            results = self.ssr[gene].get_results()
            results['input_gene'] = gene
            df = df.append(results.query("id == @gene_curie"))

        return df

    @staticmethod
    def ids_as_list(d):
        return [x['object']['id'] for x in d['associations']]
