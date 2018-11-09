## API development guidelines for NCATS translator project

This document summarizes the common guidelines we want to follow when developing new (or converting existing) APIs for the *blackboard* system, which will be used to answer the competency questions for NCATS translator project.

Just a few quick notes first:

* The response objects returned from an API should be the same entity type (a single object or a list of objects). See [entity types](#entity-types) below.
* Each entity type should have a defined "_id" field. See [entity types](#entity-types) below.
* An API should support both the query by _id, and batch query by a list of _id. See [API implementation](#api-implementation) below.


### Entity types
When the response of your API is relevant to these entity types, please include the minimal required field(s) listed below. The extra fields is up to the specic API.

Add the relevant entity types below as well.

#### Gene

 * required
   * **\_id**
     > *type*:   string       
     > *value*:  ncbi gene id if possible, otherwise ensembl gene id, e.g "1017"     

 * recommended
   * **symbol**
     > *type*:   string       
     > *value*:  official gene symbol, e.g. "CDK2"     

   * **symbol**
     (suggest to return when your API covers multiple species)
     > *type*:   integer       
     > *value*:  taxonomy id as an integer, e.g. 9606  

#### Variant (human varaints only for now)

 * required
   * **\_id**
     > *type*:   string       
     > *value*:  chromosome-based HGVS name, e.g. "chr1:g.35366C>T"     

     > **Note:**
     > - see [HGVS name examples from MyVariant.info](http://docs.myvariant.info/en/latest/doc/data.html#id-field) 
     > - we need to decide if we should use GRCh38 as the default human genome assembly

#### Drug/chemical compound

 * required
   * **\_id**
     > *type*:   string       
     > *value*:  InChIKey, e.g. "BQJCRHHNABKAKU-KBQPJGBKSA-N"     

     > **Note:**
     > - see [more about InChIKey here](http://www.inchi-trust.org/technical-faq/#13).
         
   * **smiles**
     > *type*: string
     > *value*: A SMILES string, e.g., c1ccccc1C(=O)N

     > **Note:**
     > - inclusion of SMILES string avoids the need for a registry lookup, since InChIKey's are not decodable         

### API implementation

#### Entity retrieval endpoint
   This is **required**. At minimal, you need to implement an endpoint for entity retrieval.
   
   * URL pattern should be like /<entity_type>, e.g., /gene, or /v1/gene if versioning is used.
   * GET request with an *id* URL parameter should return a single entity, e.g., /gene/1017 return gene object for 1017
   * POST request to this endpoint should do a batch query with a passed list of ids. It returns a list of matched entities.
     >POST parameter
     > - ids:    a list of ids separated by comma, e.g., "ids=1017,1018"

#### Entity query endpoint
   This is **recommended**, often **required** depending on the use cases of your API.
   
   * URL pattern should be like /query, or /v1/query if versioning is used.
   * GET request with *q* query parameter will perform a query with the input query term. e.g. /query?q=CDK2
   * POST request with *q* parameter with comma-separated query terms will perform a batch query.
     >POST parameter
     > - q:    a list of query terms separated by comma, e.g. "q=CDK2,BTK"          
     >
   * Recommended query behavior is to support both simple query like "q=CDK2" and also fielded query like "q=symbol:CDK2", even with boolean expression 'q=name:"tumor suppressor" NOT name:receptor'.     
   
#### Notes
  * More recommended API implementation guidelines can follow [BioThings API specs](http://biothings.io/specs)
  * [MyGene.info](http://mygene.info) API can serve as an example API implementation. See [its API documentation](http://mygene.info/v3/api).
  
