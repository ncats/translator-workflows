import pandas as pd
import requests

def parse_answer(returnanswer, 
                   node_list=[], 
                   edge_list= [], 
                   node_properties =['name', 'id'] , 
                   edge_properties =['type', 'edge_source'],
                   answer_properties= ['score'], 
                   max_edges = 1,
                   first_x_nodes = 2 #will display the first two nodes if node_list is not specified
                ):    
    """Given an answer in the KG 0.9 format, produce a pandas frame containing answers as rows.

    Parameters
    ----------

    node_list: a list of machine_question node indexes that will be used to generate columns
    edge_list: a list of machine_question edge indexes that will be used to generate columns
    node_properties: a list of properties that will be turned into columns for each node in node_list
    edge_properties: a list of properties that will be turned into columns for each edge in edge_list
    answer_properties: a list of answer properties that will be turned into columns. Defaults to ['score']
    """
    # try to figure out default nodes
    
    node_list = node_list if node_list != [] else [node['id'] for node in  returnanswer['question_graph']['nodes'][:first_x_nodes]]
    kg_nodes = { n['id']: n for n in returnanswer['knowledge_graph']['nodes']}
    kg_edges = { e['id']: e for e in returnanswer['knowledge_graph']['edges']}
    answers=[]
    for answer in returnanswer['answers']:
        nodes = {}
        for node in node_list:
            if node not in answer['node_bindings']:
                #skip if provided node doesn't exist
                continue
            if type(answer['node_bindings'][node]) != list:
                nodes.update({f'{node} - {prop}': kg_nodes[answer['node_bindings'][node]][prop]\
                         for prop in node_properties\
                         if prop in kg_nodes[answer['node_bindings'][node]]})
            else:
                nodes.update({f'{node} - {prop}': ', '.join(
                    kg_nodes[answer['node_bindings'][node][idx]][prop] 
                    for idx, x in enumerate(answer['node_bindings'][node])
                ) for prop in node_properties})
                    
                    
        edges = {}
        for edge in edge_list:
            if edge not in answer['edge_bindings']:
                #skip if provided edge doesn't exist.
                continue
            e = answer['edge_bindings'][edge] 
            edge_count =  max_edges if len(e) > max_edges else len(e)
            if max_edges > 1:
                edges.update({f'{edge} - contains': f'{edge_count} edge'})
            edges.update({
                    f'{edge} - {prop}': ', '.join([kg_edges[e[index]][prop] for index in range(0,edge_count)])
                for prop in edge_properties} )
        nodes.update(edges)
        nodes.update({prop: answer[prop] for prop in answer_properties if prop in answer})
        answers.append(nodes)
    return pd.DataFrame(answers)

def get_view_url(returnanswer,robokop='robokop.renci.org'):
    """Given an answer in KGS v0.9 format, post the answer to robokop, and return a link that can be followed to
    view the answer in the UI"""
    view_post_url = f'http://{robokop}/api/simple/view/'
    view_post_response = requests.post(view_post_url, json=returnanswer)
    uid=view_post_response.json()
    view_url = f'http://{robokop}/simple/view/{uid}'
    return view_url

import requests

def quick(question,max_results=None,output_format=None,max_connectivity=None,robokop_server='robokop.renci.org'):
    """Posts a machine question to ROBOKOP's quick service

    Parameters
    ----------

    question: a machine question in v 0.9 formatn
    max_results: the maximum number of results to return.  Defaults to 250.  0 returns all results.
    max_connectivity: The maximum degree of a node to be included inu an answer.  Used to control generality and speed. Defaults to 0 (unlimited) but 1000 is a good value to try
    robokop_server: the server name or ip address where robokop is running
    """
    url=f'http://{robokop_server}:80/api/simple/quick/'
    if max_results is not None:
        url += f'?max_results={max_results}'
    if output_format is not None:
        j = '&' if '?' in url else '?'
        url += f'{j}output_format={output_format}'
    if max_connectivity is not None:
        j = '&' if '?' in url else '?'
        url += f'{j}max_connectivity={max_connectivity}'
    response = requests.post(url,json=question)
    print( f"Return Status: {response.status_code}" )
    if response.status_code == 200:
        return response.json()
    return response


def expand(type1,identifier,type2,max_results=None,rebuild=None,output_format=None,predicate=None,direction=None,robokop_server='robokop.renci.org'):
    url=f'http://{robokop_server}:80/api/simple/expand/{type1}/{identifier}/{type2}'
    params = {'rebuild': rebuild, 
              'predicate': predicate,
              'output_format': output_format,
              'direction': direction,
              'max_results': max_results}
    params = { k:v for k,v in params.items() if v is not None }
    response = requests.get(url,params=params)
    if response.status_code == 200:
        return response.json()
    return []

