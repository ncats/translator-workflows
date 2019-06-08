import fire
from typing import List
import biolinkmodel.datamodel
from biocwl import biocwl

class DiseaseGeneLookup(biocwl.BiolinkWorkflowCommand):
    def __init__(self):
        super().__init__()
        self.spec = {
            'data_type': 'disease',
            'input_type': {
                'complexity': 'single',
                'id_type': ['MONDO', 'DO', 'OMIM'],
            },
            'output_type': {
                'complexity': 'set',
                'id_type': 'HGNC'
            },
            'taxon': 'human',
            'limit': None,
            'source': 'Monarch Biolink',
            'predicate': 'blm:gene associated with condition'
        }

    def _process_input(self, input: biolinkmodel.datamodel.Disease):  # -> List[biolinkmodel.datamodel.Gene]:
        return type(input)


if __name__ == '__main__':
    fire.Fire(DiseaseGeneLookup)
