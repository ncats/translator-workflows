from SPARQLWrapper import SPARQLWrapper, JSON
from MyGene.mygene_client import QueryMyGene
from pprint import pprint
from UniProt.uniprot_sparql_wrapper import UniProtSparql


class RheaMethods(object):
    def __init__(self):
        self.endpoint = SPARQLWrapper('https://sparql.rhea-db.org/sparql')
        self.mygene = QueryMyGene()
        self.ups = UniProtSparql()

    def execute_query(self, query):
        self.endpoint.setQuery(query)
        self.endpoint.setReturnFormat(JSON)
        return self.endpoint.query().convert()

    def get_all_reactions_that_produce_compound(self, chebi):
        query = '''PREFIX rh:<http://rdf.rhea-db.org/>
            PREFIX ec:<http://purl.uniprot.org/enzyme/>
            SELECT ?reaction ?reactionEquation  ?ecNumber ?chebi_id ?curatedOrder WHERE {
              ?reaction rdfs:subClassOf rh:Reaction;
                        rh:status rh:Approved;
                        rh:ec ?ecNumber;
                        rh:directionalReaction ?directional_reaction.
              ?directional_reaction rh:status rh:Approved;
                                    rh:products ?productside;
                                    rh:equation ?reactionEquation.
              ?productside rh:curatedOrder ?curatedOrder;
                           rh:contains ?products.
              ?products rh:compound ?small_molecule.
              ?small_molecule rh:accession '%s';
                              rh:accession ?chebi_id.
            }
        ''' % (chebi)
        return self.execute_query(query)

    def get_all_reactions_that_consume_compound(self, chebi):
        query = '''PREFIX rh:<http://rdf.rhea-db.org/>
        SELECT ?reaction ?reactionEquation  ?ecNumber ?chebi_id  ?curatedOrder ?substrates WHERE {
              ?reaction rdfs:subClassOf rh:Reaction;
                            rh:status rh:Approved;
                            rh:ec ?ecNumber;
                            rh:directionalReaction ?directional_reaction.
                            
              ?directional_reaction rh:status rh:Approved;
                        rh:equation ?reactionEquation;
                        rh:substrates ?substrateside.
              ?substrateside rh:curatedOrder ?curatedOrder;
                             rh:contains ?substrates.
              ?substrates rh:compound ?small_molecule.
              ?small_molecule rh:accession '%s';
                              rh:accession ?chebi_id.
            }
        ''' % (chebi)
        return self.execute_query(query)

    def get_reaction_by_ec(self, ec):
        query = '''PREFIX rh:<http://rdf.rhea-db.org/>
            PREFIX ec:<http://purl.uniprot.org/enzyme/>
            SELECT ?reaction ?reactionEquation ?ecNumber ?chebi_id ?curatedOrder WHERE {
              ?reaction rdfs:subClassOf rh:Reaction;
                        rh:status rh:Approved;
                        rh:ec ?ecNumber;
                        rh:directionalReaction ?directional_reaction.
              ?directional_reaction rh:products ?productside;
                                    rh:equation ?reactionEquation.
              ?productside rh:curatedOrder ?curatedOrder;
                           rh:contains ?products.
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
            if reaction['curatedOrder'] == 2:
                ec = reaction['ecNumber']['value'].split('/')[-1]

                output = {
                    'input': chebi,
                    'type': 'products',
                    'proteins': self.ups.ec2uniprot(ec=ec),
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
            output = {
                'input': chebi,
                'type': 'substrates',
                'proteins': self.ups.ec2uniprot(ec=ec),
                'ec': ec,
                'rheaid': reaction['reaction']['value'],
                'reaction': reaction['reactionEquation']['value'],
            }
            outputs.append(output)
        return outputs

    def gene2product(self, ncbigene):
        mg = self.mygene.query_mygene(curie=ncbigene)
        uniprot = ''
        if len(mg) == 1:
            uniprot = "".join(self.mygene.parse_uniprot(mg[0]))
        ec = self.ups.uniprot2ec(uniprot)






