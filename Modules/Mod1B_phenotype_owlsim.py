class PhenotypeOwlSim(object):

    def __init__(self, test_results):
        self.blw = BioLinkWrapper()
        self.gene_phenotypes = ''
        self.results = []
        self.test_results = ''
        with open('test_results.json', 'r') as test_results:
            self.test_results = json.load(test_results)

    def load_gene_set(self, gene_set, taxon=None):
        """
        Load a gene set and taxon
        """
        self.gene_set = gene_set
        self.taxon = taxon

    def map_phenotypes(self):
        self.gene_phenotypes = {gene: self.blw.gene2phenotypes(gene_curie=gene)['objects'] for gene in self.gene_set}

    def compute_similarity(self):
        for gene, phenos in self.gene_phenotypes.items():
            os = SimSearch()
            self.results.append({'gene': gene,
                                 'results': os.phenotype_search(phenos)
                                 })

    def parse_results(self, upper_bound, lower_bound):
        parsed_results = []
        for res in self.test_results:
            if 'matches' in res['results'].keys():
                filtered_matches = list(
                    map(lambda x: PhenotypeOwlSim.parse_match(x, upper_bound=upper_bound, lower_bound=lower_bound),
                        res['results']['matches']))
                parsed_results.append({res['gene']: [x for x in filtered_matches if x != None]})
        return parsed_results

    @staticmethod
    def parse_match(match, upper_bound, lower_bound):
        parsed = None
        gene_prefix = 'NCBIGene'
        if match['rawScore'] > float(lower_bound) and match['rawScore'] < float(upper_bound):
            match.update({'output': 'Mod1B'})
            if gene_prefix in match['matchId']:
                match.update({"category": "gene"})
            else:
                match.update({"category": "disease"})
            parsed = match
        return parsed


