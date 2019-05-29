from os import makedirs
from pathlib import Path

import pandas as pd
from html3.html3 import XHTML

from Modules.Mod0_disease_gene_lookup import DiseaseAssociatedGeneSet
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
    doc.body.p.text(body.to_html(escape=False), escape=False)

    output.write(str(doc))


def diseaseGeneLookUp(input_disease_symbol, input_disease_mondo):
    gene_set = DiseaseAssociatedGeneSet(input_disease_symbol, input_disease_mondo)

    # save the seed gene definition and gene list to a
    # file under the "Tidbit/<symbol>" subdirectory

    output = output_file(input_disease_symbol, "Definition", "json")
    gene_set.echo_input_object(output)
    output.close()

    if _echo_to_console:
        print("\nDisease Associated Input Gene Set:\n")
        print(gene_set.get_data_frame().to_string())

        # save the gene list to a file under the "Tidbit" subdirectory
        output = output_file(input_disease_symbol, "Disease Associated Genes", "html")
        dump_html(output, gene_set.get_data_frame())
        output.close()

    # genes to investigate
    return gene_set


def similarity(model, input_gene_set, threshold, label, title):
    # Subtle model-specific difference in gene set loading??
    annotated_input_gene_set = model.load_gene_set(input_gene_set)

    # Perform the comparison on specified gene set
    results = model.compute_similarity(annotated_input_gene_set, threshold)

    # Process the results
    results_table = pd.DataFrame(results)
    results_table = \
        results_table[~results_table['hit_id'].
            isin(input_gene_set.get_data_frame()['hit_id'].
                 tolist())].sort_values('score', ascending=False)
    results_table['module'] = label

    if _echo_to_console:
        # save the gene list to a file under the "Tidbit" subdirectory
        output = output_file(input_gene_set.get_input_disease_symbol(), title, "html")
        dump_html(output, results_table)
        output.close()

    return results_table


def aggregrate_results(resultsA, resultsB, input_object_id):
    all_results = pd.concat([resultsA, resultsB])
    so = StandardOutput(results=all_results.to_dict(orient='records'), input_object_id=input_object_id)
    return so.output_object


if __name__ == '__main__':
    # Module functions run as a sample query using Fanconi Anemia

    input_disease_symbol = "FA"
    input_disease_mondo = 'MONDO:0019391'

    disease_associated_gene_set = \
        diseaseGeneLookUp(
            input_disease_symbol,
            input_disease_mondo
        )

    # Functional similarity using Jaccard index threshold
    # Called once, creating this object triggers
    # its initialization with GO ontology and annotation
    func_sim_human = FunctionalSimilarity('human')

    Mod1A_results = \
        similarity(
            func_sim_human,
            disease_associated_gene_set,
            0.75,
            'Mod1A',
            "Functionally Similar Genes"
        )

    # Trigger the garbage collection of FunctionalSimilarity()?
    func_sim_human = None

    print(Mod1A_results.to_string())

    # Phenotype similarity using OwlSim calculation threshold
    # Called once, creating this object triggers
    # its initialization with GO ontology and annotation
    pheno_sim_human = PhenotypeSimilarity('human')

    Mod1B_results = \
        similarity(
            pheno_sim_human,
            disease_associated_gene_set,
            0.35,
            'Mod1B',
            "Phenotypically Similar Genes"
        )

    # Trigger the garbage collection of PhenotypeSimilarity()?
    pheno_sim_human = None

    print(Mod1B_results.to_string())

    std_api_response_json = \
        aggregrate_results(Mod1A_results,
                           Mod1B_results,
                           disease_associated_gene_set.get_input_object_id()
                           )

    # Echo to console
    print(std_api_response_json)
