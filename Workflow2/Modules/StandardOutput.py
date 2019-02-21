from datetime import datetime


class StandardOutput(object):
    edge_types = {
        'Mod0': 'pathogenic_for',
        'Mod1A': 'functially_similar_to',
        'Mod1B': 'phenotypically_similar_to',
        'Mod1E': 'interacts_with'
    }
    essence_map ={
        'Mod0': 'disease, gene',
        'Mod1A': 'gene, functional similarity',
        'Mod1B': 'gene, phenotypic similarity',
        'Mod1E': 'protein, interactions'
    }

    def __init__(self, results, input_object):
        self.results = results
        self.input_object = input_object
        self.results_count = len(results)
        self.output_object = self.mod_level_output()
        self.generate_result()

    def mod_level_output(self):
        return {
            'context': 'https://raw.githubusercontent.com/biolink/biolink-model/master/context.jsonld',
            'datetime': str(datetime.now()),
            'id': '',
            'message': '{} results found'.format(self.results_count),
            'n_results': self.results_count,
            'original_question_text': 'What genes are functionally similar to genes associated with {}'.format(
                self.input_object['id']),
            'query_type_id': 'query_id',
            'reasoner_id': 'Orange',
            'response_code': 'OK',
            'restated_question_text': 'What genes are functionally similar to genes associated with {}'.format(
                self.input_object['id']),
            'result_list': [],
            'schema_version': '0.8.0',
            'table_column_names': ['input_id', 'input_symbol', 'result_id', 'result_symbol', 'score'],
            'terms': {'disease': 'gene_id'},
            'tool_version': 'orange',
            'type': 'medical_translator_query_response'
        }

    def generate_result(self):
        for result in self.results:
            result_meta = {'confidence': result['score'],
                           'essence': StandardOutput.essence_map[result['module']],
                           'id': result['module'],
                           'reasoner_id': "orange",
                           'result_graph': {
                               'edge_list': [],
                               'node_list': [],
                           },
                           'result_type': 'gene',
                           'row_data': [",".join(list(result.keys()))],
                           'text': ''}

            edge = {'is_defined_by': 'orange',
                    'provided_by': 'BioLink',
                    'source_id': result['input_id'],
                    'target_id': result['hit_id'],
                    'type': StandardOutput.edge_types[result['module']]
                    }

            nodes = [{
                'description': 'gene',
                'id': result['hit_id'],
                'name': result['hit_symbol'],
                'type': 'gene',
                'uri': ''},
                {
                    'description': 'gene',
                    'id': result['input_id'],
                    'name': result['input_symbol'],
                    'type': 'gene',
                    'uri': ''
                },
            ]

            result_meta['result_graph']['edge_list'].append(edge)
            for node in nodes:
                result_meta['result_graph']['node_list'].append(node)
            self.output_object['result_list'].append(result_meta)
