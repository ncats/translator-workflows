# Workflow 2, Module 1A: Functional similarity
from pprint import pprint
from biothings_client import get_client
from .generic_similarity import GenericSimilarity


class FunctionalSimilarity(GenericSimilarity):

    def __init__(self, taxon):
        GenericSimilarity.__init__(self)
        self.mg = get_client('gene')
        self.input_object = ''
        self.taxon = taxon
        self.ont = 'go'
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
            'predicate': ['blm:macromolecular machine to biological process association',
                          'macromolecular machine to molecular activity association']
        }

        # Load the functional catalog of
        # GO ontology and annotation associations
        self.load_associations(taxon)

    def metadata(self):
        print("""Mod1A Functional Similarity metadata:""")
        pprint(self.meta)

    def load_gene_set(self, input_gene_set):
        annotated_gene_set = []
        for gene in input_gene_set.get_input_curie_set():
            gene_curie = ''
            sim_input_curie = ''
            symbol = ''
            if 'MGI' in gene['hit_id']:
                gene_curie = gene['hit_id']
                sim_input_curie = gene['hit_id'].replace('MGI', 'MGI:MGI')
                symbol = None
            if 'HGNC' in gene['hit_id']:
                gene_curie = gene['hit_id'].replace('HGNC', 'hgnc')
                scope = 'HGNC'
                mg_hit = self.mg.query(gene_curie,
                                  scopes=scope,
                                  species=self.taxon,
                                  fields='uniprot, symbol, HGNC',
                                  entrezonly=True)
                try:
                    gene_curie = gene['hit_id']
                    sim_input_curie = 'UniProtKB:{}'.format(mg_hit['hits'][0]['uniprot']['Swiss-Prot'])
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
            if self.taxon == 'human':
                result['hit_id'] = self.symbol2hgnc(result['hit_symbol'])
            for gene in annotated_gene_set:
                if gene['sim_input_curie'] != result['input_id']:
                    result['input_id'] = self.symbol2hgnc(result['input_symbol'])
        return results

    def symbol2hgnc(self, symbol):
        mg_hit = self.mg.query('symbol:{}'.format(symbol),
                          fields='HGNC,symbol,taxon',
                          species='human',
                          entrezonly=True)
        if mg_hit['total'] == 1:
            return 'HGNC:{}'.format(mg_hit['hits'][0]['HGNC'])
