from BioLink.biolink_client import BioLinkWrapper
from pprint import pprint
import pandas as pd


class OrthologTraversal(object):

    def __init__(self):
        self.blw =BioLinkWrapper()

    def ortholog_set_by_taxid(self, gene_set, taxon_name):
        orthos = self.blw.get_orthoglog_gene_set(gene_set=gene_set, orth_taxon_name=taxon_name)
        orthologs = []
        for ortho in orthos:
            for ortho_id in ortho['associations']:
                orthologs.append(self.blw.parse_association(input_id=ortho_id['subject']['id'],
                                                         input_label=ortho_id['subject']['label'],
                                                         association=ortho_id))
        return orthologs

    def single_gene_ortholog(self, gene, taxon_name):
        ortho = self.blw.gene2orthologs(gene_curie=gene, orth_taxon_name=taxon_name)
        orthologs = []
        for assoc in ortho['associations']:
            orthologs.append({
                'gene_id': gene,
                'orth_id': assoc['object']['id'],
                'orth_label': assoc['object']['label'],
            })
        return orthologs










