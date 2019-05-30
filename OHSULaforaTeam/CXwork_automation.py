## Reorganized by Megan Grout (mgrout81) 20190516
## Import libraries
import sys
import shutil
from os import makedirs
import requests
import pandas as pd
from html3.html3 import XHTML

# Adjust path to find custom modules
if '/' in sys.executable:
    pyptha = sys.executable.split('/')
    pyptha[-2]= 'lib'
else:
    pyptha = sys.executable.split('\\')
    pyptha[-2] = 'lib'
pypth='/'.join(pyptha) + '*/site-packages'

# Hack to get around problematic updating of distutils installed PyYAML and a 
# slightly older pandas requiring a compatible numpy
shutil.rmtree(pypth + '/PyYAML*', ignore_errors=True)
shutil.rmtree(pypth + '/numpy*', ignore_errors=True)

sys.path.append("../mvp-module-library")
# Install pip requirements
#!{sys.executable} -m pip install -r requirements.txt

from BioLink.biolink_client import BioLinkWrapper
from Modules.Mod0_lookups import LookUp
from Modules.Mod1A_functional_sim import FunctionalSimilarity
from Modules.Mod1B1_phenotype_similarity import PhenotypeSimilarity
from Modules.Mod1E_interactions import GeneInteractions
from Modules.StandardOutput import StandardOutput


"""
This function takes in three strings, representing the tag, title, and file extension
for an output file, and returns an _io.TextIOWrapper object.
"""
def output_file(tag, title, ext):
    # print("output_file",type(tag), type(title),type(ext))
    basepath = "./Tidbit/" + tag
    filename = title.replace(" ", "_")
    filepath = basepath + "/" + filename + "." + ext
    makedirs(basepath, exist_ok=True)
    output = open(filepath, "w+")
    output.info = {'tag': tag, 'title': title}
    # print("output_file",type(output))
    return output

"""
This function takes in an _io.TextIOWrapper object and a Pandas df and writes
the information to file.
"""
def dump_html(output, body):
    # print("dump_html", type(output),type(body))
    title = output.info['title'] + " for " + output.info['tag']

    doc = XHTML()

    doc.head.title(title)
    doc.body.h1(title)
    doc.body.p(body.to_html())

    output.write(str(doc))
    return None

""" 
This method takes strings representing the disease of interest's symbol and MONDO
code and returns a dictionary, a Pandas df, and a list representing information
about the disease. CX: using Mod0
""" 
def diseaseLookUp(input_disease_symbol, input_disease_mondo):
    # print("diseaseLoopUp",type(input_disease_symbol), type(input_disease_mondo))
    # workflow input is a disease identifier
    lu = LookUp()  

    input_object = {
        'input': input_disease_mondo,
        'parameters': {
            'taxon': 'human',
            'threshold': None,
        },
    }

    lu.load_input_object(input_object=input_object)

    # get genes associated with disease from Biolink
    disease_associated_genes = lu.disease_geneset_lookup()

    # create list of gene curies for downstream module input
    input_curie_set = disease_associated_genes[['hit_id', 'hit_symbol']].to_dict(orient='records')

    # show the disease associated genes
    disease_associated_genes['modules'] = 'Mod0'

    # save the seed gene definition and gene list to a
    # file under the "Tidbit/<symbol>" subdirectory

    output = output_file(input_disease_symbol, "Definition", "json")
    lu.echo_input_object(output)
    output.close()

    output = output_file(input_disease_symbol, "Disease Associated Genes", "html")
    dump_html(output, disease_associated_genes)
    output.close()

    # genes to investigate
    # print("diseaseLookUP output",type(lu.input_object),type(disease_associated_genes),type(input_curie_set))
    return lu.input_object, disease_associated_genes, input_curie_set

"""
This function takes in a Modules.Mod1A_functional_sim.FunctionalSimilarity
object representing the gene model, the data in a list, and a float threshold
value and returns the model with genes loaded in.
"""
def load_genes(model, data, threshold):
    # Module specification
    inputParameters = {
        'input': data,
        'parameters': {
            'taxon': 'human',
            'threshold': threshold,
        },
    }

    # Load the computation parameters
    model.load_input_object(inputParameters)
    model.load_gene_set()
    return model

