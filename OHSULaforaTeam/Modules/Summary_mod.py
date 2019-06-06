# Written 20190603 by Megan Grout (groutm@ohsu.edu)
# using Python 3
#
# The purpose of this script is to create an class to
# aggregate and display summary data from the automated
# modules.

# Import libraries
import sys
import pandas as pd
import numpy as numpy

# Main class
class Summary_mod(object):

    # Initializing function
    def __init__(self):
        self.brief_table = pd.DataFrame(
            columns = ['Output_gene','Input_gene','Func_sim_input_gene_ct','Pheno_sim_input_gene_ct'])
        self.desc_table = pd.DataFrame(
        	columns = ['Output_gene','Input_gene'])


    # This method builds the descriptive table pandas dataframe. It returns nothing
    # and is given a pandas dataframe of an individual module's results.
    def build_desc_table(self, mod_results):
        # Combine exisiting desc_table with mod pre-processed data
        # If desc_table is empty, it will only hold mod info and columns pertaining to particular mod
        # If desc_table already holds, say, mod1b info, will add mod1a-specific columns, too
        # This command also combines lines from desc_table and input mod such that if a particular
        # input-output gene relationship already exists in table, we effectively new info 
        # to the row that already contains some info on this input-output gene relationship
        self.desc_table = pd.merge(self.desc_table, mod_results, on=['Input_gene','Output_gene'], how='outer')

        # Sort desc_table by the the sum of the similarity scores, or just the one if no second score present
        # This is not too elegant
        # Basically, keep trying to create a sum column until it works
        try:
            self.desc_table['sum'] = self.desc_table['Func_sim_score'] + self.desc_table['Pheno_sim_score']
        except KeyError:
            self.desc_table['sum'] = self.desc_table['Func_sim_score']
        except:
            self.desc_table['sum'] = self.desc_table['Pheno_sim_score']
        # Now do the sorting
        self.desc_table = self.desc_table.sort_values(['sum'], ascending = False)
        # Now drop the column used to sort
        self.desc_table = self.desc_table.drop(columns="sum")
    
    # This method builds the brief table pandas dataframe. it returns nothing and
    # takes no parameters.
    def build_brief_table(self):
        # Create table that has unique Output_gene entries in first column
        # subsequent columns count # non-null entries for that output_gene,
        # for any given column
        # so we would have output_genes in first column, and subsequent columns
        # are COUNTS (not sums) for func and pheno sim scores and go terms
        # func sim scores/go terms should be the same counts
        # pheno sim scores/go terms should be the same counts
        self.brief_table = self.desc_table.groupby(['Output_gene']).aggregate('count')
        
        # Again, not elegant
        # Now we want to drop one of the columns with identical data (pheno hit counts
        # or fun hit counts), but doing so by name of column, so have the if ctl 
        # structure to handle fun vs pheno data
        # Remember, brief table COULD only have mod1a data, or just mod1b, or both
        # Also want to rename remaining func or pheno columns with appropriate name
        # for table printing!
        if 'Func_assoc_terms' in list(self.brief_table.columns.values):
            self.brief_table = self.brief_table.drop(columns='Func_assoc_terms')
            self.brief_table = self.brief_table.rename(
                index=str, columns = {'Func_sim_score':'Func_sim_input_gene_ct'})
        if 'Pheno_assoc_terms' in self.brief_table.columns.values:
            self.brief_table = self.brief_table.drop(columns='Pheno_assoc_terms')
            self.brief_table = self.brief_table.rename(
                index=str, columns = {'Pheno_sim_score':'Pheno_sim_input_gene_ct'})

        # sort by the total number of input genes for each output gene
        self.brief_table = self.brief_table.sort_values(['Input_gene'],ascending =False)


    # This function takes in the Module1A results and updates both tables
    def add1A(self, mod1a_results):
        """ Add to desc_table """
        # drop irrelevant columns
        mod1a_processed = mod1a_results.drop(columns=['hit_id','input_id','commonTerm_ids','module'])
        
        # drop duplicates in input
        mod1a_processed = mod1a_processed.drop_duplicates(subset=['input_symbol','hit_symbol'])
        
        # rename columns to match desc_table desired output column names
        mod1a_processed = mod1a_processed.rename(index = str, columns = {'hit_symbol':'Output_gene','input_symbol':'Input_gene','score':'Func_sim_score','commonTerm_labels':'Func_assoc_terms'})
        
        # Recast GO terms as a list, so we can do sorting later
        mod1a_processed.Func_assoc_terms = mod1a_processed.Func_assoc_terms.astype(str)
        
        # Update descriptive table
        self.build_desc_table(mod1a_processed)

        ### Add to brief table ###
        # Update brief table
        self.build_brief_table()
        

    # This function takes in the Module1B results and updates both tables
    def add1B(self, mod1b_results):    
        ### Add to desc_table ###
        # drop irrelevant columns
        mod1b_processed = mod1b_results.drop(columns=['hit_id','input_id','commonTerm_ids','module'])
        
        # drop duplicates in input
        mod1b_processed = mod1b_processed.drop_duplicates(subset=['input_symbol','hit_symbol'])
        
        # rename columns to match desired desc_table output column names
        mod1b_processed = mod1b_processed.rename(index = str, columns = {'hit_symbol':'Output_gene','input_symbol':'Input_gene','score':'Pheno_sim_score','commonTerm_labels':'Pheno_assoc_terms'})
        
        #### send to desc_table builder here ####
        mod1b_processed.Pheno_assoc_terms = mod1b_processed.Pheno_assoc_terms.astype(str)
        
        # Update descriptive table
        self.build_desc_table(mod1b_processed)
    
        # Update brief table
        self.build_brief_table()


    # This function does do anything yet, but the idea is
    # This function takes in the Module1E results and updates both tables
    def add1E(self, mod1e_results):
        return None

    # This function prints the brief table to console
    def get_brief(self):
        print(self.brief_table.to_string())

    # This function prints the descriptive table to console
    def get_descriptive(self):
        print(self.desc_table.to_string())

    # This function prints both the brief and descriptive tables to console
    def get_all(self):
        print("here")
        self.get_brief()
        self.get_descriptive()

    # This function writes the brief table to csv
    # An optional parameter specifies the filename
    def write_brief(self, outname ="brief_table.csv"):
        self.brief_table.to_csv(outname)

    # This function writes the descriptive table to csv
    # An optional parameter specifies the filename
    def write_descriptive(self, outname="desc_table.csv"):
        self.desc_table.to_csv(outname)

    # This function writes both the brief and descriptive tables to csv
    def write_all(self):
        self.write_brief()
        self.write_descriptive()

    # This function writes the brief table to json
    # An optional parameter specifies the filename
    def write_json_brief(self, outname="brief_table.json"):
        self.brief_table.to_json(outname)

    # This function writes the descriptive table to json
    # An optional parameter specifies the filename
    def write_json_desc(self, outname="desc_table.json"):
        self.desc_table.to_json(outname)

    # This function writes both the brief and descriptive tables to json
    def write_json(self):
        self.write_json_brief()
        self.write_json_desc()
