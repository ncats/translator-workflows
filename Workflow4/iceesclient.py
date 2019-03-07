import requests
import json
import argparse
requests.packages.urllib3.disable_warnings()

tabular_headers = {"Content-Type" : "application/json", "accept": "text/tabular"}
json_headers = {"Content-Type" : "application/json", "accept": "application/json"}

class DefineCohort ():
    def __init__(self):
        pass
    
    def make_cohort_definition(self, feature, value, operator):
        feature_variables = '{{"{0}": {{ "value": {1}, "operator": "{2}"}}}}'.format(feature, value, operator)
        return feature_variables
    
    def define_cohort_query(self, feature_variables, year=2010, table='patient', version='1.0.0'): # year, table, and version are hardcoded for now
        define_cohort_response = requests.post('https://icees.renci.org/{0}/{1}/{2}/cohort'.format(version, table, year), data=feature_variables, headers = json_headers, verify = False)               
        return define_cohort_response

    def run_define_cohort (self, feature, value, operator):
        feature_variables = self.make_cohort_definition(feature, value, operator)
        define_cohort_query = self.define_cohort_query(feature_variables)
        define_cohort_query_json = define_cohort_query.json()
        return define_cohort_query_json

class GetCohortDefinition():
    def __init__(self):
        pass
    
    def get_cohort_definition_query(self, cohort_id, year=2010, table='patient', version='1.0.0'):
        cohort_definition_response = requests.get('https://icees.renci.org/{0}/{1}/{2}/cohort/{3}'.format(version, table, year, cohort_id), headers = json_headers, verify = False)               
        return cohort_definition_response

    def run_get_cohort_definition(self, cohort_id):
        cohort_definition_query = self.get_cohort_definition_query(cohort_id)
        cohort_definition_query_json = cohort_definition_query.json()
        return cohort_definition_query_json
    
class GetFeatures():
    def __init__(self):
        pass

    def get_features_query(self, cohort_id, year=2010, table='patient', version='1.0.0'):
        features_response = requests.get('https://icees.renci.org/{0}/{1}/{2}/cohort/{3}/features'.format(version, table, year, cohort_id), headers=json_headers, verify=False)
        return features_response

    def run_get_features(self, cohort_id):
        features_query = self.get_features_query(cohort_id)
        features_query_json = features_query.json()
        return features_query_json

class FeatureAssociation():
    def __init__(self):
        pass

    def make_feature_association(self, feature_a, feature_a_operator, feature_a_value, feature_b, feature_b_operator, feature_b_value):
        feature_assoc_variables = '{{"feature_a":{{"{0}":{{"operator":"{1}","value":{2}}}}},"feature_b":{{"{3}":{{"operator":"{4}","value":{5}}}}}}}'.format(feature_a, feature_a_operator, feature_a_value, feature_b, feature_b_operator, feature_b_value)
        return feature_assoc_variables

    def feature_association_query(self, feature_assoc_variables, cohort_id, year=2010, table='patient', version='1.0.0'):
        feature_association_response = requests.post('https://icees.renci.org/{0}/{1}/{2}/cohort/{3}/feature_association'.format(version, table, year, cohort_id), data=feature_assoc_variables, headers=json_headers, verify=False)
        return feature_association_response

    def run_feature_association(self, feature_a, feature_a_operator, feature_a_value, feature_b, feature_b_operator, feature_b_value, cohort_id):
        feature_assoc_variables = self.make_feature_association(feature_a, feature_a_operator, feature_a_value, feature_b, feature_b_operator, feature_b_value)
        feature_assoc_query = self.feature_association_query(feature_assoc_variables, cohort_id)
        feature_assoc_query_json = feature_assoc_query.json()
        return feature_assoc_query_json

class AssociationToAllFeatures():
    def __init__(self):
        pass
    
    def make_association_to_all_features(self, feature, value, operator, maximum_p_value):
        feature_variable_and_p_value = '{{"feature":{{"{0}":{{"operator":"{1}","value":{2}}}}},"maximum_p_value":{3}}}'.format(feature, value, operator, maximum_p_value)
        return feature_variable_and_p_value

    def assocation_to_all_features_query(self, feature_variable_and_p_value, cohort_id, year=2010, table='patient', version='2.0.0'):
        assoc_to_all_features_response = requests.post('https://icees.renci.org/{0}/{1}/{2}/cohort/{3}/associations_to_all_features'.format(version, table, year, cohort_id), data=feature_variable_and_p_value, headers= json_headers, verify=False)
        return assoc_to_all_features_response

    def run_association_to_all_features(self, feature, value, operator, maximum_p_value, cohort_id):
        feature_variable_and_p_value = self.make_association_to_all_features(feature, value, operator, maximum_p_value)
        assoc_to_all_features_query = self.assocation_to_all_features_query(feature_variable_and_p_value, cohort_id)
        assoc_to_all_features_query_json = assoc_to_all_features_query.json()
        return assoc_to_all_features_query_json

class GetDictionary():
    def __init__(self):
        pass

    def get_dictionary_query(self, year=2010, table='patient', version='1.0.0'):
        dictionary_response = requests.get('https://icees.renci.org/{0}/{1}/{2}/cohort/dictionary'.format(version, table, year), headers = json_headers, verify = False) 
        return dictionary_response

    def run_get_dictionary(self):
        dictionary_query = self.get_dictionary_query()
        dictionary_query_json = dictionary_query.json()
        return dictionary_query_json


# You can use the work below to treat this module as a CLI utility. Currently, it is configured to accept inputs for and
# return values from the simplest input, "DefineCohort"... feel free to copy/fork and customize for your own purposes!

parser = argparse.ArgumentParser()
parser.add_argument("-ftr", "--feature", help="feature name")
parser.add_argument("-v", "--value", help="feature value")
parser.add_argument("-op", "--operator", help="feature operator")
args = parser.parse_args()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 3:
        icees_define_cohort = DefineCohort()
        output = icees_define_cohort.run_define_cohort(args.feature, args.value, args.operator)
        #if 'cohort_id' in str(output):
        print()
        print ('Cohort definition accepted')
        print(output['return value'])
        print()
    else:
        print("Expected script call is of the form: $python3 icees_caller.py -ftr <feature> -val <value> -op \<operator>")