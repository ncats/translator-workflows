from ontobio.ontol_factory import OntologyFactory
from ontobio.io.gafparser import GafParser
from ontobio.assoc_factory import AssociationSetFactory
from ontobio.assocmodel import AssociationSet
from typing import List, Union, TextIO
from ontobio.analysis.semsim import jaccard_similarity


class GenericSimilarity(object):
    def __init__(self, associations:AssociationSet=None) -> None:
        self.associations = associations
        self.ofactory = OntologyFactory()

    def load_associations(self, ont, group, parse=False):
        taxon_map = {
            'human': 'NCBITaxon:9606',
            'mouse': 'NCBITaxon:10090',
        }
        ont_fac = self.ofactory.create(ont)
        p = GafParser()
        afactory = AssociationSetFactory()
        if ont == 'go':
            url = "http://geneontology.org/gene-associations/gene_association.{}.gz".format(group)
            if group == 'human':
                url = "http://geneontology.org/gene-associations/goa_human.gaf.gz"
            assocs = p.parse(url)
            assocs = [x for x in assocs if 'header' not in x.keys()]
            self.associations = afactory.create_from_assocs(assocs, ontology=ont_fac)

        if ont == 'hp':
            self.associations = afactory.create(ontology=ont_fac,
                       subject_category='gene',
                       object_category='phenotype',
                       taxon=taxon_map[group])

    def compute_jaccard(self, input_genes:List[dict], lower_bound:float=0.7) -> List[dict]:
        similarities = []
        for index, igene in enumerate(input_genes):
            for subject_curie in self.associations.subject_label_map.keys():
                if igene['sim_input_curie'] is not subject_curie:
                    score = jaccard_similarity(self.associations, igene['sim_input_curie'], subject_curie)

                    if float(score) > float(lower_bound):
                        subject_label = self.associations.label(subject_curie)
                        similarities.append({
                            'input_curie': igene['sim_input_curie'],
                            'sim_hit_name': subject_label,
                            'sim_hit_curie': subject_curie,
                            'sim_score': score,
                        })
        return similarities
