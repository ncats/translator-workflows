import requests


class BioLinkWrapper(object):
    def __init__(self):
        self.endpoint = 'https://api.monarchinitiative.org/api/'
        self.params = {
            'fetch_objects': 'true',
        }

    def get_obj(self, obj_id):
        url = '{0}bioentity/{1}'.format(self.endpoint, obj_id)
        response = requests.get(url)
        return response.json()

    def disease2genes(self, disease_curie):
        params = {}
        params.update(self.params)
        url = '{0}bioentity/disease/{1}/genes'.format(self.endpoint, disease_curie)
        response = requests.get(url, params)
        return response.json()

    def disease2phenotypes(self, disease_curie):
        params = {}
        url = '{0}bioentity/disease/{1}/phenotypes'.format(self.endpoint, disease_curie)
        response = requests.get(url, params)
        return response.json()

    def gene(self, gene_curie):
        params = {}
        url = '{0}bioentity/gene/{1}'.format(self.endpoint, gene_curie)
        response = requests.get(url, params)
        return response.json()

    def gene2orthologs(self, gene_curie, orth_taxon_name=None):
        taxon_map = {
            'human': 'NCBITaxon:9606',
            'mouse': 'NCBITaxon:10090',
            'rat': 'NCBITaxon:10116',
            'zebrafish': 'NCBITaxon:7955',
            'fly': 'NCBITaxon:7227',
            'worm': 'NCBITaxon:6239'
        }
        params = {}
        if orth_taxon_name:
            params['homolog_taxon'] = taxon_map[orth_taxon_name]
        url = '{}bioentity/gene/{}/homologs'.format(self.endpoint, gene_curie)
        response = requests.get(url, params)
        return response.json()

    def phenotype2genes(self, phenotype_curie):
        url = '{}bioentity/phenotype/{}/genes'.format(self.endpoint, phenotype_curie)
        response = requests.get(url)
        return response.json()

    def gene2phenotypes(self, gene_curie):
        url = '{}bioentity/gene/{}/phenotypes'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def gene2diseases(self, gene_curie):
        url = '{}bioentity/gene/{}/diseases'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def gene_interactions(self, gene_curie):
        url = '{}bioentity/gene/{}/interactions'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def gene2functions(self, gene_curie):
        url = '{}bioentity/gene/{}/function'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def gene2tissue_expression(self, gene_curie):
        url = '{}bioentity/gene/{}/expression/anatomy'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def tissue2gene_expression(self, tissue_curie):
        url = '{}bioentity/anatomy/{}/genes'.format(self.endpoint, gene_curie)
        response = requests.get(url)
        return response.json()

    def disease_models(self, disease_curie):
        url = '{}/bioentity/disease/{}/models'.format(self.endpoint, disease_curie)
        response = requests.get(url)
        return response.json()

    def taxon2phenotypes(self, taxon_curie):
        # get phenotypes associated with taxid
        url = "mart/gene/phenotype/{}".format(self.endpoint, taxon_curie)
        response = requests.get(url)
        return response.json()

    def parse_gene_functions(self, curie):
        function_list = list()
        functions = self.gene2functions(gene_curie=curie)
        if 'associations' in functions.keys():
            for assoc in functions['associations']:
                function_list.append(assoc['object']['label'])
        function_set = set(function_list)
        return ", ".join(function_set)

    def get_orthoglog_gene_set(self, gene_set, orth_taxon_name):
        orth_set = []
        for gene in gene_set:
            orth_set.append(self.gene2orthologs(gene_curie=gene, orth_taxon_name=orth_taxon_name))
        return orth_set

    def compute_jaccard(self, id1, id2, category):
        url = "{0}/pair/sim/jaccard/{1}/{2}/".format(self.endpoint, id1, id2)
        params ={
            'object_category': category
        }
        params.update(self.params)
        response = requests.get(url, params)
        return response.json()

    def compute_owlsim(self, id):
        url = '{0}sim/search'.format(self.endpoint)
        params = {
            'id': id,
        }
        params.update(self.params)
        response = requests.get(url, params)
        return response.json()

    @staticmethod
    def parse_sources(sources):
        return [x.split('/')[-1].rstrip('.ttl') for x in sources]

    @staticmethod
    def parse_association(input_id, input_label, association, invert_subject_object=False):
        hit_id = association['object']['id']
        hit_label = association['object']['label']
        relation_label = association['relation']['label']
        if invert_subject_object:
            hit_id = association['subject']['id']
            hit_label = association['subject']['label']

        parsed_association = {
            'input_id': input_id,
            'input_symbol': input_label,
            'hit_id': hit_id,
            'hit_symbol': hit_label,
            'sources': BioLinkWrapper.parse_sources(association['provided_by']),
            'relation': relation_label
        }
        return parsed_association

    @staticmethod
    def return_objects(assoc_package):
        return assoc_package['objects']

    @staticmethod
    def filter_on_predicate(package, predicate):
        package['associations'] = [x for x in package['associations'] if x['relation']['label'] == predicate]
        return package


