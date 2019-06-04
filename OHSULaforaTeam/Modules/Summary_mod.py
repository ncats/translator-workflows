import pandas as pd
import numpy as numpy


class Summary(object):
	desc_table = None
	brief_table = None
	output_genes = set()
	input_genes = set()

	def __init__(self):
		self.test = "hello"
		self.brief_table = pd.DataFrame(columns =['Output_gene','Input_gene','Func_sim_input_gene','Pheno_sim_input_gene'])
		self.desc_table = pd.DataFrame(columns = ['Output_gene', 'Input_gene','Func_sim_score','Func_assoc_terms','Pheno_sim_score','Pheno_assoc_terms'])

	def build_desc_table(self, mod_results):
		# get column numbers from module output by names
		hit_symbol = mod_results.columns.get_loc('hit_symbol')
		input_symbol = mod_results.columns.get_loc('input_symbol')
		score = mod_results.columns.get_loc('score')
		module = mod_results.columns.get_loc('module')
		commonTerm_labels = mod_results.columns.get_loc('commonTerm_labels')
		### Build descriptive table ###
		# assumes one input-output gene line per table
		# get index of column headers...
		for i in range(mod_results.shape[0]):
			output_gene = mod_results.iloc[i,hit_symbol]
			input_gene = mod_results.iloc[i,input_symbol]
			score_value = mod_results.iloc[i,score]
			terms = mod_results.iloc[i, commonTerm_labels]
			module_value = mod_results.iloc[i, module]
			#print(module_value, input_gene, output_gene)
			lines = self.desc_table[(self.desc_table['Output_gene']==output_gene) & (self.desc_table['Input_gene']==input_gene)]
			if lines.shape[0] == 0: # input-output gene relationship not yet in desc_table
				if module_value == 'Mod1A':
					self.desc_table.loc[self.desc_table.shape[0]] = [output_gene, input_gene, score_value, terms,0,""]
				elif module_value == 'Mod1B':
					self.desc_table.loc[self.desc_table.shape[0]] = [output_gene, input_gene, 0, "", score_value, terms]
			# else if input-output gene relationship already in desc_table
			else:
				# find row number of input-output gene relationship in desc_table
				row_num = self.desc_table.loc[(self.desc_table['Output_gene']==output_gene) & (self.desc_table['Input_gene']==input_gene)].index
				# update desc_table for the score and terms for this module
				## VALUE DEPENDS ON MODULE!
				if module_value == 'Mod1A':
					self.desc_table.iloc[row_num, 2] = score_value
					self.desc_table.iloc[row_num, 3] = terms
				elif module_value == 'Mod1B':
					self.desc_table.iloc[row_num, 4] = score_value
					self.desc_table.iloc[row_num[0], 5] = str(terms)
					
	def add1A(self, mod1a_results):
		self.mod1A = mod1a_results
		### Build brief table ###
		# first update genes already in table
		old_output_genes = mod1a_results['hit_symbol'][mod1a_results['hit_symbol'].isin(self.brief_table['Output_gene'])]
		for gene in old_output_genes:
			lines = mod1a_results.loc[mod1a_results['hit_symbol']==gene]
			## how do we know if we're adding a new input_gene connection?
			## build desc_table first...
		# then update table to add new genes
		# get list of output genes not currently in brief table
		new_output_genes = mod1a_results['hit_symbol'][~mod1a_results['hit_symbol'].isin(self.brief_table['Output_gene'])]
		for gene in new_output_genes:
			lines = mod1a_results.loc[mod1a_results['hit_symbol']==gene]
			count = lines.shape[0]
			#self.brief_table.append(pd.Series[gene, count, count, 0])
			self.brief_table.loc[self.brief_table.shape[0]] = [gene, count, count, 0]

		self.build_desc_table(mod1a_results)
		self.build_brief_table()

	def build_brief_table(self):
		#output #ct_inputs #func_ct_inputs #pheno_ct_inputs
		for output_gene in self.desc_table.Output_gene.unique():
			print(output_gene)
			desc_lines = self.desc_table[(self.desc_table['Output_gene']==output_gene)]
			print(desc_lines)

	def add1B(self, mod1b_results):
		self.build_desc_table(mod1b_results)
		self.build_brief_table()

	def add1E(self, mod1e_results):
		self.mod1E = mod1e_results

	def get_brief(self):
		print(self.brief_table.to_string())

	def get_descriptive(self):
		print(self.desc_table.to_string())

	def get_all(self):
		print("here")
		self.get_brief()
		self.get_descriptive()

	def write_brief(self):
		self.brief_table.to_csv("brief_table.csv")

	def write_descriptive(self):
		self.desc_table.to_csv("desc_table.csv")

	def write_all(self):
		self.write_brief()
		self.write_descriptive()

	def write_json(self):
		self.brief_table.to_json("brief_table.json")
		self.desc_table.to_json("desc_table.json")
		return None
