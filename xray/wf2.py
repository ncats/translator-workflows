#!/usr/bin/python3

# wf2.py: a simple script to use a WF2-like approach to generate a list of potential drug targets for a disease
# It returns a list of proteins that are connected to the disease, and that are connected to a phenotype
# that is connected to the disease. Output is JSON to stdout.

# Written by: @stephenaramsey at the winter hackathon for Translator, 2019.03.07

import requests
import neo4j
import json
import getpass

password = getpass.getpass("Please enter the password for accessing the RTX database: ")

driver = neo4j.GraphDatabase.driver('bolt://rtx.ncats.io:7687', auth=neo4j.basic_auth("neo4j", password))

session = driver.session()

disease_doid = 'DOID:1936'  # atherosclerosis

## module 1:  get list of proteins involved in <disease>
statement_result = session.run("match (n:protein)-[r]-(m:disease {id: '" + disease_doid + "'}) return n.id")
uniprot_list = [item['n.id'] for item in statement_result]

## module 2:  get list of phenotypic_features involved in <disease>
statement_result = session.run("match (n:phenotypic_feature)-[r]-(m:disease {id: '" + disease_doid + "'}) return n.id")
phenotype_list = [item['n.id'] for item in statement_result]

## go through each phenotype and get list of genes assoc with the phenotype
phenotype_proteins = set()
for phenotype in phenotype_list:
    statement_result = session.run("match (n:protein)-[r]-(m:phenotypic_feature {id: '" + phenotype + "'}) return n.id")
    phenotype_proteins.update([item['n.id'] for item in statement_result])

final_protein_ids = set(uniprot_list) & phenotype_proteins

## get annotated info for these protein IDs
res_list = []
for protein_id in final_protein_ids:
    statement_result = session.run("match (n:protein {id: '" + protein_id + "'}) return properties(n)")
    record = statement_result.single()
    res_dict = dict()
#    print(record)
    res_list += [record.value(key='properties(n)')]
#    for key in record.keys():
#        if key == "properties(n)":
#            print(record[key])
#            res_list += [record[key]]
#    res_list += record.value(key='properties(n)')
print(json.dumps(res_list))






                        
