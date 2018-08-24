from ontobio.ontol_factory import OntologyFactory
from ontobio.assoc_factory import AssociationSetFactory

from ontobio.assocmodel import AssociationSet
from ontobio.ontol import Ontology
from typing import List, Union, TextIO

from ontobio.analysis.semsim import jaccard_similarity

class GenericSimilarity(object):
    def __init__(self, associations:AssociationSet=None) -> None:
        self.associations = associations

    def load_associations(self, ontology_name:str=None, subject_category:str=None, object_category:str=None, evidence=None, taxon:str=None, relation=None, file:Union[str, TextIO]=None, fmt:str=None, skim:bool=False) -> None:
        ofactory = OntologyFactory()
        afactory = AssociationSetFactory()

        ontology = ofactory.create(ontology_name, subject_category)

        self.associations = afactory.create(
            ontology=ontology,
            subject_category=subject_category,
            object_category=object_category,
            evidence=evidence,
            taxon=taxon,
            relation=relation,
            file=file,
            fmt=fmt,
            skim=skim
        )

    def compute_jaccard(self, input_curies:List[str], lower_bound:float=0.7, upper_bound:float=1.0) -> List[dict]:
        similarities = []

        for input_curie in input_curies:
            for subject_curie in self.associations.subject_label_map.keys():
                score = jaccard_similarity(self.associations, input_curie, subject_curie)

                if score > lower_bound and score < upper_bound:
                    similarities.append({
                        'input_curie': input_curie,
                        'sim_hit_name': self.associations.label(subject_curie),
                        'sim_hit_curie': subject_curie,
                        'sim_score': score,
                    })

        return similarities
