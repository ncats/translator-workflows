import pandas as pd

def parse_answer(returnanswer, 
                   node_list=['n1'], 
                   edge_list= ['e0'], 
                   node_properties =['name', 'id'] , 
                   edge_properties =['type', 'edge_source'],
                   answer_properties= ['score'], 
                   max_edges = 1):    
    """Given an answer in the KG 0.9 format, produce a pandas frame containing answers as rows.

    Parameters
    ----------

    node_list: a list of machine_question node indexes that will be used to generate columns
    edge_list: a list of machine_question edge indexes that will be used to generate columns
    node_properties: a list of properties that will be turned into columns for each node in node_list
    edge_properties: a list of properties that will be turned into columns for each edge in edge_list
    answer_properties: a list of answer properties that will be turned into columns. Defaults to ['score']
    """
    kg_nodes = { n['id']: n for n in returnanswer['knowledge_graph']['nodes']}
    kg_edges = { e['id']: e for e in returnanswer['knowledge_graph']['edges']}
    answers=[]
    for answer in returnanswer['answers']:
        nodes = {}
        for node in node_list:
            if node not in answer['node_bindings']:
                #skip if provided node doesn't exist
                continue
            nodes.update({f'{node} - {prop} ': kg_nodes[answer['node_bindings'][node]][prop]\
                     for prop in node_properties\
                     if prop in kg_nodes[answer['node_bindings'][node]]})
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
                    f'{edge} - {prop}': ' '.join([kg_edges[e[index]][prop] for index in range(0,edge_count)])
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

