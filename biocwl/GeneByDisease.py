import fire
from biocwl.biocwl import BiolinkWorkflowCommand
import biolinkmodel.datamodel
from typing import Set


class GeneByDisease(BiolinkWorkflowCommand):
    def __init__(self):
        super().__init__()
        self.spec = self._read_spec()
        """
        {
            'input_type': {
                'complexity': 'single',
                'id_type': ['MONDO', 'DO', 'OMIM'],
                'data_type': 'disease'
            },
            'output_type': {
                'complexity': 'set',
                'id_type': 'HGNC',
                'data_type': 'gene'
            },
            'taxon': 'human',
            'limit': None,
            'source': 'Monarch Biolink',
            'predicate': 'blm:gene associated with condition'
        }
        """

    # todo: how do we ensure integrity between these type arguments and the spec
        # in this case there is no bridge for inference from the spec. on the other hand these types are only
        # weakly enforced and are thus strictly optional, meant mainly for the developer's convenience
    def _process_input(self, input: biolinkmodel.datamodel.DiseaseId) -> Set[biolinkmodel.datamodel.GeneId]:
        # todo delegate the mod0 processing into here!
        return type(input)


if __name__ == '__main__':
    fire.Fire(DiseaseGeneLookup)
