import pandas as pd


class FanconiGeneImporter(object):
    gh_config = {
        "base_url": "https://raw.githubusercontent.com/NCATS-Tangerine/cq-notebooks/master/FA_gene_sets/",
        "columns": ['gene_curie', 'gene_symbol'],
    }

    def __init__(self, gene_set):
        self.gene_set = gene_set

    def fa_core(self):
        return pd.read_csv(
            FanconiGeneImporter.gh_config['base_url'] +
            self.gene_set, sep='\t',
            names=FanconiGeneImporter.gh_config['columns']
        )






