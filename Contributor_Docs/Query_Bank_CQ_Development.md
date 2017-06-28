# Orange Team Query Bank Development

### Overview
Benchmarking CQs are 'elemental' queries that can be executed to assess the scope, content, and evolution of data in the Translator system over time.  A set of benchmark queries is being staged in the [**Benchmark Query Bank**](https://docs.google.com/spreadsheets/d/1wbP1Ykryibcan2ZgZTOmnGp9WjcRE7nNig3akiq0PuY/edit#gid=1337100562) spreadsheet, seeded by queries from the original [**Mechanistic CQ Matrix**](https://docs.google.com/spreadsheets/d/1wbP1Ykryibcan2ZgZTOmnGp9WjcRE7nNig3akiq0PuY/edit#gid=234309826). Matrix queries are first refined into clear, precise, elemental questions. Next, knowledge sources and access endpoints required to address each question are identified and evaluated. Finally, the questions are translated into one or more 'executable' formats (e.g. an API call, cypher or sparql query). 

Part of the query refinement task is assessing suitability of the query for benchmarking purposes. Questions that are too complex for this use case can be recast as one or more simpler retrieval/filtering level queries and kept in this spreadsheet. The original query can be copied into the [**Complex Query Bank**](https://docs.google.com/spreadsheets/d/1wbP1Ykryibcan2ZgZTOmnGp9WjcRE7nNig3akiq0PuY/edit#gid=1363545460) spreadsheet where it can be further specified and staged for implementation. Any new/additional complex queries that come to  mind can be recorded in this sheet as well.

### Workplan
- General CQ development practices are defined [here](https://github.com/NCATS-Tangerine/cq-notebooks/blob/master/CONTRIBUTING.md). 
- Translator team members can work asynchronously to curate and prepare queries in the Query Bank spreadsheets. 
- In addition, we hold weekly calls to discuss queries and progress (Thursdays, 2PM PT, http://bit.ly/devzoom). 
- Once a particular query is ready for implementation, a developer can take ownership and move the work to Github (i.e make a readme file, a create a cq-status ticket, and begin a Jupyter notebook).


### Benchmark Query Bank Spreadsheet Column Definitions
- **ID:**  A prefixed numerical identifier for the query
- **Original Query:** The original query as written in the matrix spreadsheet is copied into this column.
- **Refined Query:** The original query is re-written in more precise language, and scoped for benchmarking purposes.

- **Supported?:** Indicate if the query is currently supported by sources in the Translator System
- **Benchmark?:** Indicate if the original matrix question is elemental enough to serve as a Benchmarking query (once all queries have been refined and all non-benchmark queries transferred, this column can be removed)
- **Primary KS (in system):**  Indicate primary knowledge sources in the Translator System that support this query
- **Primary KS (not in system):** Indicate primary knowledge sources not (yet) in the Translator System that would support this query 
- **Access Endpoint/API:** API(s) that serve data supporting the query

- **Executable Query:** Formalized query executable at the indicated endpoint.
- **Assignee:** Person leading notebook implementation


### Glossary

1. **Primary Knowledge Source (KS):** The original knowledge/data source that initially collected, curated, and provisioned data that may be ingested/aggregated in larger systems (e.g. ClinVar, Bgee, MGI, CTD, Ensemble, CIViC)
2. **Access Endpoint:**  an API or service from which information can be obtained and operated on to support query answering or computational analysis tasks (e.g. Monarch, Wikidata, Biothings are endpoints developed by Translator team, while Pharos, Ensembl, CIViC endpoints are externally developed.  Note that APIs correspond to a single Primary KS while others integrated and serve information from many primary KSs.
4. **Translator System:** The set of all Access Endpoints and Services that can be used dynamically to answer questions. Includes systems developed by our teams and external teams (e.g. Monarch, Wikidata, Biothings, synthetic data APIs), and those developed externally (e.g. Ensemble, Pharos, CIViC).  Ideally, all Access Endpoints are registered with smartAPI and wrapped in a Knowledge Beacon.
