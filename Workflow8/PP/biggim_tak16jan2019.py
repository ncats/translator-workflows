import json
import requests
import pandas
import time
from multiprocessing import Pool
import logging

base_url = 'http://biggim.ncats.io/api'

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.debug("test")

def doid_to_genes(doid): 
    """
    Parameters
    ----------
    doid : list of str
    """

    if not isinstance(doid, list): 
        doid = [doid]

    logging.info("Geting HP ids from DOID")

    #http://disease-ontology.org/
    disease_doid = doid
    hpids = doid_to_hp(disease_doid)
    if len(hpids) == 0:
        raise Exception("No phenotypes related to %s" % (str(disease_doid)))
    else:
        print("Returned %i phenotypes" % (len(hpids), ))

    logging.info("Geting OMIM from HP ids")
    #https://hpo.jax.org/app/
    omims = hp_to_omim(hpids, limit=50)

    if len(omims) == 0:
        raise Exception("No mendelian diseases(OMIM) related to %s" % (str(hpids)))
    else:
        print("Returned %i mendelian diseases" % (len(hpids), ))

    logging.info("Geting genes from OMIM")
    #https://omim.org/
    genes = omim_to_gene(omims)
    #genes are ncbi
    if len(genes) == 0:
        raise Exception("No genes associated with %s" % (str(omims),))
    else:
        print("Returned %i genes" % (len(omims,)))

    return genes

"""Running BigGIM"""
def call_biggim(genes, columns, limit, query_id2=False, return_genes=False, limit_genes=500): 
    """
    Parameters
    ----------
    genes : list of str 

    columns : list of str

    limit : int

    query_id2 : bool
        If query_id2, the genes are duplicated for the ids2 field. 
        This forces biggim to return all interactions within genes.
    """

    #columns = ["GTEx_Brain_Correlation"]
    
    gene_list = ','.join(genes)

    example_query = {
        "restriction_gt": ','.join(["%s,0.5" % (c,) for c in columns]),
        "table": "BigGIM_70_v1",
        "columns": ','.join(columns),
        "ids1": gene_list,
        "limit": limit
    }

    if query_id2: 
        example_query["ids2"] = gene_list

    try:
        query_submit = get('biggim/query', data=example_query)
        jprint(query_submit)
    except requests.HTTPError as e:
        print(e)
        
        jprint(e.response.json())

    try:
        while True:
            query_status = get('biggim/status/%s'% (query_submit['request_id'],))
            jprint(query_status)
            if query_status['status'] !='running':
                # query has finished
                break
            else:
                time.sleep(1)
                print("Checking again")
    except requests.HTTPError as e:
        print(e)
        
        jprint(e.response.json())
        
    result = pandas.concat(map(pandas.read_csv, query_status['request_uri']))
    

    if return_genes: 
        df = result
        df  = df.sort_values(by=columns[0],ascending=False)
        df = df.reset_index()
        del df['index']
        gene_list = []
        i = len(gene_list)
        for index, row in df.iterrows():
            if i==limit_genes:
                break
            gene_list.append(row['Gene1'])
            gene_list.append(row['Gene2'])
            gene_list = list(set(gene_list))
            i = len(gene_list)

        gene_list.sort()
        gene_list = [int(x) for x in gene_list]
        gene_list = [str(x) for x in gene_list]

        return gene_list 

    return result

def query_single_edge(_input, _output, _value):
    """
        Retrieve results using one API call from input to output.
        :param _input: the input prefix, for a list of input prefix in BioThings Explorer, visit: http://biothings.io/explorer/api/v2/metadata/bioentities
        :param _output: the output prefix, for a list of output prefix in BioThings Explorer, visit: http://biothings.io/explorer/api/v2/metadata/bioentities
        :_value: The value of the input
        :return:
    """
    """
    endpoint = 'directinput2output'
    base_url = 'http://biothings.io/explorer/api/v2'
    data = {'output_prefix':_output,
            'input_prefix': _input,
            'input_value': _value,
            'format': 'translator'
    }"""
    #doc = get(endpoint, data=data, base_url=base_url)
    qurl = 'http://biothings.io/explorer/api/v2/directinput2output?'
    qurl += 'input_prefix=%s&output_prefix=%s&input_value=%s&format=translator'
    qurl = qurl % (_input, _output, _value)
    print(qurl)
    try:
        req = requests.get(qurl.strip(), timeout=10)
    except:
        print("timeout")
        return []
    #print("Sent: GET %s?%s" % (req.request.url,req.request.body))
    return req.json()


"""Helpers"""

def el(result):
    try:
        return result['result_list']['edge_list']
    except:
        logging.warning(result)
        return []
    

def _doid_to_hp(doid):

    
    qse = query_single_edge(_input='doid', 
                                _output='hp', 
                                _value=doid
                           )
    results = el(qse)
    ts = set([x['target_id'] for x in results])
    return [x.split(':')[-1] for x in ts if x]

def doid_to_hp(doids, limit=None):
    
    #res = my_pool.map(_doid_to_hp, doids)
    res = []
    
    for doid in doids:
        if limit is None or len(set(res)) < limit:
            res += _doid_to_hp(doid)
    return res


def hp_to_omim(hpids, limit=None):
    #res = my_pool.map(_hp_to_omim, hpids)
    res = []
    for hpid in hpids:
        if limit is None or len(set(res)) < limit:
            res += _hp_to_omim(hpid)
    return res

def _hp_to_omim(hpid):
    qse = query_single_edge(_input='hp', 
                                _output='omim.disease', 
                                _value=hpid)
    results = el(qse)
    ts = set([x['target_id'] for x in results])
    return [x.split(':')[-1] for x in ts if x]

def omim_to_gene(omims, limit=None):
    #res = my_pool.map(_omim_to_gene, omims)
    res = []
    for omim in omims:
        if limit is None or len(set(res)) > limit:
            res += _omim_to_gene(omim)
    return res

def _omim_to_gene(omim):
    qse = query_single_edge(_input='omim.disease', 
                                _output='ncbigene',  
                                _value=omim)
    results = el(qse)
    ts = set([x['target_id'] for x in results])
    return [x.split(':')[-1] for x in ts if x]

def _hp_to_uberon(hpid):

    qse = query_single_edge(_input='hp', 
                                _output='uberon', 
                                _value=hpid)
    
    results = el(qse)
    ts = set([x['target_id'] for x in results])
    return [x.split(':')[-1] for x in ts if x]

def hp_to_uberon(hpids, limit=None):
    #res = my_pool.map(_hp_to_uberon,hpids)
    res = []
    
    for hpid in hpids:
        if limit is None or len(set(res)) > limit:
            res += _hp_to_uberon(hpid)
    return res


def uberon_to_bto(ubid):
    uberon_to_bto = json.load(open('bto_uberon_bg.json'))
    for x in uberon_to_bto:
        if x['uberon_id'] == ubid and x['bg_label']:
            return x['bg_label']
    return None


# A few helper functions for posting and getting api requests
#a couple of simple helper functions
def post(endpoint, data={}, base_url=base_url):
    req = requests.post('%s/%s' % (base_url,endpoint), data=data)
    req.raise_for_status()
    return req.json()

def get(endpoint, data={}, base_url=base_url):
    req = requests.get('%s/%s' % (base_url,endpoint), data=data)
    try:
        req.raise_for_status()
    except requests.HTTPError as e:
        print("Sent: GET %s?%s" % (req.request.url,req.request.body))
        if e.response.status_code == 400:
            print(e.response)
            jprint(e.response.json())
        raise
    print("Sent: GET %s?%s" % (req.request.url,req.request.body))
    return req.json()

def jprint(dct):
    print(json.dumps(dct, indent=2))
    
def wrapper(endpoint, data={}, base_url=base_url):
    try:
        response = get(endpoint, data, base_url)
        jprint(response)
    except requests.HTTPError as e:

        print(e)
        if e.response.status_code == 400:
            jprint(e.response.json())
        raise
    try:
        ctr = 1
        while True:
            query_status = get('%s/status/%s'% (endpoint.split('/')[0],response['request_id'],))
            jprint(query_status)
            if query_status['status'] !='running':
                # query has finished
                break
            else:
                time.sleep(ctr)
                ctr += 5
                #linear backoff
                print("Checking again")
    except requests.HTTPError as e:
        print(e)
        if e.response.status_code == 400:
            jprint(e.response.json())
        raise
    return pandas.concat(map(pandas.read_csv, query_status['request_uri']))

    