# Uncomment when we need to debug
#import logging
#logging.basicConfig(level=logging.INFO)

from os import makedirs
from pathlib import Path
import argparse

import pandas as pd
from html3.html3 import XHTML

#############################################################
# First, before loading all our analysis modules, we need
# to tweak OntoBio to disable its @cachier cache. Our
# patched Ontobio has an 'ignore_cache' flag which may be
# overridden here before the rest of the system is loaded.
# We do this because cachier seems to introduce an odd system
# instability resulting in deep recursion on one method,
# creating new threads and consuming stack memory to the point
# of system resource exhaustion!  We conjecture that cachier
# caching is unnecessary since we read the pertinent ontology
# catalogs in just once into memory, for readonly reuse.
##############################################################
from ontobio.config import session
session.config.ignore_cache = True

# Now we can import the remainder of the modules (some which call Ontobio)
from Modules.Mod0_disease_gene_lookup import DiseaseAssociatedGeneSet
from Modules.Mod1A_functional_sim import FunctionalSimilarity
from Modules.Mod1B1_phenotype_similarity import PhenotypeSimilarity
from Modules.StandardOutput import StandardOutput
from Modules.Mod1E_interactions import GeneInteractions

_SCRIPTNAME='WF2_automation.py'

# Flag to control console output
_echo_to_console = False


# Data type of switch input is interpreted as a Boolean value
def set_console_echo(switch):
    global _echo_to_console
    _echo_to_console = switch


def output_file(tag, title, ext):

    # takes the tidbit directory that is relative to the current directory
    # parameterized across two functions so that it's made explicit without
    # over-encoding the paths within their constructor arguments (makes it easier to edit.)

    folder_name = tag.replace(" ", "_")
    tidbit_path = Path("Tidbit").relative_to(".") / folder_name

    filename = title.replace(" ", "_")
    output_file_path = tidbit_path / (filename + "." + ext)
    makedirs(tidbit_path, exist_ok=True)

    # Path objects compatible with file operations
    output = open(output_file_path, "w+")
    output.info = {'tag': tag, 'title': title}
    return output


def dump_html(output, body, columns=None):
    title = output.info['title'] + " for " + output.info['tag']

    doc = XHTML()

    doc.head.title(title)
    doc.body.h1(title)
    doc.body.p.text(body.to_html(escape=False, columns=columns), escape=False)

    output.write(str(doc))


def disease_gene_lookup(name, id):
    
    gene_set = DiseaseAssociatedGeneSet(name, id)

    # save the seed gene definition and gene list to a
    # file under the "Tidbit/<symbol>" subdirectory

    output = output_file(name, "Definition", "json")
    gene_set.echo_input_object(output)
    output.close()

    # save the gene list to a file under the "Tidbit" subdirectory
    df = gene_set.get_data_frame()

    # Dump HTML representation
    output = output_file(name, "Disease Associated Genes", "html")
    dump_html(output, df)
    output.close()

    # Dump JSON representation
    output = output_file(name, "Disease Associated Genes", "json")
    df.to_json(output)
    output.close()

    # genes to investigate
    return gene_set


STD_RESULT_COLUMNS = ['hit_id', 'hit_symbol', 'input_id', 'input_symbol', 'score']


def similarity(model, input_gene_set, threshold, module, title):

    # Subtle model-specific difference in gene set loading
    annotated_input_gene_set = model.load_gene_set(input_gene_set)

    # Perform the comparison on specified gene set
    results = model.compute_similarity(annotated_input_gene_set, threshold)

    # Process the results
    results_table = pd.DataFrame(results)
    results_table = \
        results_table[~results_table['hit_id'].
            isin(input_gene_set.get_data_frame()['hit_id'].
                 tolist())].sort_values('score', ascending=False)
    results_table['module'] = module

    # save the gene list to a file under the "Tidbit" subdirectory

    # Dump HTML representation
    output = output_file(input_gene_set.get_input_disease_name(), title, "html")
    dump_html(output, results_table, columns=STD_RESULT_COLUMNS)
    output.close()

    # Dump JSON representation
    output = output_file(input_gene_set.get_input_disease_name(), title, "json")
    results_table.to_json(output)
    output.close()

    return results_table


def gene_interactions(model, input_gene_set, module, title):

    # Subtle model-specific difference in gene set loading
    annotated_input_gene_set = GeneInteractions.load_gene_set(input_gene_set)

    results = model.get_interactions(annotated_input_gene_set)

    results_table = pd.DataFrame(results)

    counts = results_table['hit_symbol'].value_counts().rename_axis('unique_values').to_frame('counts').reset_index()
    high_counts = counts[counts['counts'] > 12]['unique_values'].tolist()

    final_results_table = pd.DataFrame(results_table[results_table['hit_symbol'].isin(high_counts)])

    final_results_table['module'] = module

    # save the gene list to a file under the "Tidbit" subdirectory

    # Dump HTML representation
    output = output_file(input_gene_set.get_input_disease_name(), title, "html")
    dump_html(output, final_results_table.head())
    output.close()

    # Dump JSON representation
    output = output_file(input_gene_set.get_input_disease_name(), title, "json")
    # dumping the whole table in the JSON? or should I just dump the head?
    final_results_table.to_json(output)
    output.close()

    return final_results_table


def aggregate_results(results_a, results_b, input_object_id):
    all_results = pd.concat([results_a, results_b])
    so = StandardOutput(results=all_results.to_dict(orient='records'), input_object_id=input_object_id)
    return so.output_object


