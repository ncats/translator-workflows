import pandas as pd

from BioLink.biolink_client import BioLinkWrapper
from MyGene.mygene_client import QueryMyGene
from ontobio.ontol_factory import OntologyFactory
from ontobio.io.gafparser import GafParser
from ontobio.assoc_factory import AssociationSetFactory
from pprint import pprint


class FunctionalSim(object):
    """

    """
    def __init__(self):
        self.ontology = self.load_ontology(ont='go')
        self.gene_set = ''
        self.associations = ''
        self.taxon = None

    def load_gene_set(self, gene_set, taxon=None):
        self.gene_set = gene_set
        self.taxon = taxon

    def load_associations(self, group):
        p = GafParser()
        afactory = AssociationSetFactory()
        url = "http://geneontology.org/gene-associations/gene_association.{}.gz".format(group)
        if group == 'human':
            url = "http://geneontology.org/gene-associations/goa_human.gaf.gz"
        assocs = p.parse(url)
        assocs = [x for x in assocs if 'header' not in x.keys()]
        self.associations = afactory.create_from_assocs(assocs, ontology=self.ontology)

    def compute_similarity(self):
        sims = list()
        for gene in self.gene_set:
            mg = QueryMyGene(curie=gene, taxon=self.taxon)
            mg.query_mygene()
            gene_dat = mg.package
            ukb = mg.parse_uniprot()
            symbol = gene_dat['symbol']
            for sub_gene in list(self.associations.subject_label_map.keys()):
                amScore = self.associations.jaccard_similarity('UniProtKB:{}'.format("".join(ukb)), sub_gene)
                if amScore > .7 and amScore < 1:
                    sims.append({
                        'input_gene': symbol,
                        'input_gene_curie': gene,
                        'sim_gene_name': self.associations.label(sub_gene),
                        'sim_hit_curie': sub_gene,
                        'sim_score': amScore,
                    })
        return sims

    @staticmethod
    def load_ontology(ont):
        print('loading ontology -- this can take a while')
        ofactory = OntologyFactory()
        return ofactory.create(ont)











