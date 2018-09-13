from BioLink.biolink_client import BioLinkWrapper


class GeneInteractions(object):
    def __init__(self):
        self.blw = BioLinkWrapper()
        self.gene_set = None
        self.interactions = []

    def load_gene_set(self, gene_set):
        self.gene_set = gene_set

    def get_interactions(self):
        for gene in self.gene_set:
            interactions = self.blw.gene_interactions(gene_curie=gene)
            for assoc in interactions['associations']:
                self.interactions.append(self.blw.parse_association(input_id=gene, input_label=None, association=assoc))