"""
This function is used for Mod1A and Mod1B. It takes in a model (Mod1A or Mod1B),
a list of data, a float threshold value, strings
to represent the input disease symbol, module, and title, and a Pandas df of
disease associated genes.
"""
def similarity(model, data, threshold, input_disease_symbol, module, title, disease_associated_genes):
    # Initialize
    load_genes(model, data, threshold)
    model.load_associations()

    ## Perform the comparison: CX MOD of compute_similarity function (from generic_similarity.py) to return an extra entry in each dictionary. 
    ## common_terms is a list of the GO terms in common between the input and output
    results = model.compute_similarity()

    # Process the results
    ## CX: EPM2A has no functional annotation in Monarch, which is why it has no results in Module 1A
    results_table = pd.DataFrame(results)
    results_table = results_table[
        ~results_table['hit_id'].isin(disease_associated_genes['hit_id'].tolist())].sort_values('score', ascending=False)
    # results_table = results_table.sort_values('score', ascending=False)                                  
    results_table['module'] = module
    ## CX: reordering columns
    results_table = results_table[['hit_id', 'hit_symbol', 'input_id', 'input_symbol', 'score', 'module', 'commonTerm_ids', 'commonTerm_labels']]
    # CX: Commented out. save the gene list to a file under the "Tidbit" subdirectory
    # output = output_file(input_disease_symbol, title, "html")
    # dump_html(output, results_table)
    # output.close()
    return results_table

"""
This function takes in two Pandas df objects and a dictionary
"""
def aggregrate_results(resultsA,resultsB, input_object):
    all_results = pd.concat([resultsA,resultsB])
    so = StandardOutput(results=all_results.to_dict(orient='records'), 
        input_object=input_object)
    return so.output_object


"""
This function writes an output file
"""
def file_index(output, input_disease_symbol, input_disease_mondo, rtx_ui_url):
    title = "Results for " + input_disease_symbol + "[" + input_disease_mondo + "]"

    doc = XHTML()

    doc.head.title(title)
    doc.body.h1(title)
    ul = body.ul
    ul.li.a("Input Disease Details", href="Definition.json")
    ul.li.a("Disease Associated Genes", href="Disease_Associated_Genes.html")
    ul.li.a("Functionally Similar Genes", href="Functionally_Similar_Genes.html")
    ul.li.a("Phenotypically Similar Genes", href="Phenotypically_Similar_Genes.html")
    ul.li.a("Gene Interactions", href="Gene_Interactions.html")
    doc.body.p.a("RTX UI Display of Details", href="https://rtx.ncats.io/?r=%s" % rtx_ui_url.json()['response_id'])
    doc.body.p.a("Reasoner API formatted JSON results",
                 href="https://rtx.ncats.io/api/rtx/v1/response/%s" % rtx_ui_url.json()['response_id'])

    output.write(doc)
    return None

