#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 21:36:12 2019

@author: jay
"""
import pandas as pd

pathBrief = "./brief_table.csv"
pathDesc = "./sorted_desc_table.csv"
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

## re-sort in alphabetical order
## another idea, set an interaction equal to lowest threshold = 0.2. 
## then sort on the sum of all terms. 
## stuff with just interaction will be at the bottom
## stuff with interaction and another module will be pushed up
# descTable2 = descTable.sort_values(by="OutputGene", axis=0)

##Read out table
descOut = "./CXdescTable.csv"
descTable.to_csv(descOut)