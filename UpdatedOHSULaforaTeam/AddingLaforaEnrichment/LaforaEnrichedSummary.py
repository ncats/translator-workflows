#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Written by OHSU Colleen Xu 6/6/19

Input: CSV output of the Descriptive Summary from main automation script Lafora_team_final_automation.py
       (desc_table.csv)
       Functional and Phenotypic Enrichment info from ShinyGOProcessing.py
       (FunctEnrichedLaforaOutput.csv, PhenoEnrichedLaforaOutput.csv)

Output: Descriptive Summary where long lists of shared GO terms (from shared_labels) has been replaced
        with short (3 or less) list of enriched terms. Note that the original ShinyGO files only contained
        the top 30 most enriched terms of each type of enrichment, so some output-input pairs with 
        functional/phenotypic similarity don't have associated enriched terms.

KNOWN BUG: 
There are "output gene-input gene" pairs that have support from Mod1E, but are below threshold/not supported
by Mod1A and Mod1B. These shouldn't have anything in the FunctAssociatedTerms and PhenoAssociatedTerms columns,
but this script can add info to those columns! This is because there isn't any filtering step (checking that 
there is a Functional or Phenotypic Similarity score before adding something to those columns). 
"""
import pandas as pd

pathDesc = "./desc_table.csv"
pathFunct = "./FunctEnrichedLaforaOutput.csv"
pathPheno = "./PhenoEnrichedLaforaOutput.csv"

## Descriptive Table
descTable = pd.read_csv(pathDesc)
descTable = descTable.drop(columns=['Unnamed: 0', 'Func_assoc_terms', 'Pheno_assoc_terms'])

functTable = pd.read_csv(pathFunct)
functTable = functTable.drop(columns=['Unnamed: 0'])
phenoTable = pd.read_csv(pathPheno)
phenoTable = phenoTable.drop(columns=['Unnamed: 0'])

functTable = functTable.rename(index=str, columns={"Output_Gene": "Output_gene", 
                                            "Input_Gene":"Input_gene",
                                            "FunctAssociatedTerms":"Func_assoc_terms"})

phenoTable = phenoTable.rename(index=str, columns={"Output_Gene": "Output_gene", 
                                            "Input_Gene":"Input_gene",
                                            "PhenoAssociatedTerms":"Pheno_assoc_terms"})

descTable = descTable.merge(functTable, how='left', on=["Output_gene", "Input_gene"])
descTable = descTable.merge(phenoTable, how='left', on=["Output_gene", "Input_gene"])

descTable = descTable.rename(index=str, columns={"Output_gene":"OutputGene",
                                                 "Input_gene":"InputGene",
                                                 "Func_sim_score":"FuncSimScore",
                                                 "Pheno_sim_score":"PhenoSimScore",
                                                 "Gene_Gene_hit":"InteractionFound",
                                                 "Func_assoc_terms":"FuncSharedTerms",
                                                 "Pheno_assoc_terms":"PhenoSharedTerms"})

##Read out table
descOut = "./EnrichedDescLaforaSummary.csv"
descTable.to_csv(descOut)
