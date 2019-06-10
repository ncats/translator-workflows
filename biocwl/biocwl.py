import fire
import inspect
import biolinkmodel.datamodel
import yaml

class BiolinkWorkflow(object):
    def __init__(self):
        # TODO: does this need to have some kind of equivalence with what is used in CWL?
        """
        Let's make it so.
        * The important feature is that types that are placed in a CWL spec having their eqvuivalents
            used inside of the implementation language.
        * So from the spec, there needs to be a transformation that allows us to infer what these types
            are supposed to be.
        * For the spec to be read, we need to not only to know the location of the spec but also that it's
            the intended spec. But since the spec defines the command, and the command uses the spec, there
            is a circularity that needs to be broken with some extraneous information.
        * In this case we intend the developer to standardize the token name across both the script, the class,
            and the cwl spec (not necessarily the input to the workflow during runtime), so that it is easy to
            determine uniquely what implementation maps to what command, and what types to validate internally.
        """
        self.spec = {
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

        # this acts as the internal state for any runtime related tasks
        # self._input = biolinkObjectFactory()

    def _read_spec(self, spec_name=None):
        if not spec_name:
            spec_name = type(self).__name__ + '.cwl'

        # TODO: read the CWL spec to ensure that this transform is complete
        complexity = {
            'string': 'single',
            'list': 'set',
        }

        with open(spec_name, 'r') as spec_stream:
            try:
                spec_dict = yaml.safe_load(spec_stream)
                # TODO: generalize to multi-input, multi-output spec
                spec = {
                    'input_type': {
                        'complexity': complexity[spec_dict['inputs'][0]['type']],
                        'data_type': spec_dict['inputs'][0]['id'],
                        # TODO: refactor name 'id ~> 'curie for distinction from its uses elsewhere
                        'curie_type': ['MONDO', 'DO', 'OMIM'],
                    },
                    'output_type': {
                        'complexity': complexity[spec_dict['outputs'][0]['type']],
                        'data_type':  spec_dict['outputs'][0]['id'],
                        # TODO: refactor name 'id ~> 'curie for distinction from its uses elsewhere
                        # TODO: Ensure that even if curies used are singular, they are still elements in a list
                            # there should be a uniform treatment of datatypes to reduce exception treatment and bloat.
                        'curie_type': ['HGNC']
                    }
                }
            except Exception as e:
                print("spec didn't load properly")

        return spec

    def metadata(self):
        return self.spec

    # TODO: need to make sure this is always extensible to input, because we don't want it to be overriden?
    # else we run the risk fo the implementor forgetting to go through the pre-processing steps
    # convert it into an annotation?
        # TODO: use *args? **kwargs?
    def run(self, input):
        """
        This run function is a standard interface across all BioCWL scripts to be used as the command
        for such scripts within a CWL specification. Override `_process_input` in your implementation
        for the actual logic of your script.
        """
        input = self._deserialize_input(input) if self._valid_input(input) else None
        output = self._process_input(input)
        return self._serialize_output(output) if self._valid_output(output) else None

    def _process_input(self, input):
        output = input
        # todo: transform the biolinkml python into equivalent json_ld output against meta
        return output

    # TODO: handling multiple I/O types?
    def _deserialize_input(self, input):
        input = biolink_object_factory(self.spec['input_type']['data_type'], input)
        return input

    # TODO: handling multiple I/O types?
    def _serialize_output(self, output):
        return str(output)

    def _valid_input(self, input):
        if self._check(input, self.spec['input_type']):
            return True
        else:
            return False

    def _valid_output(self, output):
        if self._check(output, self.meta['output_type']):
            return True
        else:
            return False

    def _check(self, data, datatype):
        # todo: see if the data is (a) valid json-ld, and (b) satisfies against the biolink schema for given input meta
        for key, value in datatype.items():
            if key is 'complexity':
                # todo: handle complexity validation on data
                pass
            elif key is 'data_type':
                # todo: handle datatype validation on data
                pass
            elif key is 'curie_type':
                # todo: handle datatype validation on data
                pass
            # todo: else: other cases?
        return True

def biolink_object_factory(spec_obj, input):
    # https://realpython.com/python-metaclasses/
    # https://realpython.com/python-data-classes/#more-flexible-data-classes
    # https://stackoverflow.com/questions/1796180/how-can-i-get-a-list-of-all-classes-within-current-module-in-python
    # https://stackoverflow.com/questions/2466191/set-attributes-from-dictionary-in-python
    data_type = spec_obj.title()  # TODO: guarantee camelcase? would imply guaranteeing a certain format for self.spec (need spaces)
    biolink_class = dict(inspect.getmembers(biolinkmodel.datamodel, inspect.isclass))[data_type]
    biolinkObj = object.__new__(biolink_class)
    for key in input:
        setattr(biolinkObj, key, input[key])
    return biolinkObj


if __name__ == '__main__':
    fire.Fire(BiolinkWorkflowCommand)

