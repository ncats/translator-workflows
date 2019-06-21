from os import makedirs
from pathlib import Path

import argparse

import pandas as pd
from html3.html3 import XHTML

from Modules.Mod0_disease_gene_lookup import DiseaseAssociatedGeneSet
from Modules.Mod1A_functional_sim import FunctionalSimilarity
from Modules.Mod1B1_phenotype_similarity import PhenotypeSimilarity
from Modules.Mod1E_interactions import GeneInteractions
from Modules.StandardOutput import StandardOutput

try:
	import _pickle as cPickle
except:
	import cPickle

_SCRIPTNAME='WF2_automation.py'

# Flag to control console output
_echo_to_console = False


# Data type of switch input is interpreted as a Boolean value
def setConsoleEcho(switch):
    global _echo_to_console
    _echo_to_console=switch


def output_file(tag, title, ext):

    # takes the tidbit directory that is relative to the current directory
    # parameterized across two functions so that it's made explicit without
    # over-encoding the paths within their constructor arguments (makes it easier to edit.)

    foldername = tag.replace(" ", "_")
    tidbitPath = Path("Tidbit").relative_to(".") / foldername

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


def diseaseGeneLookUp(disease_name, mondo_id):
    gene_set = DiseaseAssociatedGeneSet(disease_name, mondo_id)

    # save the seed gene definition and gene list to a
    # file under the "Tidbit/<symbol>" subdirectory

    output = output_file(disease_name, "Definition", "json")
    gene_set.echo_input_object(output)
    output.close()

    # save the gene list to a file under the "Tidbit" subdirectory
    output = output_file(disease_name, "Disease Associated Genes", "html")
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

    # save the gene list to a file under the "Tidbit" subdirectory
    output = output_file(input_gene_set.get_input_disease_name(), title, "html")
    dump_html(output, results_table)
    output.close()

    return results_table


def aggregate_results(resultsA, resultsB, input_object_id):
    all_results = pd.concat([resultsA, resultsB])
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
        setConsoleEcho(True)

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

    # diseases.tsv is assumed to be a tab delimited
    # file of diseases named (column 0) with their MONDO identifiers (column 1)
    # The optional header should read 'Disease' in the first column
    for disease_name, mondo_id in disease_list:

        print("\nProcessing '" + disease_name + "(" + mondo_id + "):\n")

        disease_associated_gene_set = \
            diseaseGeneLookUp(
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

        if _echo_to_console:
            print("\nMod1A Results for '" +
                  disease_name + "(" + mondo_id + "):\n")
            print(Mod1A_basicSummary.to_string())   ## CX: changed to see my summary


## JG: Mod1A now saving both things
    with open('data/mod1a_raw.picky','wb') as fh:
        cPickle.dump(Mod1A_results ,fh)






        Mod1B_results = \
            similarity(
                pheno_sim_human,
                disease_associated_gene_set,
                phenotype_threshold,
                'Mod1B',
                'Phenotypically Similar Genes'
            )

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

        if _echo_to_console:
            print("\nMod1B Results for '" +
                  disease_name + "(" + mondo_id + "):\n")
            print(Mod1B_basicSummary.to_string())  ## CX: changed to see my summary

    ## JG: Mod1B now saving both things
    with open('data/mod1b_raw.picky','wb') as fh:
        cPickle.dump(Mod1B_results, fh)






        ## CX: Mod1E code from WF2_FA_human.py file
        ## I didn't make it into a function since I couldn't figure that out    
        ## I made input for Mod1E lafora specific since otherwise I would need to change more stuff
        LaforaGenes = [{'hit_id': 'HGNC:21576', 'hit_symbol': 'NHLRC1'}, {'hit_id': 'HGNC:3413', 'hit_symbol': 'EPM2A'}]
        interactions_human = GeneInteractions()
        mod1E_input_object_human = {
            'input': LaforaGenes,
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
        rawMod1Eresults = rawMod1Eresults[~rawMod1Eresults['hit_symbol'].isin(disease_associated_gene_set.get_data_frame()['hit_symbol'].tolist())]
    
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

## JG: Mod1E now saving both things
    with open('data/mod1e_raw.picky','wb') as fh:
        cPickle.dump(rawMod1Eresults ,fh)






        #std_api_response_json = \
        #    aggregate_results(
        #        Mod1A_results,
        #        Mod1B_results,
        #        disease_associated_gene_set.get_input_object_id()
        #    )

        # Echo to console
        #if _echo_to_console:
        #    print("\nAggregate Mod1A and Mod1B Results as JSON for '" +
        #          disease_name + "(" + mondo_id + "):\n")
        #    print(std_api_response_json)

    print("\nWF2 Processing complete!")
# Python 2 vs Python 3 Pickle:
