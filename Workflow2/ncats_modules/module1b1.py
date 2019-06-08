# Workflow 2, Module 1B: Phenotype similarity
from pprint import pprint
from mygene import MyGeneInfo
from .generic_similarity import GenericSimilarity


class PhenotypeSimilarity(GenericSimilarity):

    def __init__(self, taxon):

        GenericSimilarity.__init__(self)

        self.taxon = taxon
        if self.taxon == 'mouse':
            self.ont = 'mp'
        if self.taxon == 'human':
            self.ont = 'hp'
        self.meta = {
            'input_type': {
                'complexity': 'set',
                'id_type': 'HGNC',
                'data_type': 'gene',
            },
            'output_type': {
                'complexity': 'set',
                'id_type': 'HGNC',
                'data_type': 'gene',
            },

            'source': 'Monarch Biolink',
            'predicate': ['blm:has phenotype']
        }

        # Load the associated Biolink (Monarch)
        # phenotype ontology and annotation associations
        self.load_associations(taxon)

    def metadata(self):
        print("""Mod1B1 Phenotype Similarity metadata:""")
        pprint(self.meta)

    def load_gene_set(self, input_gene_set):
        annotated_gene_set = []
        for gene in input_gene_set.get_input_curie_set():
            mg = MyGeneInfo()
            gene_curie = ''
            sim_input_curie = ''
            symbol = ''
            if 'MGI' in gene['hit_id']:
                gene_curie = gene['hit_id']
                sim_input_curie = gene['hit_id']
                # if self.ont == 'go':
                #     sim_input_curie = gene.replace('MGI', 'MGI:MGI')
                # else:
                #
                symbol = None
            if 'HGNC' in gene['hit_id']:
                mgi_gene_curie = gene['hit_id'].replace('HGNC', 'hgnc')
                scope = 'HGNC'
                mg_hit = mg.query(mgi_gene_curie,
                                  scopes=scope,
                                  species=self.taxon,
                                  fields='uniprot, symbol, HGNC',
                                  entrezonly=True)
                try:
                    gene_curie = gene['hit_id']
                    sim_input_curie = gene['hit_id']
                    symbol = mg_hit['hits'][0]['symbol']

                except Exception as e:
                    print(__name__+".load_gene_set() Exception: ", gene, e)

            annotated_gene_set.append({
                'input_id': gene_curie,
                'sim_input_curie': sim_input_curie,
                'input_symbol': gene['hit_symbol']
            })

        return annotated_gene_set

    def compute_similarity(self, annotated_gene_set, threshold):
        lower_bound = float(threshold)
        results = self.compute_jaccard(annotated_gene_set, lower_bound)
        for result in results:
            for gene in annotated_gene_set:
                if gene['sim_input_curie'] == result['input_id']:
                    result['input_symbol'] = gene['input_symbol']
        return results
