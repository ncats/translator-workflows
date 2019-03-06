#!/usr/bin/python3

# This is a solution script for workflow #1 using results from 3(+) reasoning teams.
# Initially written by the Workflow 1 team at the Portland Hackathon (Fall 2018).d
# Adapted by Stephen Ramsey to run over multiple diseases, 2019.03.05.

#### Import some needed modules
import requests
import json
import sys

#### Workflow 1

num_robocop_results = 25
output_format="DENSE"

#### Set the base URL for the reasoner and its endpoint
XRAY_API_BASE_URL = 'https://rtx.ncats.io/api/rtx/v1'
xray_url_str = XRAY_API_BASE_URL + "/query"

ROBOCOP_API_BASE_URL = 'http://robokop.renci.org/api/'

annot_url_str = "https://rtx.ncats.io/api/rtx/v1/response/process"

#print("xray URL: " + xray_url_str)
#print("robocop mod3 URL: " + robocop_mod3_url_str)
#print("robocop mod3a URL: " + robocop_mod3a_url_str)

#### Set the input disease, change this value to test a new disease
input_disease = "DOID:14330"

def get_wf1_results_for_doid(doid: str):
    
################################################################
    # X-ray module 1: given a disease, find genetic conditions that share "representative phenotypes" in common

#### Create a dict of the request, specifying the query type and its parameters
    request = {"query_type_id": "Q10001", "terms": {"disease": doid}}
    #### Send the request to RTX and check the status
#    print("posting request to RTX")
    response_content = requests.post(xray_url_str, json=request, headers={'accept': 'application/json'})
    status_code = response_content.status_code
    assert status_code == 200 !=0, "Module 1 failed"
    module1_xray_results_json = response_content.json()
#    print('Module 1 completed successfully. ' + str(len(module1_xray_results_json)) + ' conditions with similar phenotypes found')
    #for result in module1_xray_results_json['result_list']:
    #        print(result['essence'])
    request = {"query_type_id": "Q55", "terms": {"disease": doid}}
    #### Send the request to RTX and check the status
#    print("posting request to RTX")
    response_content = requests.post(xray_url_str, json=request, headers={'accept': 'application/json'})
    status_code = response_content.status_code
    assert status_code == 200 !=0, "Module 2 failed"
    module2_xray_results_json = response_content.json()
    myResultSet = set()
    result_list = module2_xray_results_json.get('result_list', None)
    if result_list is not None:
        for result in module2_xray_results_json['result_list']:
            if 'row_data' in result:
                myResultSet.add((result['row_data'][2],result['row_data'][3]))
            #this is to resolve potential caching issues that cause results without row_data to be returned
            #Could use some cleanup to resolve the repetition
#    if(len(myResultSet)==0):
#        print("posting Q55 request to RTX")
    request = {"query_type_id": "Q55", "terms": {"disease": doid}, "bypass_cache": "true"}
    response_content = requests.post(xray_url_str, json=request, headers={'accept': 'application/json'})
    status_code = response_content.status_code
    assert status_code == 200 !=0, "Module 2 failed"
    module2_xray_results_json = response_content.json()
    result_list = module2_xray_results_json.get('result_list', None)
    if result_list is not None:
        for result in module2_xray_results_json['result_list']:
            if 'row_data' in result:
                myResultSet.add((result['row_data'][2],result['row_data'][3]))
#    print("Module 2 completed successfully")
#    print(str(len(myResultSet))+' drugs found')
    #for drug in myResultSet:
    #   print(drug)
    ################################################################
    # Gamma team module 3: agent-centric
    # Mod 3 un-lettered approach
    robocop_mod3_url_str = ROBOCOP_API_BASE_URL + "simple/quick/template/wf1mod3/%s/?max_results=%d&output_format=%s" % (doid, num_robocop_results,output_format)
    robocop_mod3a_url_str = ROBOCOP_API_BASE_URL + "simple/quick/template/wf1mod3_v2/%s/?max_results=%d&output_format=%s" % (doid, num_robocop_results,output_format)
    response_content = requests.get(robocop_mod3_url_str, json={}, headers={'accept': 'application/json'})
    status_code = response_content.status_code
    assert status_code == 200 !=0, "Module 3 failed"
    module3_robocop_results_json = response_content.json()
