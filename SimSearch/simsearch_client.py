import requests
import pandas as pd


class SimSearchWrapper:
    SIMSEARCH_API = "https://monarchinitiative.org/simsearch/phenotype"

    def get_phenotypically_similar_genes(self, input_gene, phenotypes, taxon):
        """
        :param input_gene: gene with phenotypes
        :param phenotypes: list of phenotype curies
        :param taxon: an ncbi taxid (e.g. "10090")
        :param return_all:
        :return:
        """
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
        }
        data = {'input_items': " ".join(phenotypes), "target_species": taxon}
        r = requests.get(self.SIMSEARCH_API, params=data, headers=headers)
        d = r.json()
        return SimSearchResult(input_gene, d)


class SimSearchResult:
    def __init__(self, input_gene, d):
        self.d = d
        self.input_gene = input_gene
        self.matches = []
        if 'b' in self.d:
            for x in self.d['b']:
                self.matches.append(SimScoreMatch(x))

    def get_results(self):
        results = list()
        for smatch in self.matches:
            try:
                results.append((self.input_gene, smatch.get_id(), smatch.get_score(), smatch.get_label(), smatch.explain_match()))
            except Exception as e:
                print(e, smatch)

        return pd.DataFrame(results, columns=["input_id", "id", "score", "label", "explanation"])

    def explain_match(self, _id):
        match = [m for m in self.matches if m.get_id() == _id][0]
        return match.explain_match()


class SimScoreMatch:
    """ a match looks like:
    {
      'id': 'MGI:1914792',
      'label': 'Cog6',
      'matches': [{'a': {'IC': 4.758053613685234,
         'id': 'HP:0001903',
         'label': 'Anemia'},
        'b': {'IC': 12.3826428380023,
         'id': 'MP:0013022',
         'label': 'increased Ly6C high monocyte number'},
        'lcs': {'IC': 3.6863721977964343,
         'id': 'MP:0013658',
         'label': 'abnormal myeloid cell morphology'}},
       {'a': {'IC': 6.047802632643478,
         'id': 'HP:0001679',
         'label': 'Abnormal aortic morphology'},
        'b': {'IC': 10.936619714893055,
         'id': 'MP:0011683',
         'label': 'dual inferior vena cava'},
        'lcs': {'IC': 5.823930299277827,
         'id': 'UBERON:0003519PHENOTYPE',
         'label': 'thoracic cavity blood vessel phenotype'}}],
      'score': {'metric': 'combinedScore', 'rank': 93, 'score': 70},
      'taxon': {'id': 'NCBITaxon:10090', 'label': 'Mus musculus'},
      'type': 'gene'
    }
  """

    def __init__(self, match):
        # input is an item in the "b" list in the response from the simsearch api
        self.match = match

    def get_score(self):
        return self.match['score']['score']

    def get_label(self):
        return self.match['label']

    def get_id(self):
        return self.match['id']

    def explain_match(self):
        # semicolon separated: (human phenotype -> LCS <- other phenotype)
        # Anemia -> abnormal myeloid cell morphology <- increased Ly6C high monocyte number; Abnormal aortic morphology -> thoracic cavity blood vessel phenotype <- dual inferior vena cava
        s = []
        for m in self.match['matches']:
            s.append("{} -> {} <- {}".format(m['a']['label'], m['lcs']['label'], m['b']['label']))
        return "\n".join(s)


class test_SimSearchWrapper:
    def test(self):
        # from SimSearch.simsearch_client import *
        phenotypes = ['HP:0001679', 'HP:0001903']
        taxon = "10090"
        w = SimSearchWrapper()
        ssr = w.get_phenotypically_similar_genes(phenotypes, taxon)
        ssr.get_results()
        ssr.explain_match('MGI:3030214')