if __name__ == '__main__':

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        prog=_SCRIPTNAME, formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='NCATS Translator Workflow 2 Command Line Script'
    )

    parser.add_argument('-v', '--verbose', help='echo script output verbosely to console', action='store_true')

    disease_query = parser.add_mutually_exclusive_group(required=True)

    # single disease input specification as a 2-tuple
    disease_query.add_argument('-d', '--disease',
                        help="""
Comma delimited 'name, MONDO identifier'
2-tuple string of a single disease to analyze"""
                        )

    # disease input as a list
    disease_query.add_argument('-l', '--diseaseTable',
                        help="""
name of a tab delimited text file table of disease names - in the first column - 
and associated MONDO identifiers - in the second column"""
                        )

    parser.add_argument('-f', '--functionalThreshold',
                        type=float, default=0.75, help='value of Functional Similarity threshold')

    parser.add_argument('-p', '--phenotypeThreshold',
                        type=float, default=0.35, help='value of Phenotype Similarity threshold')

    args = parser.parse_args()

    print("\nRunning the "+_SCRIPTNAME+" script...")

    if args.verbose:
        print("Echoing results verbosely to the console!\n")
        set_console_echo(True)

    # read in the diseases to analyze
    disease_list = []

    if args.disease:
        disease_name, mondo_id = args.disease.split(',')
        disease_name = disease_name.strip()
        print("\nSingle disease specified:\t" + disease_name + "(" + mondo_id + "):\n")
        disease_list.append((disease_name, mondo_id))

    elif args.diseaseTable:

        disease_table_filename = args.diseaseTable
        print("Table of diseases specified in file:\t\t" + disease_table_filename)

        with open(disease_table_filename, "r") as diseases:
            for entry in diseases.readlines():

                field = entry.split("\t")

                # Skip the header
                if str(field[0]).lower() == "disease":
                    continue

                # The first field is assumed to be the gene name or symbol, the second field, the MONDO identifier
                disease_name = field[0]
                disease_name = disease_name.strip()

                mondo_id = field[1]

                disease_list.append((disease_name, mondo_id))

    functional_threshold = args.functionalThreshold
    print("Functional Similarity Threshold:\t" + str(functional_threshold))

    phenotype_threshold = args.phenotypeThreshold
    print("Phenotype Similarity Threshold: \t"+str(phenotype_threshold))

    print("\nLoading source ontology and annotation...")

    # Ontology Catalogs only need to be initialized once!

    # Functional similarity using Jaccard index threshold
    # Called once, creating this object triggers
    # its initialization with GO ontology and annotation
    func_sim_human = FunctionalSimilarity('human')

    # Phenotype similarity using OwlSim calculation threshold
    # Called once, creating this object triggers
    # its initialization with GO ontology and annotation
    pheno_sim_human = PhenotypeSimilarity('human')

    # Gene interactions curated in the Biolink (Monarch) resource
    interactions_human = GeneInteractions()

    # diseases.tsv is assumed to be a tab delimited
    # file of diseases named (column 0) with their MONDO identifiers (column 1)
    # The optional header should read 'Disease' in the first column
    for disease_name, mondo_id in disease_list:

        print("\nProcessing '" + disease_name + "(" + mondo_id + "):\n")

        disease_associated_gene_set = \
            disease_gene_lookup(
                disease_name,
                mondo_id
            )

        if _echo_to_console:
            print(
                "\nDisease Associated Input Gene Set for '" +
                disease_name + "(" + mondo_id + "):\n")
            print(disease_associated_gene_set.get_data_frame().to_string())

        Mod1A_results = \
            similarity(
                func_sim_human,
                disease_associated_gene_set,
                functional_threshold,
                'Mod1A',
                'Functionally Similar Genes'
            )

        if _echo_to_console:
            print("\nMod1A Results for '" +
                  disease_name + "(" + mondo_id + "):\n")
            print(Mod1A_results.to_string(columns=STD_RESULT_COLUMNS))

        Mod1B_results = \
            similarity(
                pheno_sim_human,
                disease_associated_gene_set,
                phenotype_threshold,
                'Mod1B',
                'Phenotypic Similar Genes'
            )

        if _echo_to_console:
            print("\nMod1B Results for '" +
                  disease_name + "(" + mondo_id + "):\n")
            print(Mod1B_results.to_string(columns=STD_RESULT_COLUMNS))

        # Find Interacting Genes from Monarch data
        Mod1E_results = \
            gene_interactions(
                interactions_human,
                disease_associated_gene_set,
                'Mod1E',
                "Gene Interactions"
            )

        if _echo_to_console:
            print("\nMod1E Results for '" +
                  disease_name + "(" + mondo_id + "):\n")
            print(Mod1E_results.head().to_string(columns=STD_RESULT_COLUMNS))

        # Not sure how useful this step is: to be further reviewed
        # (carried over from the Jupyter notebook)
        std_api_response_json = \
            aggregate_results(
                Mod1A_results,
                Mod1B_results,
                disease_associated_gene_set.get_input_object_id()
            )

        # Echo to console
        if _echo_to_console:
            print("\nAggregate Mod1A and Mod1B Results as JSON for '" +
                  disease_name + "(" + mondo_id + "):\n")
            print(std_api_response_json)

    print("\nWF2 Processing complete!")
