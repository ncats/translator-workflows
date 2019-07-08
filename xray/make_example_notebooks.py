import os
import sys

import nbformat
from nbformat import v4 as nbf
from nbconvert.preprocessors import ExecutePreprocessor


import_cell_source = \
'''
#### Import some needed modules
from IPython.core.display import display, HTML
import pandas as pd
import requests
import json
import sys
'''

execute_cell_source = \
'''
#### Set the base URL for the reasoner and its endpoint
API_BASE_URL = 'https://rtx.ncats.io/api/rtx/v1'
url_str = API_BASE_URL + "/query"

def execute_example(disease_id, disease_name, query_type='{}'):
    display(HTML('<h3>{{}}</h3>'.format(disease_name)))

    #### Create a dict of the request, specifying the query type and its parameters
    request = {{ "query_type_id": query_type, "terms": {{ "disease": "{{}}".format(disease_id) }} }}

    #### Send the request to RTX and check the status
    response_content = requests.post(url_str, json=request, headers={{'accept': 'application/json'}})
    if response_content.status_code != 200:
        print("Error")
        return

    #### Unpack the response content into a dict
    response_dict = response_content.json()
    if 'result_list' not in response_dict:
        print("No results found")
        return
    
    #### Display the summary table of the results
    if "table_column_names" in response_dict:
        result_frame = pd.DataFrame(
            [r['row_data'] for r in response_dict['result_list'][1:]], 
            columns = response_dict['table_column_names']
        )
    
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        display(result_frame)

    #### NOTE: Some rows below appear as duplicates in this summary table but they correspond to different paths in the KG.
'''

# load in some example disease lists to try
example_path = os.path.abspath(os.path.join('examples'))
sys.path.append(example_path)

from disease_lists import disease_ids, disease_names
diseases = zip(disease_ids, disease_names)

def create_notebook(notebook_path,
                    title,
                    query_id,
                    inputs):

    notebook = nbf.new_notebook()

    cell = nbf.new_markdown_cell('## {}'.format(title))
    notebook.cells.append(cell)

    cell = nbf.new_code_cell(import_cell_source)
    notebook.cells.append(cell)

    cell = nbf.new_code_cell(
        execute_cell_source.format(query_id)
    )
    notebook.cells.append(cell)

    for disease_id, disease_name in inputs:
        cell = nbf.new_code_cell(
            f'execute_example("{disease_id}","{disease_name}")'
        )
        notebook.cells.append(cell)

    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(notebook, {'metadata': {'path': './'}})
    with open(notebook_path, 'wt') as f:
        nbformat.write(notebook, f)

create_notebook(
    'WF1_MOD1_MOD2_examples.ipynb',
    'Workflow 1 example code for RTX system',
    'Q55',
    diseases,
)

create_notebook(
    'WF1_2.1_examples.ipynb',
    '',
    'Q7',
    diseases
)