def main():
    # Set disease of interest: Lafora Disease 
    input_disease_symbol = "LD"
    input_disease_mondo = 'MONDO:0009697'
    
    # CX: from Mod0
    ## Lookup disease and get data available on it
    input_object, disease_associated_genes, input_curie_set = diseaseLookUp(input_disease_symbol, input_disease_mondo)

    ## print objects from Mod0
    print("Mod0 results: input_object")
    print(input_object)
    print("Mod0 results: disease associated genes")
    print(disease_associated_genes)
    print("Mod0 results: input curie set")
    print(input_curie_set)
    ## Echo to console
    # disease_associated_genes

    ## Functional Similarity using Jaccard index threshold
    ## Originally set to 0.75 for Threshold. Lowering it (with Marcin's advice)
    # 0.25 gave me 563 results.  
    func_sim_human = FunctionalSimilarity()
    Mod1A_results = similarity( func_sim_human, input_curie_set, 0.4, input_disease_symbol, 'Mod1A', "Functionally Similar Genes",disease_associated_genes )
    ## merging columns, creating lists of the inputs and sums of the scores
    ## CX note: obviously it would be nice to do this all at once. the apply(list) only worked on one column at a time. aggregate only accepts a limited number of functions
    Mod1A_part1 = Mod1A_results.groupby(['hit_symbol','hit_id'])['input_symbol'].apply(list).reset_index()
    Mod1A_part2 = Mod1A_results.groupby(['hit_symbol','hit_id'])['input_id'].apply(list).reset_index()
    Mod1A_part3 = Mod1A_results.groupby(['hit_symbol','hit_id']).aggregate({'score': 'count'}).rename(index=str, columns={'score':'FunctionalSimilarity'})
    
    ## Merge the parts together!
    Mod1A_final = Mod1A_part1.merge(Mod1A_part2, on=['hit_symbol', 'hit_id'])
    ## Another merge, and sort in descending order of number of interactions, ascending alphabetical order
    Mod1A_final = Mod1A_final.merge(Mod1A_part3, on=['hit_symbol', 'hit_id']).sort_values(by=['FunctionalSimilarity','hit_symbol'], ascending=[False, True])
    
    Mod1A_basicSummary = Mod1A_final.filter(items=['hit_symbol', 'input_symbol', 'FunctionalSimilarity']).rename(index=str, columns={'hit_symbol': 'Output_Gene', 'input_symbol':'Input_Gene'})
    print("Mod1A results: threshold 0.4")
    print(Mod1A_basicSummary.to_string())
    # csvPath1A = "./Mod1Aoutput.csv"
    # Mod1A_results.to_csv(csvPath1A, sep="\t")

    ## Phenotypic simulatiry using OwlSim calculation threshold
    ## Originally set to 0.50 for Threshold. Lowering it (with Marcin's advice)
    pheno_sim_human = PhenotypeSimilarity()
    Mod1B_results = similarity( pheno_sim_human, input_curie_set, 0.25, input_disease_symbol, 'Mod1B', "Phenotypically Similar Genes",disease_associated_genes )
    ## merging columns, creating lists of the inputs and sums of the scores
    ## CX note: obviously it would be nice to do this all at once. the apply(list) only worked on one column at a time. aggregate only accepts a limited number of functions
    Mod1B_part1 = Mod1B_results.groupby(['hit_symbol','hit_id'])['input_symbol'].apply(list).reset_index()
    Mod1B_part2 = Mod1B_results.groupby(['hit_symbol','hit_id'])['input_id'].apply(list).reset_index()
    Mod1B_part3 = Mod1B_results.groupby(['hit_symbol','hit_id']).aggregate({'score': 'count'}).rename(index=str, columns={'score':'PhenotypicSimilarity'})

    ## Merge the parts together!
    Mod1B_final = Mod1B_part1.merge(Mod1B_part2, on=['hit_symbol', 'hit_id'])
    ## Another merge, and sort in descending order of number of interactions, ascending alphabetical order
    Mod1B_final = Mod1B_final.merge(Mod1B_part3, on=['hit_symbol', 'hit_id']).sort_values(by=['PhenotypicSimilarity','hit_symbol'], ascending=[False, True])

    Mod1B_basicSummary = Mod1B_final.filter(items=['hit_symbol', 'input_symbol', 'PhenotypicSimilarity']).rename(index=str, columns={'hit_symbol': 'Output_Gene', 'input_symbol':'Input_Gene'})


    print("Mod1B results: threshold 0.25")
    print(Mod1B_basicSummary.to_string())
    # csvPath1B = "./Mod1Boutput.csv"
    # Mod1B_results.to_csv(csvPath1B, sep="\t")

    ## CX: Mod1E code from WF2_FA_human.py file
    ## I didn't make it into a function since I couldn't figure that out
    
    interactions_human = GeneInteractions()
    mod1E_input_object_human = {
        'input': input_curie_set,
        'parameters': {
        'taxon': 'human',
        'threshold': None,
        },
    }
    interactions_human.load_input_object(mod1E_input_object_human)
    interactions_human.load_gene_set()
    rawMod1Eresults = pd.DataFrame(interactions_human.get_interactions())
    # rawMod1Eresults = pd.DataFrame(rawMod1Eresults)
     
    ## adjust the number in high counts to get output for genes with lots of interactions
    # counts = rawMod1Eresults['hit_symbol'].value_counts().rename_axis('unique_values').to_frame('counts').reset_index()
    ## For Lafora, make the number below 2, to get the genes that interact with both input genes
    # high_counts = counts[counts['counts'] >= 12]['unique_values'].tolist()
    # rawMod1Eresults= pd.DataFrame(rawMod1Eresults[rawMod1Eresults['hit_symbol'].isin(high_counts)])
    
    ## optional: add module name to it. 
    # rawMod1Eresults['module']='Mod1E'
    ## the highest results are the input genes...remove them
    rawMod1Eresults = rawMod1Eresults[~rawMod1Eresults['hit_symbol'].isin(disease_associated_genes['hit_symbol'].tolist())]
    
    ## merging columns, creating lists of the inputs and sums of the scores
    ## CX note: obviously it would be nice to do this all at once. the apply(list) only worked on one column at a time. aggregate only accepts a limited number of functions
    Mod1E_part1 = rawMod1Eresults.groupby(['hit_symbol','hit_id'])['input_symbol'].apply(list).reset_index()
    Mod1E_part2 = rawMod1Eresults.groupby(['hit_symbol','hit_id'])['input_id'].apply(list).reset_index()    
    Mod1E_part3 = rawMod1Eresults.groupby(['hit_symbol','hit_id']).aggregate({'score': 'sum'}).rename(index=str, columns={'score':'Interactions'})
    ## Merge the parts together!
    Mod1E_final = Mod1E_part1.merge(Mod1E_part2, on=['hit_symbol', 'hit_id'])
    ## Another merge, and sort in descending order of number of interactions, ascending alphabetical order
    Mod1E_final = Mod1E_final.merge(Mod1E_part3, on=['hit_symbol', 'hit_id']).sort_values(by=['Interactions','hit_symbol'], ascending=[False, True])
    
    Mod1E_basicSummary = Mod1E_final.filter(items=['hit_symbol', 'input_symbol', 'Interactions']).rename(index=str, columns={'hit_symbol': 'Output_Gene', 'input_symbol':'Input_Gene'})
    print("Mod1E results:")
    print(Mod1E_basicSummary.to_string())
    # print(Mod1E_part2.to_string())
    # print(Mod1E_part3.to_string())

    # std_api_response_json = aggregrate_results(Mod1A_results, Mod1B_results, input_object)
    # Echo to console
    # std_api_response_json

