from SPARQLWrapper import SPARQLWrapper, JSON


class UniProtSparql(object):
    def __init__(self):
        self.endpoint = SPARQLWrapper('http://sparql.uniprot.org/sparql/')

    def execute_query(self, query):
        self.endpoint.setQuery(query)
        self.endpoint.setReturnFormat(JSON)
        return self.endpoint.query().convert()

    def ec2uniprot(self, ec):
        query = '''
         PREFIX up:<http://purl.uniprot.org/core/> 
        PREFIX ec:<http://purl.uniprot.org/enzyme/> 
        PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> 
        SELECT ?protein 
        WHERE
        {
         ?protein up:enzyme ?enzyme.
          FILTER (?enzyme=ec:%s)
        }
        ''' % (ec)
        results = self.execute_query(query=query)
        uniprots = []
        for hit in results['results']['bindings']:
            uniprots.append(hit['protein']['value'].split('/')[-1])
        return uniprots

    def uniprot2ec(self, uniprot):
        query = '''
        BASE <http://purl.uniprot.org/uniprot/> 
        PREFIX ec:<http://purl.uniprot.org/enzyme/>
        PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> 
        PREFIX up:<http://purl.uniprot.org/core/> 
        
        SELECT ?protein ?enzyme
        WHERE
        {
            VALUES ?protein {<%s>}
            ?protein a up:Protein;
                up:enzyme ?enzyme.
            ?enzyme rdfs:subClassOf ?ecClass. 
        }
        ''' % (uniprot)
        results = self.execute_query(query=query)
        ecnumbers = []
        for hit in results['results']['bindings']:
            ecnumbers.append(hit['enzyme']['value'].split('/')[-1])
        return ecnumbers


