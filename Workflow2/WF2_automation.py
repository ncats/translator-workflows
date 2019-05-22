from os import makedirs
from pathlib import Path

import pandas as pd
from html3.html3 import XHTML

from Modules.Mod0_lookups import LookUp
from Modules.Mod1A_functional_sim import FunctionalSimilarity
from Modules.Mod1B1_phenotype_similarity import PhenotypeSimilarity
from Modules.StandardOutput import StandardOutput

# Flag to control console output
_echo_to_console = True

# Data type of switch input is interpreted as a Boolean value
def setConsoleEcho(switch):
    _echo_to_console = switch

def output_file(tag, title, ext):
    # takes the tidbit directory that is relative to the current directory
    # parameterized across two functions so that it's made explicit without
    # over-encoding the paths within their constructor arguments (makes it easier to edit.)
    tidbitPath = Path("Tidbit").relative_to(".") / tag

    filename = title.replace(" ", "_")
    outputFilePath = tidbitPath / (filename + "." + ext)
    makedirs(tidbitPath, exist_ok=True)

    # Path objects compatible with file operations
    output = open(outputFilePath, "w+")
    output.info = {'tag': tag, 'title': title}
    return output


def dump_html(output, body):
    title = output.info['title'] + " for " + output.info['tag']

    doc = XHTML()

    doc.head.title(title)
    doc.body.h1(title)
    doc.body.p(body.to_html())

    output.write(str(doc))


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

    if _echo_to_console:
        # save the gene list to a file under the "Tidbit" subdirectory
        output = output_file(input_disease_symbol, "Disease Associated Genes", "html")
        dump_html(output, disease_associated_genes)
        output.close()

    # genes to investigate
    return lu.input_object, disease_associated_genes, input_curie_set


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


def similarity(input_gene_set, model, data, threshold, input_disease_symbol, module, title):
    # Initialize
    load_genes(model, data, threshold)
    model.load_associations()

    # Perform the comparison
    results = model.compute_similarity()

    # Process the results
    results_table = pd.DataFrame(results)
    results_table = results_table[
        ~results_table['hit_id'].isin(input_gene_set['hit_id'].tolist())].sort_values('score',
                                                                                                ascending=False)
    results_table['module'] = module

    if _echo_to_console:
        # save the gene list to a file under the "Tidbit" subdirectory
        output = output_file(input_disease_symbol, title, "html")
        dump_html(output, results_table)
        output.close()

    return results_table


def aggregrate_results(resultsA,resultsB):
    all_results = pd.concat([resultsA,resultsB])
    so = StandardOutput(results=all_results.to_dict(orient='records'), input_object=input_object)
    return so.output_object


if __name__ == '__main__':

    # Module functions run as a sample query using Fanconi Anemia

    input_disease_symbol = "FA"
    input_disease_mondo = 'MONDO:0019391'

    input_object, disease_associated_genes, input_curie_set = diseaseLookUp(input_disease_symbol, input_disease_mondo)

    #  Echo to console
    print(disease_associated_genes.to_string())

    # Functional Simularity using Jaccard index threshold
    func_sim_human = FunctionalSimilarity()
    Mod1A_results = similarity(disease_associated_genes, func_sim_human, input_curie_set, 0.75, input_disease_symbol, 'Mod1A', "Functionally Similar Genes" )

    print(Mod1A_results.to_string())

    # Phenotypic simularity using OwlSim calculation threshold
    pheno_sim_human = PhenotypeSimilarity()
    Mod1B_results = similarity(disease_associated_genes, pheno_sim_human, input_curie_set, 0.035, input_disease_symbol, 'Mod1B', "Phenotypically Similar Genes" )

    print(Mod1B_results.to_string())

    std_api_response_json = aggregrate_results(Mod1A_results, Mod1B_results)

    # Echo to console
    print(std_api_response_json)
