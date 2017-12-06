# cq-notebooks

Notebooks for answering competency questions

Our goal here is to create a catalog of working examples that demonstrate how to access, transform, integrate and visualize the diverse data sources we intend to use for projects like Translator.

We are currently using Jupyter notebooks as our means of documenting, prototyping, and sharing code. As some of these experiments mature into working prototype pipelines, we intend to extract this functionality from the notebooks and migrate it into a production pipeline.

## Workplan

Orange team queries are initially collected in the spreadsheet [here](http://bit.ly/orange_cq), with tabs for different collections of notebooks (e.g. demonstrator-driven queries, general benchmarking queries). From this staging area, select queries are implemented in Jupyter or Zeppelin notebooks. A detailed overview of spreadsheet contents and the workflow for CQ development can be found in the documents [here](https://github.com/NCATS-Tangerine/cq-notebooks/blob/master/Contributor_Docs/CONTRIBUTING.md) and [here](https://github.com/NCATS-Tangerine/cq-notebooks/blob/master/Contributor_Docs/Query_Bank_CQ_Development.md).

Notebooks under active development each have an associated directory in this repo that includes the notebook itself, a descriptive README, and any associated code or data. For each notebook, a Github ticket is also created and tagged with a `notebook-status` label to track its status, ownership, and outcomes. These tickets enable a dashboard-like overview of progress notebooks to be generated [here](https://github.com/NCATS-Tangerine/cq-notebooks/issues?q=is%3Aopen+is%3Aissue+label%3A%22notebook+status%22).



## Running Locally

### One-time Setup

You will need Python (e.g., Python 3.5.2).

```
virtualenv env
source env/bin/activate
pip install jupyter ipython pandas requests
```

### Running

```
source env/bin/activate
jupyter notebook
```


## APIs

[API development guidelines](API_dev_guidelines.md)

TODO: we should aim to drive this list from Smart API registry

### Live

 * Pharos https://pharos.nih.gov/ (Purple) - drug info
 * Ginas http://ginas.ncats.nih.gov (Purple) - substances
 * BioLink https://api.monarchinitiative.org/api/ (Orange)
 * BioThings API for genes: [MyGene.info](http://mygene.info) (Orange)
 * BioThings API for variants: [MyVariant.info](http://myvariant.info) (Orange)
 * BioThings API for drugs/Compounds: http://c.biothings.io (Orange)
 * BioThings API for taxonomy: http://t.biothings.io (Orange)
 * Wikidata SPARQL (Orange)
 * DGIdb API for drug-gene interactions: http://dgidb.genome.wustl.edu/api

### Next

 * Exposure API - scores for locations (Green) - https://exposures.renci.org/v1/ui/#!/default
 * Synthetic patient data API (Green)
 * Synthetic patient data API (Orange)

### Hackathon

 * Disease prediction (Grey)
