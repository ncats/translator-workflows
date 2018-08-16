from OwlSim3.owlsim_wrapper import SimSearch


class PhenotypeSim(object):
    """

    """
    def __init__(self, phenotype_set):
        self.owlsim = SimSearch()
        self.phenotype_set = phenotype_set

    def phenotype_simsearch(self, return_type):
        self.owlsim.phenotype_search(phenotype_set=self.phenotype_set)
        if return_type == 'disease':
            return self.owlsim.disease_results()
        if return_type == 'gene':
            return self.owlsim.gene_results()


