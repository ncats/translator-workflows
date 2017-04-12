## API development guidelines for NCATS translator project

This document summarizes the common guidelines we want to follow when developing new (or converting existing) APIs for the *blackboard* system, which will be used to answer the competency questions for NCATS translator project.

Just a few quick notes first:

* The response objects returned from an API should be the same entity type (a single object or a list of objects). See [entity types]() below.
* Each entity type should have a defined "_id" field. See [entity types]() below.
* An API should support both the query by _id, and batch query by a list of _id.


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
         
         
