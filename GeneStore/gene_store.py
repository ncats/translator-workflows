import pandas as pd


class FanconiGeneImporter(object):
    sets = {
        'fa_core': 'FA_1_core_complex.txt',
        'fa_all': 'FA_4_all_genes.txt'
    }
    gh_config = {
        "base_url": "https://raw.githubusercontent.com/NCATS-Tangerine/cq-notebooks/master/FA_gene_sets/",
        "columns": ['gene_curie', 'gene_symbol'],
    }

    def __init__(self, gene_set_name):
        self.gene_set_name = gene_set_name
        self.gene_df = self.gene_set_df()

    def gene_set_df(self):
        return pd.read_csv(
            FanconiGeneImporter.gh_config['base_url'] +
            FanconiGeneImporter.sets[self.gene_set_name], sep='\t',
            names=FanconiGeneImporter.gh_config['columns']
        )

    def list_gene_ids(self):
        return self.gene_df['gene_curie'].tolist()

    def list_gene_symbols(self):
        return self.gene_df['gene_symbol'].tolist()

    def gene_objects(self):
        return self.gene_df.to_dict(orient='records')



