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
from gg_functions import parse_answer, get_view_url, expand, quick

robokop='robokop.renci.org' """

create_question_source= \
"""def create_question(disease_id,prop):
    return {
    "machine_question": {
        "nodes": [
            {
                "id": "n0",
                "type": "chemical_substance",
                prop: True
            },
            {
                "id": "n1",
                "type": "gene"
            },
            {
                "id": "n2",
                "type": "disease",
                "curie": disease_id
            }
        ],
        "edges": [
            {
                "id": "e0",
                "source_id": "n1",
                "target_id": "n0",
                "type": ["increases_degradation_of","decreases_response_to"]
            }
        ]
    }
}
"""

execute_cell_source= \
"""from scipy.stats import hypergeom
from collections import defaultdict
#Read in the list of known property counts
property_counts = pd.read_csv('../../examples/chemprops.txt','\t')

def get_contributing_chemicals(disease_id):
    # Get the chemicals that contribute to the disease
    exp_chemicals = expand('disease',disease_id,'chemical_substance',predicate='contributes_to',direction='in')
    return [x for x in exp_chemicals['knowledge_graph']['nodes'] if x['type'] == 'chemical_substance']

def get_property_counts(bad_chems):
    prop_counts = defaultdict(int)
    for n in bad_chems:
        for p in n:
            prop_counts[p] += 1
            items = list(prop_counts.items())
            count_frame = pd.DataFrame.from_records(items,columns=['property','count_in_subset'])
    return count_frame

#in scipy:
#The hypergeometric distribution models drawing objects from a bin. 
#M is the total number of objects, 
#n is total number of Type I objects. 
#The random variate represents the number of Type I objects in N drawn without replacement from the total population.

total_chemical_count=355413 # M above

def calc_enrich_p(x,n,subset_count):
    return hypergeom.sf(x-1, total_chemical_count, n, subset_count)

def execute_example(disease_id,disease_name):
    display(HTML(f'<h3>{{disease_name}}</h3>'))
    bad_chems = get_contributing_chemicals(disease_id)
    if len(bad_chems) ==0:
        print('No contributing chemicals')
        return
    count_frame = get_property_counts(bad_chems)
    df = pd.merge(count_frame, property_counts,on='property',how='inner')
    for p in ['drug','pharmaceutical','application','pharmacological_role','biological_role','entity',
              'continuant','role','mass','monoisotopic_mass','charge','chemical_role','biochemical_role']:
        df = df[ df['property'] != p]
    df['enrichment_p'] = df.apply(lambda x: calc_enrich_p(x['count_in_subset'], x['count'],len(bad_chems)), axis=1)
    df.sort_values(by='enrichment_p',inplace=True)
    propname = df.iloc[0,0]
    print('Most enriched property:',propname)
    q = create_question(disease_id,propname)
    answers=quick(q)
    if len(answers['answers']) == 0:
        print("No answers found")
        return
    view_url = get_view_url(answers)
    display(HTML(f'<a href={{view_url}}>View Answer in ROBOKOP</a>'))
    answer_frame = parse_answer(answers,node_list=['n0','n1'])
    known=expand('disease',disease_id,'gene')
    if len(known['answers']) > 0:
        known_frame = parse_answer(known,node_list=['n1'],node_properties=['id'],answer_properties=[] )
        known_frame['Known Gene']=True
        answer_with_known = pd.merge(answer_frame, known_frame, on='n1 - id', how = 'left')
        answer_with_known.fillna(False,inplace=True)
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

def create_notebook(notebook_path,robokop_template_name,title,inputs,maxcon):
    notebook = nbf.new_notebook()

    cell = nbf.new_markdown_cell(f'## {title}')
    notebook.cells.append(cell)

    cell = nbf.new_code_cell(import_cell_source)
    notebook.cells.append(cell)

    cell = nbf.new_code_cell(create_question_source)
    notebook.cells.append(cell)

    cell = nbf.new_code_cell(execute_cell_source.format(robokop_template_name,maxcon))
    notebook.cells.append(cell)

    for disease_id, disease_name in inputs:
        cell = nbf.new_code_cell(f'execute_example("{disease_id}","{disease_name}")')
        notebook.cells.append(cell)

    nbformat.write(notebook,notebook_path)

diseases = [('MONDO:0019391','fanconi anemia')]+diseases
create_notebook('workflow2/module2/Workflow2Module2_ROBOKOP_examples.ipynb','wf2mod2','Workflow 2, Module 2d',diseases,0)