#    print("Module 3 completed successfully")
#    try:
#        print(str(len(module3_robocop_results_json['result_list']))+' related chemical substances found')
#    except:
#        print ("Module 3 found no related chemical substances")
        # Mod3a approach
    response_content = requests.get(robocop_mod3a_url_str, json={}, headers={'accept': 'application/json'})
    status_code = response_content.status_code
    assert status_code == 200 !=0 ,"Module 3a failed"
    module3a_robocop_results_json = response_content.json()
 #   print("Module 3a completed successfully")
  #  try:
  #      print(str(len(module3a_robocop_results_json['result_list']))+' related chemical substances found')
  #  except: 
  #      print("Module 3a found no related chemical substances")
    ################################################################
    # Orange team module 4+5: annotation and scoring
    # annotate the x-ray results
    to_post = {"options": ["AnnotateDrugs", "Store", "ReturnResponseId"], "responses": [module2_xray_results_json]}
    module2_xray_results_annot_json = requests.post(annot_url_str, json=to_post)
    # annotate gamma 3
    to_post = {"options": ["AnnotateDrugs", "Store", "ReturnResponseId"], "responses": [module3_robocop_results_json]}
    module3_robocop_results_annot_json = requests.post(annot_url_str, json=to_post)
    #annotate gamma 3a
    to_post = {"options": ["AnnotateDrugs", "Store", "ReturnResponseId"], "responses": [module3a_robocop_results_json]}
    module3a_robocop_results_annot_json = requests.post(annot_url_str, json=to_post)
    all_results = module2_xray_results_annot_json
    # merge results
    if module3_robocop_results_annot_json.json()['status']==200:
        to_post = {"options": ["AnnotateDrugs", "Store", "ReturnResponseId"], "responseURIs":[module2_xray_results_json['id']],"responses": [module3_robocop_results_json]}
        all_results = requests.post(annot_url_str, json=to_post)
    if module3a_robocop_results_annot_json.json()['status']==200:
        to_post = {"options": ["AnnotateDrugs", "Store", "ReturnResponseId"], "responseURIs":[module2_xray_results_json['id']],"responses": [module3a_robocop_results_json]}
        all_results = requests.post(annot_url_str, json=to_post)
#    print(all_results.json())
    if 200 != all_results.status_code:
        print("failure in call to RTX", file=sys.stderr)
        return [None, dict(), None]
    response_id = all_results.json()['response_id']
    res_url = 'https://rtx.ncats.io/api/rtx/v1/response/' + str(response_id)
    final_res = requests.get(res_url)
    return [res_url, final_res.json(), response_id]

doid_dict = {'DOID:2841': 'asthma',
                'DOID:9352': 'type 2 diabetes',
                'DOID:14330': 'Parkinson',
                'DOID:1936': 'atherosclerosis',
                'DOID:10652': 'Alzheimer',
                'DOID:0050427': 'XP',
                'DOID:13636': 'fanconi anemia',
                'DOID:3302': 'chordoma',
                'DOID:0050946': 'ARSACS',
                'DOID:0110858': 'PKD', 
                'DOID:9562': 'PCD',
                'DOID:0050524': 'MODY',
                'DOID:3087': 'gingivitis',
                'DOID:8566': 'HSV',
                'DOID:8622': 'measles',
                'DOID:1508': 'candidiasis',
                'DOID:12128': 'pica', 
                'OMIM:114900': 'carcinoid tumor',
                'OMIM:209900': 'Bardet-Biedel syndrome',
                'DOID:12132': 'Wegeners syndrome'}

for doid in doid_dict.keys():
    [res_url, res_json_for_doid, response_id] = get_wf1_results_for_doid(doid)
    web_url = "https://rtx.ncats.io/devLM/list.html?r=" + str(response_id)
    print(doid + "\t" + doid_dict[doid] + "\t" + res_url + "\t" + web_url)
    f = open(doid.replace(':', '_') + ".json", 'w')
    f.write(json.dumps(res_json_for_doid))
    f.close()
    f = open(doid.replace(':', '_') + "_abridged.json", 'w')
    res_list = []
    for result in res_json_for_doid['result_list']:
        conf = result['confidence']
        drug = result['essence']
        res_list.append({'conf': conf,
                         'drug': drug})
    f.write(json.dumps(res_list))
    f.close()
    f = open(doid.replace(':', '_') + "_results.html", 'w')
    f.write('<html>')
    f.write('<meta http-equiv="Refresh" Content="0;URL=' + web_url + '" />')
    f.write("</html>")
    f.close()
#    print(get_wf1_results_for_doid(input_disease))

      
