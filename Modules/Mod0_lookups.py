from BioLink.biolink_client import BioLinkWrapper
from mygene import MyGeneInfo
import pandas as pd


class LookUp(object):

    def __init__(self):
        self.blw = BioLinkWrapper()
        self.mg = MyGeneInfo()

    def input_object_lookup(self, input_curie):
        input_object = self.blw.get_obj(obj_id=input_curie)
        return {
            'id': input_object['id'],
            'label': input_object['label'],
            'description': input_object['description'],
        }

    def disease_geneset_lookup(self, disease2genes_object):
        input_disease_object = self.input_object_lookup(input_curie=disease2genes_object['id'])
        input_disease_id = input_disease_object['id']
        input_disease_label = input_disease_object['label']
        input_gene_set = self.blw.disease2genes(input_disease_id)
        input_gene_set = [self.blw.parse_association(input_disease_id, input_disease_label, x) for x in input_gene_set['associations']]
        for input_gene in input_gene_set:
            igene_mg = self.mg.query(input_gene['hit_id'].replace('HGNC', 'hgnc'), species='human', entrezonly=True,
                                fields='entrez,HGNC,symbol')
            input_gene.update({'ncbi': 'NCBIGene:{}'.format(igene_mg['hits'][0]['_id'])})

        input_genes_df = pd.DataFrame(data=input_gene_set)
        # # group duplicate ids and gather sources
        input_genes_df['sources'] = input_genes_df['sources'].str.join(', ')
        input_genes_df = input_genes_df.groupby(
            ['input_id', 'input_label', 'hit_id', 'hit_label', 'ncbi'])['sources'].apply(', '.join).reset_index()

        return input_genes_df


