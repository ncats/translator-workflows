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
			columns = ['Output_gene','Input_gene','Func_sim_input_gene','Pheno_sim_input_gene'])
		self.desc_table = pd.DataFrame(
			columns = ['Output_gene', 'Input_gene','Func_sim_score','Func_assoc_terms','Pheno_sim_score','Pheno_assoc_terms'])

	# This method builds the descriptive table pandas dataframe. It returns nothing
	# and is given a pandas dataframe of an individual module's results
	def build_desc_table(self, mod_results):
		# Get column numbers from module output by column names
		# Written in case column order changes
		# Assumes column names are the same in each module
		hit_symbol = mod_results.columns.get_loc('hit_symbol')
		input_symbol = mod_results.columns.get_loc('input_symbol')
		score = mod_results.columns.get_loc('score')
		module = mod_results.columns.get_loc('module')
		commonTerm_labels = mod_results.columns.get_loc('commonTerm_labels')
		# assumes one input-output gene line per table
		# Iterate through each row in module results
		for i in range(mod_results.shape[0]):
			# Extract data from relevant columns in the input row, using the column
			# numbers set above
			output_gene = mod_results.iloc[i,hit_symbol] # output gene for this row
			input_gene = mod_results.iloc[i,input_symbol]
			score_value = mod_results.iloc[i,score]
			terms = mod_results.iloc[i, commonTerm_labels]
			module_value = mod_results.iloc[i, module]
			# Find all rows in the descriptive table that correspond to the current
			# input-output gene pair in module results
			lines = self.desc_table[(self.desc_table['Output_gene']==output_gene) 
				& (self.desc_table['Input_gene']==input_gene)]
			
			# If there are no lines in the descriptive table about this input-output
			# gene pair yet:
			if lines.shape[0] == 0:
				# Add a line in the desc_table corresponding to what we know about
				# this input-output gene pair (i.e., functional or phenotypic)
				# similarity 
				# column number dependent on module number
				if module_value == 'Mod1A':
					self.desc_table.loc[self.desc_table.shape[0]] \
						= [output_gene, input_gene, score_value, terms,0,"N/A"]
				elif module_value == 'Mod1B':
					self.desc_table.loc[self.desc_table.shape[0]] = \
						[output_gene, input_gene, 0, "N/A", score_value, terms]
				else:
					print("Summary_mod.py build_desc_table must be updated to accomodate module ",
						module_value)
					sys.exit()
			# else if input-output gene relationship already in desc_table:
			else:
				# find row number of input-output gene relationship in desc_table
				row_num = self.desc_table.loc[(self.desc_table['Output_gene']==output_gene) 
					& (self.desc_table['Input_gene']==input_gene)].index
				# update desc_table for the score and terms for this module
				# Column number dependent on module number
				if module_value == 'Mod1A':
					self.desc_table.iloc[row_num, 2] = score_value
					self.desc_table.iloc[row_num, 3] = str(terms)
				elif module_value == 'Mod1B':
					self.desc_table.iloc[row_num, 4] = score_value
					self.desc_table.iloc[row_num[0], 5] = str(terms)
				else:
					print("Summary_mod.py build_desc_table must be updated to accomodate module ",module_value)
					sys.exit()
		# sort desc_table by the two scores
		self.desc_table['sum'] = self.desc_table['Func_sim_score'] + self.desc_table['Pheno_sim_score']
		self.desc_table = self.desc_table.sort_values(['sum'], ascending = False)
		self.desc_table = self.desc_table.drop(columns="sum")
		#self.desc_table = self.desc_table.sort_values(['Func_sim_score','Pheno_sim_score'], ascending=False)
	
	# This method builds the brief table pandas dataframe. it returns nothing and
	# takes no parameters.
	def build_brief_table(self):
		# We're building this from scratch each time the method is called 
		# because it's easier to write at the moment
		# Create a new pandas dataframe to hold results
		self.brief_table = pd.DataFrame(
			columns =['Output_gene','Input_gene','Func_sim_input_gene','Pheno_sim_input_gene'])
		# Iterate through each unique output gene found in the desc_table
		for output_gene in self.desc_table.Output_gene.unique():
			# Pull out all lines in the desc_table that contain this output gene
			desc_lines = self.desc_table[self.desc_table['Output_gene']==output_gene]
			# Get total count of output gene in desc_lines
			total_count = desc_lines.shape[0]
			# Get count of input genes corresponding to output gene for both
			# the functional and phenotypic analyses
			# NOTE: the ['...score'] > 0 evaluation might get weird if we
			# 	change the default no-data value for score from int 0 to
			#	a string or something else.
			func_count = desc_lines[desc_lines['Func_sim_score'] >0].shape[0]
			pheno_count = desc_lines[desc_lines['Pheno_sim_score'] >0].shape[0]
			# Now add a row to the brief_table about these findings
			self.brief_table.loc[self.brief_table.shape[0]] = [output_gene, total_count, 
				str(func_count)+"/"+str(total_count), str(pheno_count)+"/"+str(total_count)]

		# Sort the brief table by the number of functional, phenotypic input gene hits
		self.brief_table = self.brief_table.sort_values(
			['Func_sim_input_gene','Pheno_sim_input_gene'], ascending=False)



	# This function takes in the Module1A results and updates both tables
	def add1A(self, mod1a_results):
		self.build_desc_table(mod1a_results)
		self.build_brief_table()

	# This function takes in the Module1B results and updates both tables
	def add1B(self, mod1b_results):
		self.build_desc_table(mod1b_results)
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
