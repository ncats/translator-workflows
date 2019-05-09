import sys
import shutil

pyptha = sys.executable.split('/')
pyptha[-2]= 'lib'
pypth='/'.join(pyptha) + '*/site-packages'

# Hack to get around problematic updating of distutils installed PyYAML and a slightly older pandas requiring a compatible numpy
shutil.rmtree(pypth + '/PyYAML*', ignore_errors=True)
shutil.rmtree(pypth + '/numpy*', ignore_errors=True)

sys.path.append("../mvp-module-library")
# Install pip requirements
!{sys.executable} -m pip install -r requirements.txt


from BioLink.biolink_client import BioLinkWrapper
import pandas as pd
from os import makedirs
from html3.html3 import XHTML


def output_file(tag, title, ext):
    basepath = "./Tidbit/" + tag
    filename = title.replace(" ", "_")
    filepath = basepath + "/" + filename + "." + ext
    makedirs(basepath, exist_ok=True)
    output = open(filepath, "w+")
    output.info = {'tag': tag, 'title': title}
    return output


def dump_html(output, body):
    title = output.info['title'] + " for " + output.info['tag']

    doc = XHTML()

    doc.head.title(title)
    doc.body.h1(title)
    doc.body.p(body.to_html())

    output.write(str(doc))


from Modules.Mod0_lookups import LookUp


def diseaseLookUp(input_disease_symbol, input_disease_mondo):
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
    return lu.input_object, disease_associated_genes, input_curie_set


input_disease_symbol = "FA"
input_disease_mondo = 'MONDO:0019391'

input_object, disease_associated_genes, input_curie_set = diseaseLookUp(input_disease_symbol, input_disease_mondo)

#  Echo to console
disease_associated_genes


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


def similarity(model, data, threshold, input_disease_symbol, module, title):
    # Initialize
    load_genes(model, data, threshold)
    model.load_associations()

    # Perform the comparison
    results = model.compute_similarity()

    # Process the results
    results_table = pd.DataFrame(results)
    results_table = results_table[
        ~results_table['hit_id'].isin(disease_associated_genes['hit_id'].tolist())].sort_values('score',
                                                                                                ascending=False)
    results_table['module'] = module

    # save the gene list to a file under the "Tidbit" subdirectory
    output = output_file(input_disease_symbol, title, "html")
    dump_html(output, results_table)
    output.close()

    return results_table


from Modules.Mod1A_functional_sim import FunctionalSimilarity

# Functinoal Simularity using Jaccard index threshold
func_sim_human = FunctionalSimilarity()
Mod1A_results = similarity( func_sim_human, input_curie_set, 0.75, input_disease_symbol, 'Mod1A', "Functionally Similar Genes" )

Mod1A_results



from Modules.Mod1B1_phenotype_similarity import PhenotypeSimilarity

# Phenotypic simulatiry using OwlSim calculation threshold
pheno_sim_human = PhenotypeSimilarity()
Mod1B_results = similarity( pheno_sim_human, input_curie_set, 0.50, input_disease_symbol, 'Mod1B', "Phenotypically Similar Genes" )

Mod1B_results



from Modules.StandardOutput import StandardOutput

def aggregrate_results(resultsA,resultsB):
    all_results = pd.concat([resultsA,resultsB])
    so = StandardOutput(results=all_results.to_dict(orient='records'), input_object=input_object)
    return so.output_object

std_api_response_json = aggregrate_results(Mod1A_results_human, Mod1B_results)

# Echo to console
std_api_response_json

import requests


def file_index(output, input_disease_symbol, input_disease_mondo, rtx_ui_url):
    title = "Results for " + input_disease_symbol + "[" + input_disease_mondo + "]

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


def publish_to_rtx(output, std_api_response_json, input_disease_symbol, title):
    # get the URL for these results displayed in the RTX UI
    RTX_UI_REQUEST_URL = "https://rtx.ncats.io/api/rtx/v1/response/process"
    to_post = {"options": ["Store", "ReturnResponseId"], "responses": [std_api_response_json]}
    rtx_ui_url = requests.post(RTX_UI_REQUEST_URL, json=to_post)

    # Write out a master index web page
    output = output_file(input_disease_symbol, "index", "html")
    write_file_index(output, rtx_ui_url)
    output.close()

    return rtx_ui_url


rtx_ui_url = publish_to_rtx(std_api_response_json)

print("Please visit the following website: https://rtx.ncats.io/?r=%s" % rtx_ui_url.json()['response_id'])
print("Please visit the following link to retrieve JSON results: https://rtx.ncats.io/api/rtx/v1/response/%s" %
      rtx_ui_url.json()['response_id'])

# Read a table of diseases and process
with open("diseases.tsv","r") as diseases:
    for entry in diseases.readlines():
        field = entry.split("\t")
        continue if field[1] == "Disease"
        
        input_disease_symbol = field[1]
        input_disease_mondo  = field[3]
        
        # process
        input_object, disease_associated_genes, input_curie_set = diseaseLookUp(input_disease_symbol, input_disease_mondo)
        
        # Functinoal Simularity using Jaccard index threshold
        func_sim_human = FunctionalSimilarity()
        Mod1A_results = similarity( func_sim_human, input_curie_set, 0.75, input_disease_symbol, 'Mod1A', "Functionally Similar Genes" )

        # Phenotypic simulatiry using OwlSim calculation threshold
        pheno_sim_human = PhenotypeSimilarity()
        Mod1B_results = similarity( pheno_sim_human, input_curie_set, 0.50, input_disease_symbol, 'Mod1B', "Phenotypically Similar Genes" )

        # Find Interacting Genes
        interactions_human = GeneInteractions()
        Mod1E_results = gene_interactions( interactions_human, input_curie_set, input_disease_symbol, 'Mod1E', "Gene Interactions" )
        
        std_api_response_json = aggregrate_results(Mod1A_results, Mod1B_results)
        publish_to_rtx( output, input_disease_symbol, input_disease_mondo, std_api_response_json )
