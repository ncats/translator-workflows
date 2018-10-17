This directory holds a set of elemental **benchmarking queries** that can be executed to assess the scope, content, and evolution of data in the Translator system over time. These should be simple retrieval/filtering queries that can be executed with a minimal number of steps. Most will be framed around the **Fanconi gene sets** listed [here](https://github.com/NCATS-Tangerine/cq-notebooks/tree/master/FA_gene_sets) - but they need not be.

Benchmarking queries are being collaboratively developed and staged for implementation in the google spreadsheet [here](https://docs.google.com/spreadsheets/d/1wbP1Ykryibcan2ZgZTOmnGp9WjcRE7nNig3akiq0PuY/edit#gid=1337100562).  When a query is ready for implmentation in a Jupyter notebook, a new folder is created in this `Orange_QB1_Benchmarking` directory, and seeded with a **README file** that describes the query. An example of a README with instructions can be found [here](https://github.com/NCATS-Tangerine/cq-notebooks/blob/master/Contributor_Docs/cq_readme_template.md), and an empty template for Benchmarking query README file is below.

In addition to the README file, a **Github issue** tagged with a `notebook-status` label should be created for each notebook to track status, ownership, and outcomes.  Instructions and a template for these tickets are [here](https://github.com/NCATS-Tangerine/cq-notebooks/blob/master/Contributor_Docs/notebook_status_ticket_template.md), and a template is also included below. These tickets will enable a  dashboard-like overview of progress notebooks to be generated [here](https://github.com/NCATS-Tangerine/cq-notebooks/issues?q=is%3Aopen+is%3Aissue+label%3A%22notebook+status%22).

More information about Benchmarking Query staging and development processes can be found in the Contributor Documentation [here](https://github.com/NCATS-Tangerine/cq-notebooks/blob/master/Contributor_Docs/Query_Bank_CQ_Development.md). General information about Translator CQ development can be found [here](https://github.com/NCATS-Tangerine/cq-notebooks/blob/master/Contributor_Docs/CONTRIBUTING.md).
    

-----

# Template for QueryBank CQ README files.

## Orange QB1.4_Post_Trans_Mod

### Query:
(e.g. "What sequence features within Fanconi core complex proteins are post-translationally modified?")

### Goal:
(e.g. "A benchmarking query to assess information in the Translator system about protein post-translational modification.")

### Proposed Data Types, Sources, and Access Endpoints:
  1. ...
  2. ...
  
### Proposed Sub-Queries/Tasks:
   
**Input:** 
  1. ...
  2. ...
  3. ...

**Output:**


 
 ### Stretch Queries
 
 
 --------------------------------------------------------------------------
 
 # Template for CQ Notebook Status Tickets
 
 ### Notebook Link:  
https://github.com/NCATS-Tangerine/cq-notebooks/tree/master/Orange_Demonstrator_1_CQs/OrangeQ1.1_PPI_Network

### Implementors: 
- @kshefchek * 

(* = notebook lead)

### Status: 
- [x] Staged (described in a readme)
- [ ] Notebook started
- [ ] Notebook finished (at least one)
- [ ] Outcomes documented (in this ticket)

### Primary Knowledge Sources Used:
- (e.g. BioGrid)
- (e.g. STRING)

### APIs Used:
- (e.g. Biolink - for BioGrid, STRING)

### Notes:




