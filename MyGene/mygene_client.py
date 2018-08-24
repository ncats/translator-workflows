import requests
from pprint import pprint
import mygene
import json

class QueryMyGene(object):

    def __init__(self, url='https://mygene.info/v3'):
        self.url = url
        self.my_gene = mygene.MyGeneInfo(url)

    def query_mygene(self, curie, fields='all', taxon=None):
        """
        Get an entrez gene for a given curie
        """
        hit = None
        taxon_map = {
            'mouse': r'mgi:MGI\\:',
            'rat': 'rgd:',
            'zfin': 'zfin:',
        }
        curie = QueryMyGene.trim_curie(curie)
        if taxon:
            curie = '{0}{1}'.format(taxon_map[taxon], curie)

        results = self.my_gene.query(q=curie, fields=fields)
        if results is None or 'hits' not in results:
            print('No MyGene Record for {}'.format(curie))
        else:
            hit = results['hits'][0]

        return hit

    def ec2entrez(self, curie, fields='all'):
        """
        Get all entrez genes for a given ec identifier
        """
        hits = []
        curie = "ec:{}".format(curie)
        results = self.my_gene.query(q=curie, fields=fields)
        for result in results:
            hits.append(QueryMyGene.add_prefix(prefix='NCBIGene', identifier=result['entrezgene']))
        return hits

    @staticmethod
    def trim_curie(curie):
        """
        Trim a given curie to get its identifier
        """
        if 'HGNC' in curie:
            # MyGeneInfo supports HGNC curies
            curie = curie.replace('HGNC', 'hgnc')
        else:
            # If any other curie, then trim the curie to its identifier
            curie = curie.split(':')[1]
        return curie

    @staticmethod
    def parse_uniprot(results):
        """
        Extract only UniProt results
        """
        uniprot_results = None
        if 'uniprot' in results.keys():
            uniprot = results['uniprot']
            if 'Swiss-Prot' in uniprot.keys():
                if isinstance(uniprot['Swiss-Prot'], list):
                    uniprot_results = uniprot['Swiss-Prot']
                elif isinstance(uniprot['Swiss-Prot'], str):
                    uniprot_results = [uniprot['Swiss-Prot']]
        return uniprot_results

    @staticmethod
    def add_prefix(prefix, identifier):
        """
        Add prefix to a given identifier
        """
        return '{0}:{1}'.format(prefix, identifier)

