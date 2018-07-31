from SPARQLWrapper import SPARQLWrapper, JSON
from MyGene.mygene_client import QueryMyGene
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
            PREFIX ec:<http://purl.uniprot.org/enzyme/>
            SELECT ?reaction ?reactionEquation  ?ecNumber ?chebi_id WHERE {
              ?reaction rdfs:subClassOf rh:Reaction;
                        rh:status rh:Approved;
                        rh:ec ?ecNumber;
                        rh:directionalReaction ?directional_reaction.
              ?directional_reaction rh:products ?productside;
                                    rh:equation ?reactionEquation.
              ?productside rh:contains ?products.
              ?products rh:compound ?small_molecule.
              ?small_molecule rh:accession '%s';
                              rh:accession ?chebi_id.
            }
        ''' % (chebi)
        return self.execute_query(query)

    def get_all_reactions_that_consume_compound(self, chebi):
        query = '''PREFIX rh:<http://rdf.rhea-db.org/>
        SELECT ?reaction ?reactionEquation  ?ecNumber ?chebi_id WHERE {
          ?reaction rdfs:subClassOf rh:Reaction;
                        rh:status rh:Approved;
                        rh:ec ?ecNumber;
                        rh:directionalReaction ?directional_reaction.
                        
          ?directional_reaction rh:status rh:Approved;
                    rh:equation ?reactionEquation;
                    rh:substrates ?substrateside.
          ?substrateside rh:contains ?substrates.
          ?substrates rh:compound ?small_molecule.
          ?small_molecule rh:accession '%s';
                          rh:accession ?chebi_id.
        }
        ''' % (chebi)
        return self.execute_query(query)

    def get_reaction_by_ec(self, ec):
        query = '''PREFIX rh:<http://rdf.rhea-db.org/>
            PREFIX ec:<http://purl.uniprot.org/enzyme/>
            SELECT ?reaction ?reactionEquation ?chebi_id WHERE {
              ?reaction rdfs:subClassOf rh:Reaction;
                        rh:status rh:Approved;
                        rh:ec ?ecNumber;
                        rh:directionalReaction ?directional_reaction.
              ?directional_reaction rh:products ?productside;
                                    rh:equation ?reactionEquation.
              ?productside rh:contains ?products.
              ?products rh:compound ?small_molecule.
              ?small_molecule rh:accession ?chebi_id.
              FILTER (?ecNumber=ec:%s)
            }
        ''' % (ec)
        return self.execute_query(query)

    def product2gene(self, chebi):
        outputs = []
        reactions = self.get_all_reactions_that_produce_compound(chebi=chebi)
        for reaction in reactions['results']['bindings']:
            ec = reaction['ecNumber']['value'].split('/')[-1]
            mg = QueryMyGene(curie=ec)
            output = {
                'input': chebi,
                'type': 'products',
                'genes': mg.ec2entrez(),
                'ec': ec,
                'rheaid': reaction['reaction']['value'],
                'reaction': reaction['reactionEquation']['value'],
            }
            outputs.append(output)
        return outputs

    def substrate2gene(self, chebi):
        outputs = []
        reactions = self.get_all_reactions_that_consume_compound(chebi=chebi)
        for reaction in reactions['results']['bindings']:
            ec = reaction['ecNumber']['value'].split('/')[-1]
            mg = QueryMyGene(curie=ec)
            output = {
                'input': chebi,
                'type': 'substrates',
                'genes': mg.ec2entrez(),
                'ec': ec,
                'rheaid': reaction['reaction']['value'],
                'reaction': reaction['reactionEquation']['value'],
            }
            outputs.append(output)
        return outputs


