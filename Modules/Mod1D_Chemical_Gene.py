from CTD.CTD_wrapper import CTDWrapper



class ChemicalGeneInteractions(object):
    def __init__(self):
        self.ctd = CTDWrapper()
        self.gene_set = ''
        self.chemicals = []

    def load_gene_set(self, gene_set):
        self.gene_set = gene_set

    def load_chemicals(self, action):
        gene_chemicals = list()
        for index, row in self.gene_set.iterrows():
            gene_chemicals = gene_chemicals + self.ctd.gene2chem(row[3].split(':')[-1])
            gene_chemicals = [x for x in gene_chemicals if action in x['InteractionActions']]
        self.chemicals = self.chemicals + gene_chemicals

    def load_gene_hits(self):
        for chem in self.chemicals:
            print(self.ctd.chem2gene(chem_curie=chem['ChemicalID']))

