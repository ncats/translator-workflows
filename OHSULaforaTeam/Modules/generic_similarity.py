from ontobio.ontol_factory import OntologyFactory
from ontobio.io.gafparser import GafParser
from ontobio.assoc_factory import AssociationSetFactory
from ontobio.assocmodel import AssociationSet
from typing import List, Union, TextIO
from ontobio.analysis.semsim import jaccard_similarity
from pprint import pprint


class GenericSimilarity(object):
    def __init__(self) -> None:
        self.associations = ''
        self.ontology = ''
        self.assocs = ''
        self.afactory = AssociationSetFactory()

    def retrieve_associations(self, ont, group):
        taxon_map = {
            'human': 'NCBITaxon:9606',
            'mouse': 'NCBITaxon:10090',
        }
        ofactory = OntologyFactory()
        self.ontology = ofactory.create(ont)
        p = GafParser()
        url = ''
        if ont == 'go':
            go_roots = set(self.ontology.descendants('GO:0008150') + self.ontology.descendants('GO:0003674'))
            sub_ont = self.ontology.subontology(go_roots)
            if group == 'mouse':
                url = "http://current.geneontology.org/annotations/mgi.gaf.gz"
            if group == 'human':
                url = "http://current.geneontology.org/annotations/goa_human.gaf.gz"
            assocs = p.parse(url)
            self.assocs = assocs
            assocs = [x for x in assocs if 'header' not in x.keys()]
            assocs = [x for x in assocs if x['object']['id'] in go_roots]
            self.associations = self.afactory.create_from_assocs(assocs, ontology=sub_ont)
        else:
            self.associations = self.afactory.create(ontology=self.ontology ,
                       subject_category='gene',
                       object_category='phenotype',
                       taxon=taxon_map[group])

    def compute_jaccard(self, input_genes:List[dict], lower_bound:float=0.7) -> List[dict]:
        similarities = []
        for index, igene in enumerate(input_genes):
            for subject_curie in self.associations.subject_label_map.keys():
                input_gene = GenericSimilarity.trim_mgi_prefix(input_gene=igene['sim_input_curie'], subject_curie=subject_curie)
                if input_gene is not subject_curie:
                    score = jaccard_similarity(self.associations, input_gene, subject_curie)
                    if float(score) > float(lower_bound):
                        subject_label = self.associations.label(subject_curie)
                        similarities.append({
                            'input_id': input_gene,
                            'input_symbol': igene['input_symbol'],
                            'hit_symbol': subject_label,
                            'hit_id': subject_curie,
                            'score': score,
                        })
        return similarities

    @staticmethod
    def trim_mgi_prefix(input_gene, subject_curie):
        if 'MGI:MGI:' in subject_curie and 'MGI:MGI:' in input_gene:
            return input_gene
        elif 'MGI:MGI:' not in subject_curie and 'MGI:MGI:' in input_gene:
            return input_gene[4:]

        else:
            return input_gene
