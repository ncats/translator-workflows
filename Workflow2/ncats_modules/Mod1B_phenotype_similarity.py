import pandas as pd
from BioLink import biolink_client
from SimSearch.simsearch_client import SimSearchWrapper
from Modules.generic_similarity import GenericSimilarity
from typing import List, Union, TextIO
from pprint import pprint


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
        'worm': '6239',
        'human': '9606',
    }

    def __init__(self, **args) -> None:
        super(PhenotypeSimilarity, self).__init__(**args)
        self.b = biolink_client.BioLinkWrapper()
        self.ssw = SimSearchWrapper()
        self.gene_set = None
        self.taxon = None
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

    def metadata(self):
        print("""Mod1B Phenotype Similarity metadata:""")
        pprint(self.meta)

    def load_input_object(self, input_object):
        self.input_object = input_object

    def load_gene_set(self):
        """
        Load a gene set and taxon
        """
        self.gene_set = self.input_object['input']
        self.taxon = self.taxon_map[self.input_object['parameters']['taxon']]

    def load_associations(self,
                          ontology_name:str=None,
                          subject_category:str='gene',
                          object_category:str='phenotype',
                          evidence=None,
                          taxon:str=None,
                          relation=None,
                          file:Union[str, TextIO]=None,
                          fmt:str=None,
                          skim:bool=False):
        """
        Load gene to phenotype associations
        """
        # calling BioLink API to fetch gene to phenotype associations
        self.gene2phenotype_associations = {
            gene: PhenotypeSimilarity.ids_as_list(self.b.gene2phenotypes(gene)) for gene in self.gene_set}


    def compute_similarity(self, sim_type):
        """
        Perform similarity search and calculate score
        """
        self.ssr = {
            gene: self.ssw.get_phenotypically_similar_genes(input_gene=gene,
                                                            phenotypes=phenotypes,
                                                            taxon=self.taxon) for gene, phenotypes in self.gene2phenotype_associations.items()}
        self.results = [ssr.get_results() for ssr in self.ssr.values()]
        merged = pd.merge(self.results[0], self.results[1], on='id', how='outer')
        merged['summed_score'] = merged.score_x + merged.score_y
        merged = merged[merged['summed_score'] > self.input_object['parameters']['threshold']]
        if sim_type == 'gene':
            merged = merged[~merged['id'].str.contains('MONDO')]
        if sim_type == 'disease':
            merged = merged[merged['id'].str.contains('MONDO')]
        return merged[['input_id_x', 'id', 'label_x', 'summed_score']]

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
