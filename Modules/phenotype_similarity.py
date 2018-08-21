from functools import reduce
import pandas as pd
from BioLink import biolink_client
from SimSearch.simsearch_client import SimSearchWrapper


class PhenotypicSimilarity:
    b = biolink_client.BioLinkWrapper()
    ssw = SimSearchWrapper()
    taxon_map = {
        'mouse': '10090',
        'rat': '10116',
        'zebrafish': '7955',
        'fly': '7227',
        'worm': '6239'
    }

    def __init__(self, genes, taxon):
        """
        Input: a list of human genes, a taxon to compute phenotypic similarity across (curies)
        step1: get phenotypes for each gene
        step2: for each gene's phenotypes, get phenotypically similar genes from taxon `taxon`
        step3: sum the score across all phenotypically similar genes


        """
        self.input_genes = genes
        self.taxon = taxon
        self.gene_phenotypes = {gene: self.ids_as_list(self.b.gene2phenotypes(gene)) for gene in genes}
        self.gene_ssr = {gene: self.ssw.get_phenotypically_similar_genes(phenotypes, taxon=taxon) for gene, phenotypes
                         in self.gene_phenotypes.items()}
        all_results = [ssr.get_results() for ssr in self.gene_ssr.values()]
        self.phenogene_score = reduce(lambda x, y: pd.merge(x, y, on='id').set_index('id').sum(axis=1), all_results)

    def explain_phenotypically_similar_gene(self, gene_curie):
        # why did this gene come back?

        # gene_curie had matching phenotypes with these genes (from the input gene list)
        matching_input_genes = {gene for gene, ssr in self.gene_ssr.items() if gene_curie in {m.get_id() for m in ssr.matches}}
        df = pd.DataFrame()
        for gene in matching_input_genes:
            results = self.gene_ssr[gene].get_results()
            results['input_gene'] = gene
            df = df.append(results.query("id == @gene_curie"))

        return df

    @staticmethod
    def ids_as_list(d):
        return [x['object']['id'] for x in d['associations']]
