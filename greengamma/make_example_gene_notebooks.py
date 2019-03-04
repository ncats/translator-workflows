import nbformat 
from  nbformat import v4  as nbf
import os,sys

import_cell_source = \
"""#To make nicer looking outputs
from IPython.core.display import display, HTML
import requests
import pandas as pd
import os
import sys

#Load some functions for parsing quick output
module_path = os.path.abspath(os.path.join('../..'))
if module_path not in sys.path:
        sys.path.append(module_path)
from gg_functions import parse_answer, get_view_url, expand

robokop='robokop.renci.org' """

execute_cell_source= \
"""turl=lambda robokop,disease_id,disease_name: f'http://{{robokop}}/api/simple/quick/template/{}/{{disease_id}}/?name1={{disease_name}}&max_connectivity={}'

def execute_example(disease_id,disease_name,nn="{}"):
    url = turl(robokop,disease_id,disease_name)
    display(HTML(f'<h3>{{disease_name}}</h3>'))
    response = requests.get(url)
    if response.status_code != 200:
        print('Error')
        return
    answers=response.json()
    if len(answers['answers']) == 0:
        print("No answers found")
        return
    view_url = get_view_url(answers)
    display(HTML(f'<a href={{view_url}}>View Answer in ROBOKOP</a>'))
    answer_frame = parse_answer(answers,node_list=[nn])
    known=expand('disease',disease_id,'gene')
    if len(known['answers']) > 0:
        known_genes = parse_answer(known,node_list=['n1'],node_properties=['id'])
        v = known_genes['n1 - id'].values
        final_answer = answer_frame[ ~ answer_frame['n3 - id'].isin(v) ]
    else:
        print("No previously known answers")
        final_answer = answer_frame
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        display(final_answer)
"""

#load in some example disease lists to try
example_path = os.path.abspath(os.path.join('examples'))
sys.path.append(example_path)
from disease_lists import rare_diseases, common_diseases
#diseases = disease_lists.rare_diseases + disease_lists.common_diseases
diseases = rare_diseases + common_diseases
diseasescf = common_diseases + rare_diseases

def create_notebook(notebook_path,robokop_template_name,nodename,title,inputs,maxcon):
    notebook = nbf.new_notebook()

    cell = nbf.new_markdown_cell(f'## {title}')
    notebook.cells.append(cell)

    cell = nbf.new_code_cell(import_cell_source)
    notebook.cells.append(cell)

    cell = nbf.new_code_cell(execute_cell_source.format(robokop_template_name,maxcon,nodename))
    notebook.cells.append(cell)

    for disease_id, disease_name in inputs:
        cell = nbf.new_code_cell(f'execute_example("{disease_id}","{disease_name}")')
        notebook.cells.append(cell)

    nbformat.write(notebook,notebook_path)

#create_notebook('workflow2/module1/Workflow2Module1a_ROBOKOP_examples.ipynb','wf2mod1a','n3','Workflow 2, Module 1a',diseases,1000)

#create_notebook('workflow2/module1/Workflow2Module1a_v2_ROBOKOP_examples.ipynb','wf2mod1a_v2','n3','Workflow 2, Module 1a (disease relevant processes only)',diseases,1000)

create_notebook('workflow2/module1/Workflow2Module1d_ROBOKOP_examples.ipynb','wf2mod1d','n3','Workflow 2, Module 1d',diseases,1000)
#create_notebook('workflow2/module1/Workflow2Module1d_v2_ROBOKOP_examples.ipynb','wf2mod1d_v2','n3','Workflow 2, Module 1d (disease relevant chemicals only)',diseases,1000)
