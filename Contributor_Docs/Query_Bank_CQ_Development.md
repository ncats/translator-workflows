# Orange Team Query Bank Development

### Overview
Benchmarking CQs are 'elemental' queries that can be executed to assess the scope, content, and evolution of data in the Translator system over time. These should be simple retrieval/filtering queries that can be executed with a minimal number of steps. Most will be framed around the **Fanconi gene sets** listed [here](https://github.com/NCATS-Tangerine/cq-notebooks/tree/master/FA_gene_sets) - but they need not be. A set of benchmark queries is being staged in the [**Benchmark Query Bank**](https://docs.google.com/spreadsheets/d/1wbP1Ykryibcan2ZgZTOmnGp9WjcRE7nNig3akiq0PuY/edit#gid=1337100562) spreadsheet, seeded by queries from the original [**Mechanistic CQ Matrix**](https://docs.google.com/spreadsheets/d/1wbP1Ykryibcan2ZgZTOmnGp9WjcRE7nNig3akiq0PuY/edit#gid=234309826). Column definitions for this spreadsheet are below.


### Workplan
1. **Query Staging:** Matrix queries are first refined into clear, precise, elemental questions in the [**Benchmark Query Bank**](https://docs.google.com/spreadsheets/d/1wbP1Ykryibcan2ZgZTOmnGp9WjcRE7nNig3akiq0PuY/edit#gid=1337100562) spreadsheet. Part of the query refinement task is assessing suitability of the query for benchmarking purposes. Questions that are too complex for this use case can be recast as one or more simpler retrieval/filtering level queries and kept in this spreadsheet. The original query can be copied into the [**Other CQ Query Bank**](https://docs.google.com/spreadsheets/d/1wbP1Ykryibcan2ZgZTOmnGp9WjcRE7nNig3akiq0PuY/edit#gid=1363545460) spreadsheet where it can be further specified and staged for implementation. Other key tasks documented in the staging spreadsheet is identification and evaluation of knowledge sources and access endpoints required to address each query, and optionally translating queries into one or more 'executable' formats (e.g. an API call, cypher or sparql query). 
  
2. **Query Implementation:** When a query is ready for implmentation in a Jupyter notebook, a new folder is created in the [**Orange_QB1_Benchmark CQ**](https://github.com/NCATS-Tangerine/cq-notebooks/tree/master/Orange_QB1_Benchmark_CQs) directory, and seeded with a **README file** that describes the query. An example of a README with instructions can be found [here](https://github.com/NCATS-Tangerine/cq-notebooks/blob/master/Contributor_Docs/cq_readme_template.md).
  
3. **Query Tracking:**  In addition to the README file, a **Github issue** tagged with a `notebook-status` label is created for each notebook to track status, ownership, and outcomes.  Instructions and a template for these tickets are [here](https://github.com/NCATS-Tangerine/cq-notebooks/blob/master/Contributor_Docs/notebook_status_ticket_template.md). These tickets will enable a  dashboard-like overview of progress notebooks to be generated [here](https://github.com/NCATS-Tangerine/cq-notebooks/issues?q=is%3Aopen+is%3Aissue+label%3A%22notebook+status%22).
  
4. **Collaboration:**  Translator team members can work asynchronously to curate and prepare queries in the Query Bank spreadsheets, and implement in notebooks. In addition, we hold weekly calls to discuss queries and progress (Thursdays, 2PM PT, http://bit.ly/devzoom). General CQ development practices are defined [here](https://github.com/NCATS-Tangerine/cq-notebooks/blob/master/Contributor_Docs/CONTRIBUTING.md). 

### Benchmark Query Bank Spreadsheet Column Definitions
- **ID:**  A prefixed numerical identifier for the query
- **Original Query:** The original query as written in the matrix spreadsheet is copied into this column.
- **Refined Query:** The original query is re-written in more precise language, and scoped for benchmarking purposes.

- **Supported?:** Indicate if the query is currently supported by sources in the 'Translator System' (defiend below)
- **Benchmark?:** Indicate if the original matrix question is elemental enough to serve as a Benchmarking query (once all queries have been refined and all non-benchmark queries transferred, this column can be removed).
- **Primary KS (in system):**  Indicate 'primary' knowledge sources that can support this query and are in the Translator System (i.e. can be dynamically accessed - either from a native/source API or one of the Translator APIs such as Monarch, Wikidata, or BioThings). 
- **Primary KS (not in system):** Indicate 'primary' knowledge sources that would support this query which are not (yet) in the Translator System t (i.e. not dynamically accessible from some API endpoint).
- **Access Endpoint/API:** API(s) that serve data supporting the query.
- **Executable Query:** Formalized query executable at the indicated endpoint.
- **Owner:** Person leading notebook implementation.


### Glossary

1. **Primary Knowledge Source (KS):** The original knowledge/data source that initially collected, curated, and provisioned data that may be ingested/aggregated in larger systems (e.g. ClinVar, Bgee, MGI, CTD, Ensemble, CIViC)
2. **Access Endpoint:**  an API or service from which information can be obtained and operated on to support query answering or computational analysis tasks (e.g. Monarch, Wikidata, Biothings are endpoints developed by Translator team, while Pharos, Ensembl, CIViC endpoints are externally developed.  Note that APIs correspond to a single Primary KS while others integrated and serve information from many primary KSs.
3. **Translator System:** The set of all Access Endpoints and Services that can be used dynamically to answer questions. Includes systems developed by our teams and external teams (e.g. Monarch, Wikidata, Biothings, synthetic data APIs), and those developed externally (e.g. Ensemble, Pharos, CIViC).  Ideally, all Access Endpoints are registered with smartAPI and wrapped in a Knowledge Beacon.
