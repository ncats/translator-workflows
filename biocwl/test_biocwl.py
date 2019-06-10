"""
BioCWL Test Coverage
* Systems Integration
    * Workflow Layer
        * Workflows must return correct results that are potentially transformable into objects in the Biolink Model
            (Out of scope, just pick a workflow module that is known to work well)
    * Wrapper Layer
        # Given a mocked-up spec, the following must be true:
        * Runner must
            * Input must be validated correctly, else return nothing
            * Process Function must successfully produce mocked output
            * Process Function must be capabable of being overriden without affecting other tasks (ensure modularity)
            * Output must be transformed and validated correctly, else return nothing
        # The default BiolinkWorkflow should auto-guarantee all its formal properties without semantics from extensions:
            *
    * CWL Layer
        * The CWL-Runner must run the template class with simple types (automorphic, non-custom types)
        * The CWL-Runner must run the template class with singular complex types (automorphic, custom types)
        * The CWL-Runner must run the template class with several complex types (non-endomorphic, injective, custom types)
        * The CWL-Runner must run the template class with multiple singular complex types (non-injective, custom types)
        * The CWL-Runner must run the template class with multiple several complex types (non-injective, custom types)

* Model Validation
    * For each Systems Integration test, these custom types must be Biolink Types
"""

from biocwl.biocwl import BiolinkWorkflow
from biocwl.GeneByDisease import GeneByDisease

MockSpec = \
    {
        'input_type': {
            'complexity': 'single',
            'data_type': 'disease',
            'id_type': ['MONDO', 'DO', 'OMIM'],
        },
        'output_type': {
            'complexity': 'set',
            'data_type': 'gene',
            'id_type': 'HGNC'
        },
        'taxon': 'human',
        'limit': None,
        'source': 'Monarch Biolink',
        'predicate': 'blm:gene associated with condition'
    }

mockBiolinkWorkflowCommand = BiolinkWorkflow()
mockGeneByDisease = GeneByDisease()
