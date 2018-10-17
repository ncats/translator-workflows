# Contributing to Orange Team CQ Notebooks
This document describes the Orange Team process and artifacts for creating, documenting, and implementing Competency Questions (CQs) for the NCATS-Translator project.

----------------------

### I. CQ Development Overview
Competency questions (CQs) in the domain of Fanconi Anemia (FA) are developed to help prioritize data ingest, inform data modeling, and guide architecture decisions. Query development to date has followed the four step process:  
**Stage** -> **Document** -> **Implement** - **Track**.

1. **Staging** occurs in the spreadsheets [here](https://docs.google.com/spreadsheets/d/1wbP1Ykryibcan2ZgZTOmnGp9WjcRE7nNig3akiq0PuY/edit#gid=19786600) where CQs are defined, discussed, and formalized in preparation for implementation in Jupyter notebooks. See Section II below for a description of the different sheets in this document.  _Staging in these spreadsheets is not required,  but has been useful for collaborative development and discussion of CQs before their implementation_.
  
2. **Documentation** is captured in Github readme files in the cq-notebook repo [here](https://github.com/NCATS-Tangerine/cq-notebooks).  A separate directory and readme file is created for each CQ.  Readme files *minimally* record the free-text query along with any relevant context or significance, and may additionally suggest sources and execution tasks (in particular when a domain expert wants to make suggestions for an implementing developer).  

3. **Implementation** is done in Jupyter notebooks that are stored with their readme file in the cq-notebook repo, along with any relevant data artifacts or documentation.
  
4. **Tracking** of status, ownership, and issues is done with a separate Github ticket for each implemented CQ in the cq-notebooks repository. 

When a CQ is ready for implementation, a new directory and readme file is added to the cq-notebooks repo, and a Github ticket with a `notebook-status` label created to track its progress.  As developers implement notebook(s) for this query, this ticket should be updated to report status, challenges and lessons learned, and final outcomes. 

Edits to the cq-notebooks and documents can be pushed directly by authorized users  to the Github repo (i.e. no need to fork and make a PR).

A **CQ-readme template** is located [here](https://github.com/NCATS-Tangerine/cq-notebooks/blob/master/Contributor_Docs/cq_readme_template.md).  A **notebook status ticket template** is located [here](https://github.com/NCATS-Tangerine/cq-notebooks/blob/master/Contributor_Docs/notebook_status_ticket_template.md).

----------------------

### II. CQ Staging Google Spreadsheets
Early CQ definition and staging has been documented across several spreadsheets in a Google document, as described below.

1. **Query Matrix Spreadsheets:** The original Orange Team FA CQs were created as matrices that identified key data types and variables in the FA domain and defined a query for the intersection of each.  
these include a [**Clinical Matrix spreadsheet**](https://docs.google.com/spreadsheets/d/1wbP1Ykryibcan2ZgZTOmnGp9WjcRE7nNig3akiq0PuY/edit#gid=19786600) and [**Mechanistic Matrix spreadsheet**](https://docs.google.com/spreadsheets/d/1wbP1Ykryibcan2ZgZTOmnGp9WjcRE7nNig3akiq0PuY/edit#gid=234309826).
	
2. **Query Bank Spreadsheets:**  The free-text matrix CQs are currently being assessed and staged for implementation in Jupyter notebooks.  We initially partition these queries into two query bank spreadsheets. A [**Benchmark Query Bank**](https://docs.google.com/spreadsheets/d/1wbP1Ykryibcan2ZgZTOmnGp9WjcRE7nNig3akiq0PuY/edit#gid=1337100562) spreadsheet holds 'elemental' queries representing basic retrieval and filtering operations, that can be executed to assess the scope, content, and evolution of data in the Translator system over time. An [**Other CQ Query Bank**](https://docs.google.com/spreadsheets/d/1wbP1Ykryibcan2ZgZTOmnGp9WjcRE7nNig3akiq0PuY/edit#gid=1363545460) spreadsheet holds more complex questions that may require multiple queries or computational tasks to be chained together in a workflow.

3. **Demonstrator Query Spreadsheet:** While the query banks described above aim for broad and diverse coverage of FA data types, additional CQ sets have been developed around defined FA Demonstrator projects. These  explore how the Translator system can implement data integration and computation workflows to answer important research questions.  Queries are staged in the [**FA Demonstrator spreadsheet**](https://docs.google.com/spreadsheets/d/1wbP1Ykryibcan2ZgZTOmnGp9WjcRE7nNig3akiq0PuY/edit#gid=1912684050), and demonstrator projects described in the [**cq-notebook wiki**](https://github.com/NCATS-Tangerine/cq-notebooks/wiki).

------------

Detailed instuctions for contributing to ongoing **Benchmark Query Bank** development can be found [here](https://github.com/NCATS-Tangerine/cq-notebooks/blob/master/Contributor_Docs/Query_Bank_CQ_Development.md).
