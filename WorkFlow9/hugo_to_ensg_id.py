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
formatted_input_genes = []

with open(input_gene_list_name) as f_2:
    inputs = f_2.readlines()
    for line in inputs:
        formatted_input_genes.append(line.rstrip())

#print(formatted_input_genes)

translated_gene_set = []
print()
while formatted_input_genes:
    gene = formatted_input_genes.pop()
    print(len(formatted_input_genes))
    print('gene:', gene)
    print()
    for row in hugo_gene_ids:
        if gene in row:
            print('row:', row)
            print()
