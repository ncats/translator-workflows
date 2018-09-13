import requests
from pprint import pprint
import mygene


class QueryMyGene(object):

    def __init__(self,):
        self.my_gene = mygene.MyGeneInfo()

    def all_gene_map(self, species, fields, gene_set):
        all_genes = self.my_gene.querymany(gene_set, species=species, fields=fields)
        return all_genes

    def query_mygene(self, curie, fields='all', taxon=None, taxon_name='human'):
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

        results = self.my_gene.query(q=curie, fields=fields, species=taxon_name)
        if results is None or 'hits' not in results:
            print('No MyGene Record for {}'.format(curie))
        else:
            hit = results['hits']

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

        # curie_map derived from http://docs.mygene.info/en/latest/doc/query_service.html?highlight=mgi#scrolling-queries
        curie_map = {
            'NCBIGene': 'entrezgene',
            'UniProtKB': 'uniprot',
            'GO': 'go',
            'HGNC': 'hgnc',
            'MGI': 'mgi:MGI\\\\',
            'RGD': 'rgd',
            'FlyBase': 'flybase',
            'WormBase': 'wormbase',
            'ZFIN': 'zfin',
            'Xenbase': 'xenbase',
            'TAIR': 'tair'
        }

        if ':' in curie:
            curie_split = curie.split(':')
            prefix = curie_split[0]
            if prefix in curie_map.keys():
                curie = "{}:{}".format(curie_map[prefix], ':'.join(curie_split[1:]))

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

