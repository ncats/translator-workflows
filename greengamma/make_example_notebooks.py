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
module_path = os.path.abspath(os.path.join('../../..'))
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
    known=expand('disease',disease_id,'chemical_substance',predicate='treats',direction='in')
    if len(known['answers']) > 0:
        known_frame = parse_answer(known,node_list=['n1'],node_properties=['id'],answer_properties=[] )
        answer_with_known = pd.merge(answer_frame, known_frame, left_on=f'{{nn}} - id',right_on='n1 - id', how = 'left')
        answer_with_known['Known Treatment'] = ~answer_with_known['n1 - id'].isnull()
        answer_with_known.drop('n1 - id',axis=1,inplace=True)
    else:
        print("No previously known answers")
        answer_with_known = answer_frame
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        display(answer_with_known)
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

#create_notebook('workflow1/module2/module/Workflow1Module2_ROBOKOP_examples.ipynb','wf1mod2_direct','n2','Workflow 1, Module 2 (no pathway expansion)',diseases,1000)

create_notebook('workflow1/module2/module/Workflow1Module2_expanded_ROBOKOP_examples.ipynb','wf1mod2_expanded','n4','Workflow 1, Module 2 (pathway expansion)',diseases,500)

create_notebook('workflow1/module3/module/Workflow1Module3_ROBOKOP_examples.ipynb','wf1mod3','n3','Workflow 1, Module 3',diseasescf,0)

create_notebook('workflow1/module3/module/Workflow1Module3a_ROBOKOP_examples.ipynb','wf1mod3_v2','n3','Workflow 1, Module 3a',diseasescf,0)
