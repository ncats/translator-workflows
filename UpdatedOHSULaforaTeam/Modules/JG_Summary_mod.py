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
        # stores the dataframe from all the raw module output
        self.raw_module_data = dict()

        self.brief_table = pd.DataFrame()
        self.desc_table = pd.DataFrame(
        	columns = ['Output_gene','Input_gene'])
        # Stores the naming conventions for the brief table.
        self.module_names = dict()


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


        # JG: Attempting to use expressions to find '_score' and summing across the hits to get the 'sum' col
        # this allows for extendable coding.
        self.desc_table['sum'] = self.desc_table.filter(regex=("_score$")).sum(axis=1)

        # Sort desc_table by the the sum of the similarity scores, or just the one if no second score present
        # This is not too elegant
        # Basically, keep trying to create a sum column until it works
        #try:
        #    self.desc_table['sum'] = self.desc_table['Func_sim_score'] + self.desc_table['Pheno_sim_score']
        #except KeyError:
        #    self.desc_table['sum'] = self.desc_table['Func_sim_score']
        #except:
        #    self.desc_table['sum'] = self.desc_table['Pheno_sim_score']


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
        

        ## JG: editing the below code to be extensible for any module! added the self.module_names dictionary
        for term in self.module_names.keys():

            # Search for the title then replace with the dictionary created in the addmod___ method
            if term in list(self.brief_table.columns.values):
                self.brief_table = self.brief_table.drop(columns=term)
                self.brief_table = self.brief_table.rename(
                    index=str, columns = self.module_names[term])

        # Again, not elegant
        # Now we want to drop one of the columns with identical data (pheno hit counts
        # or fun hit counts), but doing so by name of column, so have the if ctl 
        # structure to handle fun vs pheno data
        # Remember, brief table COULD only have mod1a data, or just mod1b, or both
        # Also want to rename remaining func or pheno columns with appropriate name
        # for table printing!
        #if 'Func_assoc_terms' in list(self.brief_table.columns.values):
        #    self.brief_table = self.brief_table.drop(columns='Func_assoc_terms')
        #    self.brief_table = self.brief_table.rename(
        #        index=str, columns = {'Func_sim_score':'Func_sim_input_gene_ct'})
        #if 'Pheno_assoc_terms' in self.brief_table.columns.values:
        #    self.brief_table = self.brief_table.drop(columns='Pheno_assoc_terms')
        #    self.brief_table = self.brief_table.rename(
        #        index=str, columns = {'Pheno_sim_score':'Pheno_sim_input_gene_ct'})




        # sort by the total number of input genes for each output gene
        # Make total hits but its at the end so reorder the table 
        self.brief_table['Total_hits'] =  self.brief_table.drop('Input_gene', axis=1).sum(axis=1)

        # Send the total hits to the second columns
        cols = self.brief_table.columns.tolist()
        

        cols.insert(0, cols.pop(cols.index('Input_gene')))
        cols.insert(1, cols.pop(cols.index('Total_hits')))
        #print(cols)
        # Reorder!
        self.brief_table = self.brief_table.reindex(columns=cols)
        # Now sort
        self.brief_table = self.brief_table.sort_values(['Total_hits'],ascending =False)



    # This function takes in the Module1A results and updates both tables
    def add1A(self, mod1a_results):

        # Immediately store raw data
        self.raw_module_data['mod1A'] = mod1a_results

        """ Add to desc_table """
        ## Initalize the naming paradigm for the module and for the brief table. 
        self.module_names['Func_assoc_terms'] = {'Func_sim_score':'Func_sim_input_gene_ct'}

        # drop irrelevant columns
        mod1a_processed = mod1a_results.drop(columns=['hit_id','input_id','shared_terms','module'])
        
        # drop duplicates in input
        mod1a_processed = mod1a_processed.drop_duplicates(subset=['input_symbol','hit_symbol'])
        
        # rename columns to match desc_table desired output column names
        mod1a_processed = mod1a_processed.rename(index = str, columns = {'hit_symbol':'Output_gene','input_symbol':'Input_gene','score':'Func_sim_score','shared_labels':'Func_assoc_terms'})
        
        #print(mod1a_processed.to_string())
        # Recast GO terms as a list, so we can do sorting later
        mod1a_processed.Func_assoc_terms = mod1a_processed.Func_assoc_terms.astype(str)
        
        # Update descriptive table
        self.build_desc_table(mod1a_processed)

        ### Add to brief table ###
        # Update brief table
        self.build_brief_table()
        

    # This function takes in the Module1B results and updates both tables
    def add1B(self, mod1b_results):    
        ## Imediately store output
        self.raw_module_data['mod1B'] = mod1b_results

        ### Add to desc_table ###
        self.module_names['Pheno_assoc_terms'] = {'Pheno_sim_score':'Pheno_sim_input_gene_ct'}


        # drop irrelevant columns
        mod1b_processed = mod1b_results.drop(columns=['hit_id','input_id','shared_terms','module'])
        
        # drop duplicates in input
        mod1b_processed = mod1b_processed.drop_duplicates(subset=['input_symbol','hit_symbol'])
        

        # rename columns to match desired desc_table output column names
        mod1b_processed = mod1b_processed.rename(index = str, columns = {'hit_symbol':'Output_gene','input_symbol':'Input_gene','score':'Pheno_sim_score','shared_labels':'Pheno_assoc_terms'})
        

        #### send to desc_table builder here ####
        mod1b_processed.Pheno_assoc_terms = mod1b_processed.Pheno_assoc_terms.astype(str)
        

        # Update descriptive table
        self.build_desc_table(mod1b_processed)
    
        # Update brief table
        self.build_brief_table()


    # This function does do anything yet, but the idea is
    # This function takes in the Module1E results and updates both tables
    def add1E(self, mod1e_results):
        self.raw_module_data['mod1E'] = mod1e_results


        # drop irrelevant columns
        mod1e_processed = mod1e_results.drop(columns=['hit_id','input_id'])
        
        # drop duplicates in input
        mod1e_processed = mod1e_processed.drop_duplicates(subset=['input_symbol','hit_symbol'])
        

        # rename columns to match desired desc_table output column names
        mod1e_processed = mod1e_processed.rename(index = str, columns = {'hit_symbol':'Output_gene','input_symbol':'Input_gene','score':'Gene_Gene_hit'})
        
        # Update descriptive table
        self.build_desc_table(mod1e_processed)

        # Update brief table
        self.build_brief_table()

    # This function shows the current modules loaded into the object
    def show_mods(self):
        print(self.raw_module_data.keys())
        return None

    # This function returns a dictionary of the raw pandas data 
    def return_raw_output(self):
        return self.raw_module_data


    # This function prints the brief table to console
    def show_brief(self):
        print(self.brief_table.to_string())
        

     # This function returns the brief table
    def get_brief(self):
        return self.brief_table

    # This function prints the descriptive table to console
    def show_descriptive(self):
        print(self.desc_table.to_string())

    # This function retunrs the descriptive table 
    def get_descriptive(self):
        return self.desc_table

    # This function returns both the brief and descriptive tables to console
    def get_all(self):
        return self.get_brief() ,self.get_descriptive()

    def show_all(self):
        self.show_brief()
        self.show_descriptive()
        

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
