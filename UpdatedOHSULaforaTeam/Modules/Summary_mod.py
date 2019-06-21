# Written 20190603 by Megan Grout (groutm@ohsu.edu) ; Jacob Gutierrez (gutierja@ohsu.edu) 6/10/19 ; Colleen Xu (xco@ohsu.edu) 6/10/19 
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
    def __init__(self, disease='NA', mondo_id='MONDO:XXXXXXX'):

        # Store the disease names and mondo id
        self.disease = disease
        self.mondo_id = mondo_id

        # Store current modules being used
        self.current_mods = list()

        # stores the dataframe from all the raw module output
        # The keys are 'mod1A' , 'mod1B' etc how every extensible. 
        # This allows for retrival of raw data later on 
        self.raw_module_data = dict()

        # Stores basic summary tables for each individual modules 
        self.module_summaries = dict()

        # Dataframes for data across modules 
        self.brief_table = pd.DataFrame()
        self.desc_table = pd.DataFrame(columns = ['Output_gene','Input_gene'])

        # Stores the naming conventions for the brief table for associated terms
        # Extensible to new modules
        self.module_names = dict()


    # Method formats the disease name for printing 
    def format_print(self, title=''):

        print("\n" + title + " for " +
                  self.disease + "(" + self.mondo_id + "):\n")

        # END



    # This method builds the descriptive table pandas dataframe. It returns nothing
    # and is given a pandas dataframe of an individual module's results.
    def build_desc_table(self, mod_results):
        """
        Method builds the descriptive table into a pandas dataframe.
        Combines existings desc_table with the pre-processed data each time called
        
        Parameters: 
        mod_results >  Formatted module output with the following columns 

        output_gene | Input_gene | Scores or Hits | Terms (optional)

        Output: None

        Updates the self.desc_table dataframe by merging the new mod_results data into self.desc_table by input-output gene. 
        If the input-output gene relationship already exists the new columns is added to the end reflecting the new relationship.

        NAIVE:
        If the module output contains a score value please name the column with blank'_score'. This allows for dual use of counting gene hits 
        and sorting but the sum of the gene scores. 
        In the future this could sort on a 

        MORE EXPLAINAITION IF WE WANT

        """

        # Combine exisiting desc_table with mod pre-processed data
        # If desc_table is empty, it will only hold mod info and columns pertaining to particular mod
        self.desc_table = pd.merge(self.desc_table, mod_results, on=['Input_gene','Output_gene'], how='outer')


        # JG: Attempting to use expressions to find '_score' and summing across the hits to get the 'sum' col
        # this allows for extendable coding.
        self.desc_table['sum'] = self.desc_table.filter(regex=("_score$")).sum(axis=1)

        # Now do the sorting
        self.desc_table = self.desc_table.sort_values(['sum'], ascending = False)

        # Now drop the column used to sort
        self.desc_table = self.desc_table.drop(columns="sum")

        # End 


    def build_brief_table(self):
        """
        This method builds the brief table pandas dataframe. it returns nothing and takes no parameters.
        
        Everytime its called the brief_table is built from scratch by aggregating the descriptive table into counts.

        If optional terms are included then the self.module_names must be populated to format the columns 

        The brief table displays each unique Output_gene entry and each following column is counts of supporting info from each module. 

        This allows for an extensible platform to show lines of support 

        Brief Table Format:

        Output_gene | Input_gene_cnts | Mod1A_counts | etc...
        """


        # Find counts for all support based on each unique Output_gene
        self.brief_table = self.desc_table.groupby(['Output_gene']).aggregate('count')
        

        ## JG: editing the below code to be extensible for any module! added the self.module_names dictionary
        ## This is used to rename the associated terms into gene counts 
        for term in self.module_names.keys():

            # Search for the title then replace with the dictionary created in the addmod___ method
            if term in list(self.brief_table.columns.values):
                self.brief_table = self.brief_table.drop(columns=term)
                self.brief_table = self.brief_table.rename(
                    index=str, columns = self.module_names[term])



        # sort by the total number of input genes for each output gene
        # Make total hits but its at the end so reorder the table 
        self.brief_table['Total_hits'] =  self.brief_table.drop('Input_gene', axis=1).sum(axis=1)

        # Send the total hits to the second columns
        cols = self.brief_table.columns.tolist() # Find column names so it can be extensible
        cols.insert(0, cols.pop(cols.index('Input_gene'))) # Input_gene is first
        cols.insert(1, cols.pop(cols.index('Total_hits'))) # Total_gene is second then everything else is after that 

        # Reorder!
        self.brief_table = self.brief_table.reindex(columns=cols)

        # Now sort
        self.brief_table = self.brief_table.sort_values(['Total_hits'],ascending =False)


        # Reordering descriptive table
        new_row_order = self.brief_table.index.tolist() # get row names (output_genes)
        new_rows_Idx = dict(zip(new_row_order,range(len(new_row_order)))) # make ordered dict of output_genes 
        self.desc_table['Output_rank'] = self.desc_table['Output_gene'].map(new_rows_Idx) # map the descriptive table to this order
        self.desc_table = self.desc_table.sort_values('Output_rank') # Sort based on new mapping
        self.desc_table = self.desc_table.drop('Output_rank',axis=1) # Remove the sorting column

        # End



    # This function takes in the Module1A results and updates both tables
    def add1A(self, mod1a_results):


        # Immediately store raw data
        self.raw_module_data['mod1A'] = mod1a_results

        ##### Format Data for Cross Module Summary #####
        ## Initalize the naming paradigm for the module and for the brief table. 
        self.module_names['Func_assoc_terms'] = {'Func_sim_score':'Func_sim_input_gene_ct'}

        # drop irrelevant columns
        mod1a_processed = mod1a_results.drop(columns=['hit_id','input_id','shared_terms','module'])
        
        # drop duplicates in input
        mod1a_processed = mod1a_processed.drop_duplicates(subset=['input_symbol','hit_symbol'])
        
        # rename columns to match desc_table desired output column names
        mod1a_processed = mod1a_processed.rename(index = str, columns = {'hit_symbol':'Output_gene','input_symbol':'Input_gene','score':'Func_sim_score','shared_labels':'Func_assoc_terms'})
        
        # Recast GO terms as a list, so we can do sorting later
        mod1a_processed.Func_assoc_terms = mod1a_processed.Func_assoc_terms.astype(str)

        
        # Update descriptive table
        self.build_desc_table(mod1a_processed)

        # Update brief table
        self.build_brief_table()

        ##### Format Data for in module Summary #####
        ## Written by Colleen Xu 

        Mod1A_part1 = mod1a_results.groupby(['hit_symbol','hit_id'])['input_symbol'].apply(list).reset_index()
        Mod1A_part2 = mod1a_results.groupby(['hit_symbol','hit_id'])['input_id'].apply(list).reset_index()
        Mod1A_part3 = mod1a_results.groupby(['hit_symbol','hit_id']).aggregate({'score': 'count'}).rename(index=str, columns={'score':'FunctionalSimilarity'})
    
        ## Merge the parts together!
        Mod1A_final = Mod1A_part1.merge(Mod1A_part2, on=['hit_symbol', 'hit_id'])
        ## Another merge, and sort in descending order of number of interactions, ascending alphabetical order
        Mod1A_final = Mod1A_final.merge(Mod1A_part3, on=['hit_symbol', 'hit_id']).sort_values(by=['FunctionalSimilarity','hit_symbol'], ascending=[False, True])
    
        self.module_summaries['mod1A'] = Mod1A_final.filter(items=['hit_symbol', 'input_symbol', 'FunctionalSimilarity']).rename(index=str, columns={'hit_symbol': 'Output_Gene', 'input_symbol':'Input_Gene'})

        # END
        

    # This function takes in the Module1B results and updates both tables
    def add1B(self, mod1b_results):    
        ## Imediately store output
        self.raw_module_data['mod1B'] = mod1b_results


        ##### Format Data for Cross Module Summary #####
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

         ##### Format Data for in module Summary #####
        ## Written by Colleen Xu 

        ## merging columns, creating lists of the inputs and sums of the scores
        ## CX note: obviously it would be nice to do this all at once. the apply(list) only worked on one column at a time. aggregate only accepts a limited number of functions
        Mod1B_part1 = mod1b_results.groupby(['hit_symbol','hit_id'])['input_symbol'].apply(list).reset_index()
        Mod1B_part2 = mod1b_results.groupby(['hit_symbol','hit_id'])['input_id'].apply(list).reset_index()
        Mod1B_part3 = mod1b_results.groupby(['hit_symbol','hit_id']).aggregate({'score': 'count'}).rename(index=str, columns={'score':'PhenotypicSimilarity'})

        ## Merge the parts together!
        Mod1B_final = Mod1B_part1.merge(Mod1B_part2, on=['hit_symbol', 'hit_id'])
        ## Another merge, and sort in descending order of number of interactions, ascending alphabetical order
        Mod1B_final = Mod1B_final.merge(Mod1B_part3, on=['hit_symbol', 'hit_id']).sort_values(by=['PhenotypicSimilarity','hit_symbol'], ascending=[False, True])
        self.module_summaries['mod1B'] = Mod1B_final.filter(items=['hit_symbol', 'input_symbol', 'PhenotypicSimilarity']).rename(index=str, columns={'hit_symbol': 'Output_Gene', 'input_symbol':'Input_Gene'})



    # This function does do anything yet, but the idea is
    # This function takes in the Module1E results and updates both tables
    def add1E(self, mod1e_results):
        # Store raw data
        self.raw_module_data['mod1E'] = mod1e_results

        ##### Format Data for Cross Module Summary #####
        # drop irrelevant columns
        mod1e_processed = mod1e_results.drop(columns=['hit_id','input_id'])
        
        # drop duplicates in input
        mod1e_processed = mod1e_processed.drop_duplicates(subset=['input_symbol','hit_symbol'])
        

        # rename columns to match desired desc_table output column names
        # Rename score to Gene_Gene_hit so that the build_desc_table doesnt take the integer values in the sum. Here it is just a hit
        mod1e_processed = mod1e_processed.rename(index = str, columns = {'hit_symbol':'Output_gene','input_symbol':'Input_gene','score':'Gene_Gene_hit'})
        
        # Update descriptive table
        self.build_desc_table(mod1e_processed)

        # Update brief table
        self.build_brief_table()

        ##### Format Data for in module Summary #####
        ## Written by Colleen Xu 
        ## merging columns, creating lists of the inputs and sums of the scores
        ## CX note: obviously it would be nice to do this all at once. the apply(list) only worked on one column at a time. aggregate only accepts a limited number of functions
        Mod1E_part1 = mod1e_results.groupby(['hit_symbol','hit_id'])['input_symbol'].apply(list).reset_index()
        Mod1E_part2 = mod1e_results.groupby(['hit_symbol','hit_id'])['input_id'].apply(list).reset_index()    
        Mod1E_part3 = mod1e_results.groupby(['hit_symbol','hit_id']).aggregate({'score': 'sum'}).rename(index=str, columns={'score':'Interactions'})
        ## Merge the parts together!
        Mod1E_final = Mod1E_part1.merge(Mod1E_part2, on=['hit_symbol', 'hit_id'])
        ## Another merge, and sort in descending order of number of interactions, ascending alphabetical order
        Mod1E_final = Mod1E_final.merge(Mod1E_part3, on=['hit_symbol', 'hit_id']).sort_values(by=['Interactions','hit_symbol'], ascending=[False, True])
    
        self.module_summaries['mod1E'] = Mod1E_final.filter(items=['hit_symbol', 'input_symbol', 'Interactions']).rename(index=str, columns={'hit_symbol': 'Output_Gene', 'input_symbol':'Input_Gene'})
        

        # END

    # Method takes in a query or list of queries (module names) and returns their brief summary
    def show_single_mod_summary(self,query):

        # check if single query and make into list most extensible 
        if isinstance(query, str):
            query = [query] # make it into list of one 

        # For each query in the list display the brief data
        for mod in query:
            if mod in self.raw_module_data.keys():
                self.format_print(mod + ' results')
                print(self.module_summaries[mod].to_string())
            else:
                print('module query not found')
        return 

    # Method returns single module summary dictionary containing data frame
    def get_single_mod_summaries(self):
        return self.module_summaries

    # This function shows the current modules loaded into the object by referencing the current raw data stored
    def show_mods(self):
        self.current_mods = list(self.raw_module_data.keys())
        print('Modules Currently Loaded: ' + \
            ', '.join(self.current_mods))
        
    # Method returns list of current modules used as dictionary keys
    def get_mods(self):
        self.current_mods = list(self.raw_module_data.keys())
        return self.current_mods

    # This function returns a dictionary of the raw pandas data if people want to play with it 
    # Allows for the analysis of the raw data in other ways too as invisioned basically a container for all module output
    def return_raw_output(self):
        return self.raw_module_data


    # This function prints the brief table to console
    def show_brief(self):
        self.format_print('Brief Summary Table')
        print(self.brief_table.to_string())
        

     # This function returns the brief table
    def get_brief(self):
        return self.brief_table

    # This function prints the descriptive table to console
    def show_descriptive(self):
        self.format_print('Descriptive Summary Table')
        print(self.desc_table.to_string())

    # This function retunrs the descriptive table 
    def get_descriptive(self):
        return self.desc_table

    # This function returns both the brief and descriptive tables 
    def get_all(self):
        return self.get_brief() ,self.get_descriptive()

    # Function prints both brief and descriptive tables
    def show_all(self):
        self.format_print('Both Brief and Descriptive Summary Table')
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
