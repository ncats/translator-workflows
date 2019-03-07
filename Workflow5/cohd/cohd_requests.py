# This module defines helper functions for calling the COHD REST API

import requests
import pandas as pd
import numpy as np


# COHD API server
server = 'http://cohd.io/api'  

# ######################################################################
# Utility functions
# ######################################################################

# Convert JSON results to Pandas DataFrame
def json_to_df(results):
    # convert COHD's JSON response to Pandas dataframe
    return pd.DataFrame(results['results'])

# ######################################################################
# COHD OMOP functions
# ######################################################################

# Find concepts by name
def find_concept(concept_name, dataset_id=None, domain=None, min_count=1):
    url = f'{server}/omop/findConceptIDs'
    
    # Params
    params = {
        'q': concept_name,
        'min_count': min_count
    }
    if dataset_id is not None:
        params['dataset_id'] = dataset_id
    if domain is not None:
        params['domain'] = domain
        
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 7:
        # re-order the columns so that it displays in a more logical order
        df = df[['concept_id', 'concept_name', 'domain_id', 'concept_class_id', 
                 'vocabulary_id', 'concept_code', 'concept_count']]
    return df

# Get concept definitions from concept ID
def concept(concept_ids):   
    url = f'{server}/omop/concepts'
    
    # Convert list of concept IDs to a comma-delimited string
    concept_ids_string = ','.join([str(x) for x in concept_ids])
    
    params = {'q': concept_ids_string}
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 6:
        # re-order the columns so that it displays in a more logical order
        df = df[['concept_id', 'concept_name', 'domain_id', 'concept_class_id', 'vocabulary_id', 'concept_code']]
    return df

# Get ancestors of a concept
def concept_ancestors(concept_id, dataset_id=None, vocabulary_id=None, concept_class_id=None):
    url = f'{server}/omop/conceptAncestors'
    
    # Params
    params = {
        'concept_id': concept_id,
    }
    if dataset_id is not None:
        params['dataset_id'] = dataset_id
    if vocabulary_id is not None:
        params['vocabulary_id'] = vocabulary_id
    if concept_class_id is not None:
        params['concept_class_id'] = concept_class_id
        
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 10:
        # re-order the columns so that it displays in a more logical order
        df = df[['ancestor_concept_id', 'concept_name', 'domain_id', 'vocabulary_id', 'concept_class_id', 
                 'concept_code', 'standard_concept', 'concept_count', 'max_levels_of_separation', 
                 'min_levels_of_separation']]
    return df

# Get descendants of a concept
def concept_descendants(concept_id, dataset_id=None, vocabulary_id=None, concept_class_id=None):
    url = f'{server}/omop/conceptDescendants'
    
    # Params
    params = {
        'concept_id': concept_id,
    }
    if dataset_id is not None:
        params['dataset_id'] = dataset_id
    if vocabulary_id is not None:
        params['vocabulary_id'] = vocabulary_id
    if concept_class_id is not None:
        params['concept_class_id'] = concept_class_id
        
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 10:
        # re-order the columns so that it displays in a more logical order
        df = df[['descendant_concept_id', 'concept_name', 'domain_id', 'vocabulary_id', 'concept_class_id', 
                 'concept_code', 'standard_concept', 'concept_count', 'max_levels_of_separation', 
                 'min_levels_of_separation']]
    return df

# Get a list of OMOP vocabularies
def vocabularies():
    url = f'{server}/omop/vocabularies'
    json = requests.get(url).json()
    df = json_to_df(json)
    return df

# Map from non-standard OMOP concepts to standard OMOP concepts
def map_to_standard_concept_id(concept_code, vocabulary_id=None):
    url = f'{server}/omop/mapToStandardConceptID'
    
    # Params
    params = {'concept_code': concept_code}
    if vocabulary_id is not None:
        params['vocabulary_id'] = vocabulary_id
        
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 7:
        # re-order the columns so that it displays in a more logical order
        df = df[['source_concept_id', 'source_vocabulary_id', 'source_concept_code', 'source_concept_name', 
                 'standard_concept_id', 'standard_concept_name', 'standard_domain_id']]
    return df

# Reverse-map from standard OMOP concepts to non-standard OMOP concepts
def map_from_standard_concept_id(concept_id, vocabulary_id=None):
    url = f'{server}/omop/mapFromStandardConceptID'
    
    # Params
    params = {'concept_id': concept_id}
    if vocabulary_id is not None:
        params['vocabulary_id'] = vocabulary_id
        
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 7:
        # re-order the columns so that it displays in a more logical order
        df = df[['concept_id', 'concept_name', 'domain_id', 'concept_class_id', 
                 'vocabulary_id', 'concept_code', 'standard_concept']]
    return df