if __name__ == "__main__":
    main()



#def publish_to_rtx(output, std_api_response_json, input_disease_symbol, title):
    # get the URL for these results displayed in the RTX UI
#    RTX_UI_REQUEST_URL = "https://rtx.ncats.io/api/rtx/v1/response/process"
#    to_post = {"options": ["Store", "ReturnResponseId"], "responses": [std_api_response_json]}
#    rtx_ui_url = requests.post(RTX_UI_REQUEST_URL, json=to_post)

    # Write out a master index web page
#    output = output_file(input_disease_symbol, "index", "html")
#    write_file_index(output, rtx_ui_url)
#    output.close()

#    return rtx_ui_url


#rtx_ui_url = publish_to_rtx(output, std_api_response_json,input_disease_mondo, "input_disease_mondo" )

#print("Please visit the following website: https://rtx.ncats.io/?r=%s" % rtx_ui_url.json()['response_id'])
#print("Please visit the following link to retrieve JSON results: https://rtx.ncats.io/api/rtx/v1/response/%s" %
#      rtx_ui_url.json()['response_id'])


# Read a table of diseases and process
#with open("diseases.tsv","r") as diseases:
#    for entry in diseases.readlines():
#        field = entry.split("\t")
#        if field[1] == "Disease":
#	        continue
        
#        input_disease_symbol = field[1]
#        input_disease_mondo  = field[3]
        
        # process
#        input_object, disease_associated_genes, input_curie_set = diseaseLookUp(input_disease_symbol, input_disease_mondo)
        
        # Functinoal Simularity using Jaccard index threshold
#        func_sim_human = FunctionalSimilarity()
#        Mod1A_results = similarity( func_sim_human, input_curie_set, 0.75, input_disease_symbol, 'Mod1A', "Functionally Similar Genes" )

        # Phenotypic simulatiry using OwlSim calculation threshold
#        pheno_sim_human = PhenotypeSimilarity()
#        Mod1B_results = similarity( pheno_sim_human, input_curie_set, 0.50, input_disease_symbol, 'Mod1B', "Phenotypically Similar Genes" )

        # Find Interacting Genes
#        interactions_human = GeneInteractions()
#        Mod1E_results = gene_interactions( interactions_human, input_curie_set, input_disease_symbol, 'Mod1E', "Gene Interactions" )
        
#        std_api_response_json = aggregrate_results(Mod1A_results, Mod1B_results)
#        publish_to_rtx( output, input_disease_symbol, input_disease_mondo, "input_disease_mondo" )
