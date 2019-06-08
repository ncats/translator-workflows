import fire
import inspect
import biolinkmodel.datamodel

class BiolinkWorkflowCommand(object):
    def __init__(self):
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

    def metadata(self):
        return self.spec

    # TODO: need to make sure this is always extensible to input, because we don't want it to be overriden?
    # else we run the risk fo the implementor forgetting to go through the pre-processing steps
    # convert it into an annotation?
        # TODO: use *args? **kwargs?
    def run(self, input):
        """
        - This run function is a standard
        """
        input = self._deserialize_input(input) if self._valid_input(input) else None
        output = self._process_input(input)
        return self._serialize_output(output) if self._valid_output(output) else None

    def _process_input(self, input):
        output = input
        # todo: transform the biolinkml python into equivalent json_ld output against meta
        return output

    def _deserialize_input(self, input):
        input = biolink_object_factory(self.spec['input_type']['data_type'], input)
        return input

    def _serialize_output(self, output):
        # todo
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
                # todo: handle complexity validation
                pass
            elif key is 'data_type':
                # todo: handle datatype validation
                pass
            elif key is 'id_type':
                # todo: handle datatype validation
                pass
            # todo: else: other cases?
        return True

def biolink_object_factory(spec_obj, input):
    # https://realpython.com/python-metaclasses/
    # https://realpython.com/python-data-classes/#more-flexible-data-classes
    # https://stackoverflow.com/questions/1796180/how-can-i-get-a-list-of-all-classes-within-current-module-in-python
    # https://stackoverflow.com/questions/2466191/set-attributes-from-dictionary-in-python
    data_type = spec_obj.title()  # TODO: guarantee camelcase? would imply guaranteeing a certain format for self.spec (need spaces)
    biolink_models = inspect.getmembers(biolinkmodel.datamodel, lambda x: inspect.isclass(x) and x.__name__ is data_type)
    print(biolink_models)
    data_class = biolink_models[0][1]
    biolinkObj = object.__new__(data_class)
    for key in input:
        setattr(biolinkObj, key, input[key])
    return biolinkObj

if __name__ == '__main__':
    fire.Fire(BiolinkWorkflowCommand)