# Cross-reference a concept (CURIE) from an external ontology to OMOP (concept ID)
def xref_to_omop(curie, distance=None, local=False, recommend=False):
    url = f'{server}/omop/xrefToOMOP'
    
    # Params
    params = {
      'curie': curie,
      'local': local,
      'recommend': recommend
    }
    if distance is not None:
        params['distance'] = distance
        
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 10:
        # re-order the columns so that it displays in a more logical order
        df = df[['source_oxo_id', 'source_oxo_label', 'intermediate_oxo_id', 'intermediate_oxo_label', 
                'omop_standard_concept_id', 'omop_concept_name', 'omop_domain_id', 'omop_distance', 'total_distance']]
    return df

# Cross-reference a concept from OMOP (concept ID) to an external ontology (CURIE)
def xref_from_omop(concept_id, mapping_targets=None, distance=None, local=False, recommend=False):
    url = f'{server}/omop/xrefFromOMOP'
    
    # Params
    params = {
      'concept_id': concept_id,
      'local': local,
      'recommend': recommend
    }
    if mapping_targets is not None:
        params['mapping_targets'] = mapping_targets
    if distance is not None:
        params['distance'] = distance
        
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 15:
        # re-order the columns so that it displays in a more logical order
        df = df[['source_omop_concept_id', 'source_omop_concept_name', 'source_omop_vocabulary_id', 
                 'source_omop_concept_code', 'intermediate_omop_concept_id', 'intermediate_omop_concept_name',
                 'intermediate_omop_vocabulary_id', 'intermediate_omop_concept_code', 'intermediate_oxo_curie',
                 'intermediate_oxo_label', 'target_curie', 'target_label', 'omop_distance',
                 'oxo_distance', 'total_distance']]
    return df

# ######################################################################
# COHD metadata functions
# ######################################################################

# Get descriptions of the available data sets
def datasets():
    url = f'{server}/metadata/datasets'
    json = requests.get(url).json()
    df = json_to_df(json)
    
    if len(df.columns) == 3:
        # re-order the columns so that it displays in a more logical order
        df = df[['dataset_id', 'dataset_name', 'dataset_description']]
    return df

# Get the number of concepts in each domain
def domain_counts(dataset_id=None):
    url = f'{server}/metadata/domainCounts'
    
    # Optional params
    params = {}
    if dataset_id is not None:
        params['dataset_id'] = dataset_id
        
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 3:
        # re-order the columns so that it displays in a more logical order
        df = df[['dataset_id', 'domain_id', 'count']]
    return df

# Get the number of concept-pairs in each domain-paired
def domain_pair_counts(dataset_id=None):
    url = f'{server}/metadata/domainPairCounts'
    
    # Optional params
    params = {}
    if dataset_id is not None:
        params['dataset_id'] = dataset_id
        
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 4:
        # re-order the columns so that it displays in a more logical order
        df = df[['dataset_id', 'domain_id_1', 'domain_id_2', 'count']]
    return df

# Get the number of patients in the data set
def patient_count(dataset_id=None):
    url = f'{server}/metadata/patientCount'
    
    # Optional params
    params = {}
    if dataset_id is not None:
        params['dataset_id'] = dataset_id
    
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 2:
        # re-order the columns so that it displays in a more logical order
        df = df[['dataset_id', 'count']]
    return df    

# ######################################################################    
# COHD Clinical Frequency functions
# ######################################################################

# Get the single-concept frequency for a concept or list of single concepts
def concept_frequency(concept_ids, dataset_id=None):
    url = f'{server}/frequencies/singleConceptFreq'
    
    # Convert list of concept IDs to a comma-delimited string
    concept_ids_string = ','.join([str(x) for x in concept_ids])
    
    # Params
    params = {'q': concept_ids_string}
    if dataset_id is not None:
        params['dataset_id'] = dataset_id
        
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 4:
        # re-order the columns so that it displays in a more logical order
        df = df[['dataset_id', 'concept_id', 'concept_count', 'concept_frequency']]
    return df

# Get the most frequent concepts (optionally: in a given domain)
def most_frequent_concepts(limit, dataset_id=None, domain_id=None):
    url = f'{server}/frequencies/mostFrequentConcepts'
    
    # Params
    params = {'q': limit}
    if dataset_id is not None:
        params['dataset_id'] = dataset_id
    if domain_id is not None:
        params['domain'] = domain_id
        
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 6:
        df = df[['dataset_id', 'concept_id', 'concept_name', 'domain_id', 'concept_count', 'concept_frequency']]
    return df

# Get the co-occurrence frequency of the pair of concepts
def paired_concepts_frequency(concept_id_1, concept_id_2, dataset_id=None):
    url = f'{server}/frequencies/pairedConceptFreq'
    
    # Params
    params = {'q': f'{concept_id_1!s},{concept_id_2!s}'}
    if dataset_id is not None:
        params['dataset_id'] = dataset_id
        
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 5:
        df = df[['dataset_id', 'concept_id_1', 'concept_id_2', 'concept_count', 'concept_frequency']]
    return df

