from BioLink.biolink_client import BioLinkWrapper
from pprint import pprint
import pandas as pd


class OrthologTraversal(object):

    def __init__(self, gene_set):
        self.gene_set = gene_set
        self.blw =BioLinkWrapper()

    def ortholog_set_by_taxid(self, taxon_name):
        orthos = self.blw.get_orthoglog_gene_set(gene_set=self.gene_set, orth_taxon_name=taxon_name)
        return orthos










