from CTD.CTD_wrapper import CTDWrapper
import pandas as pd


class ChemicalGeneInteractions(object):
    def __init__(self):
        self.ctd = CTDWrapper()
        self.gene_set = ''
        self.chemicals = []
        self.gene_hits = []

    def load_gene_set(self, gene_set):
        self.gene_set = gene_set

    def get_chemicals(self, action):
        gene_chemicals = list()
        for index, row in self.gene_set.iterrows():
            gene_chemicals = gene_chemicals + self.ctd.gene2chem(row[3].split(':')[-1])
            gene_chemicals = [x for x in gene_chemicals if action in x['InteractionActions'] and '9606' in x['OrganismID']]
        self.chemicals = self.chemicals + gene_chemicals

    def get_genes(self, chemical_id, action):
        ctd_hits = self.ctd.chem2gene(chem_curie=chemical_id)
        chemical_genes = [x for x in ctd_hits if action in x['InteractionActions'] and '9606' in x['OrganismID']]
        return chemical_genes

    def load_gene_hits(self, action, rows):
        chem_df = pd.DataFrame(self.chemicals).groupby(['GeneSymbol', 'GeneID'])['ChemicalID'].apply(', '.join).reset_index().to_dict(orient='records')
        for chem in chem_df:
            for index, cid in enumerate(chem['ChemicalID'].split(',')):
                if index < rows:
                    cid = cid.lstrip().rstrip()
                    cid_hit = self.get_genes(chemical_id=cid, action=action)
                    self.gene_hits = self.gene_hits + cid_hit