# Get the co-occurrence frequency between the given concept and all other concepts
def associated_concepts_freq(concept_id, dataset_id=None):
    url = f'{server}/frequencies/associatedConceptFreq'
    
    # Params
    params = {'q': concept_id}
    if dataset_id is not None:
        params['dataset_id'] = dataset_id
        
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 7:
        df = df[['dataset_id', 'concept_id', 'associated_concept_id', 'associated_concept_name',
                'associated_domain_id', 'concept_count', 'concept_frequency']]
    return df

# Get the co-occurrence frequency between the given concept and all other concepts   in the given domain  
def associated_concept_domain_freq(concept_id, domain_id, dataset_id=None):
    url = f'{server}/frequencies/associatedConceptDomainFreq'
    
    # Params
    params = {
        'concept_id': concept_id, 
        'domain': domain_id
    }
    if dataset_id is not None:
        params['dataset_id'] = dataset_id
        
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 7:
        df = df[['dataset_id', 'concept_id', 'associated_concept_id', 'associated_concept_name',
                'associated_domain_id', 'concept_count', 'concept_frequency']]
    return df

# ######################################################################
# COHD Concept Associations 
# ######################################################################

# Get the chi-square association analysis between:
# 1) a concept and all other concepts (specify concept_id_1 only)
# 2) a concept and all other concepts in a given domain (specify concept_id_1 and domain_id)
# 3) a pair of concepts (concept_id_1 and concept_id_2)
def chi_square(concept_id_1, concept_id_2=None, domain_id=None, dataset_id=None):
    url = f'{server}/association/chiSquare'
    
    # Params
    params = {'concept_id_1': concept_id_1}
    if concept_id_2 is not None:
        params['concept_id_2'] = concept_id_2
    if domain_id is not None:
        params['domain'] = domain_id
    if dataset_id is not None:
        params['dataset_id'] = dataset_id
        
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 5:
        df = df[['dataset_id', 'concept_id_1', 'concept_id_2', 'chi_square', 'p-value']]
    elif len(df.columns) == 7:
        df = df[['dataset_id', 'concept_id_1', 'concept_id_2', 'concept_2_name', 
                 'concept_2_domain', 'chi_square', 'p-value']]
    return df

# Get the observed-to-expected frequency association analysis between:
# 1) a concept and all other concepts (specify concept_id_1 only)
# 2) a concept and all other concepts in a given domain (specify concept_id_1 and domain_id)
# 3) a pair of concepts (concept_id_1 and concept_id_2)
def obs_exp_ratio(concept_id_1, concept_id_2=None, domain_id=None, dataset_id=None):
    url = f'{server}/association/obsExpRatio'
    
    # Params
    params = {'concept_id_1': concept_id_1}
    if concept_id_2 is not None:
        params['concept_id_2'] = concept_id_2
    if domain_id is not None:
        params['domain'] = domain_id
    if dataset_id is not None:
        params['dataset_id'] = dataset_id
        
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 6:
        df = df[['dataset_id', 'concept_id_1', 'concept_id_2', 'observed_count', 'expected_count', 'ln_ratio']]
    elif len(df.columns) == 8:
        df = df[['dataset_id', 'concept_id_1', 'concept_id_2', 'concept_2_name', 
                 'concept_2_domain', 'observed_count', 'expected_count', 'ln_ratio']]
    return df

# Get the relative frequency association analysis between:
# 1) a concept and all other concepts (specify concept_id_1 only)
# 2) a concept and all other concepts in a given domain (specify concept_id_1 and domain_id)
# 3) a pair of concepts (concept_id_1 and concept_id_2)
def relative_frequency(concept_id_1, concept_id_2=None, domain_id=None, dataset_id=None):
    url = f'{server}/association/relativeFrequency'
    
    # Params
    params = {'concept_id_1': concept_id_1}
    if concept_id_2 is not None:
        params['concept_id_2'] = concept_id_2
    if domain_id is not None:
        params['domain'] = domain_id
    if dataset_id is not None:
        params['dataset_id'] = dataset_id
        
    json = requests.get(url, params).json()
    df = json_to_df(json)
    if len(df.columns) == 6:
        df = df[['dataset_id', 'concept_id_1', 'concept_id_2', 'concept_pair_count', 
                 'concept_2_count', 'relative_frequency']]
    elif len(df.columns) == 8:
        df = df[['dataset_id', 'concept_id_1', 'concept_id_2', 'concept_2_name', 'concept_2_domain', 
                 'concept_pair_count', 'concept_2_count', 'relative_frequency']]
    return df