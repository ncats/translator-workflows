from SPARQLWrapper import SPARQLWrapper, JSON
from pprint import pprint


class RheaMethods(object):
    def __init__(self):
        self.endpoint = SPARQLWrapper('https://sparql.rhea-db.org/sparql')

    def execute_query(self, query):
        self.endpoint.setQuery(query)
        self.endpoint.setReturnFormat(JSON)
        return self.endpoint.query().convert()

    def get_all_reactions_that_produce_compound(self, chebi):
        query = '''PREFIX rh:<http://rdf.rhea-db.org/>
        SELECT ?reaction ?products ?chebi_id ?ecNumber WHERE {
          ?reaction rdfs:subClassOf rh:DirectionalReaction;
                    rh:status rh:Approved;
                    rh:products ?productside.
          ?productside rh:contains ?products.
          ?products rh:compound ?small_molecule.
          ?small_molecule rh:accession '%s';
                          rh:accession ?chebi_id.
        }
        ''' % (chebi)
        return self.execute_query(query)

    def get_all_reactions_that_consume_compound(self, chebi):
        query = '''PREFIX rh:<http://rdf.rhea-db.org/>
        SELECT ?reaction ?substrates ?chebi_id ?ecNumber WHERE {
          ?reaction rdfs:subClassOf rh:DirectionalReaction;
                    rh:status rh:Approved;
                    rh:substrates ?substrateside.
          ?substrateside rh:contains ?substrates.
          ?substrates rh:compound ?small_molecule.
          ?small_molecule rh:accession '%s';
                          rh:accession ?chebi_id.
        }
        ''' % (chebi)
        return self.execute_query(query)

