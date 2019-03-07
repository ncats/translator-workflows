# USAGE: python3 hugo_to_ensg_id.py <GENE_FILE_NAME.txt>
import sys
original_dict = dict()
output_gene_list = []

with open('HUGO_geneids_download_v2.txt') as f:
    lines = f.readlines()
    rows = (line.split('\t') for line in lines )
    hugo_gene_ids = [x for x in rows]

# rows is a generator which has the stuff we need to translate...
input_gene_list_name = sys.argv[1]
#print(input_gene_list_name)
formatted_input_genes = []

with open(input_gene_list_name) as f_2:
    inputs = f_2.readlines()
    for line in inputs:
        formatted_input_genes.append(line.rstrip())
#print(formatted_input_genes)
translated_to_ENSG_gene_set = []
print()
from_ensg_to_symbol = []
while formatted_input_genes:
    #print('formatted_input_gene')
    gene = formatted_input_genes.pop().split('.')[0]
    # print(gene)
    # print()
    for row in hugo_gene_ids:
        if gene in row:
            print(gene)
            print()
            
            print(row[1])
            print()
            from_ensg_to_symbol.append([gene, row[1]])
            #print(gene)
            # for ensg_term in row:
            #     if ensg_term.startswith('ENSG'):
            #         if ensg_term not in translated_to_ENSG_gene_set:
            #             translated_to_ENSG_gene_set.append(ensg_term)

input_gene_list_name_shortened = input_gene_list_name.replace('.txt','')


converted_esng_output_gene_list_name = input_gene_list_name_shortened + '_converted_to_gene_symbols.txt'

ensg_ids = open(converted_esng_output_gene_list_name, "w")
with open(converted_esng_output_gene_list_name, 'w') as f:
    for item in from_ensg_to_symbol:
        f.write("%s\n" % item)