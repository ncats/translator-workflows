[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ncats/translator-workflows/master)

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
If you do not have pip installed, you can install it with following command:
```
sudo easy_install pip
```
Once you have pip, run the following commands for first time setup

```
virtualenv env
source env/bin/activate
pip install jupyter ipython pandas requests
```

### Running
After the initial setup, you only need to execute the commands below to bring up the notebooks

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
 * Jaspar SPARQL endpoint: https://tfbsmotif.ncats.io/blazegraph/#query 
 * Clinical profiles API: [HAPI FHIR](https://hapi.clinicalprofiles.org/) (Orange)
    * [Demo use](https://github.com/translational-informatics/TransMed-Clinical-Profiles/blob/master/using-profiles/Downloading%20EDS%20Profiles%20from%20clinicalprofiles.org.ipynb)

### Next

 * Exposure API - scores for locations (Green) - https://exposures.renci.org/v1/ui/#!/default
 * Synthetic patient data API (Green)

### Hackathon

 * Disease prediction (Grey)


# Translator TIDBITS Workflows

This is where the TIDBITS Workflows can be stored and edited.

In particular, you can use this git repository to track issues related to a given workflow.

## One-time Setup

Upon git cloneing the project, you need to configure the mvp-modules-library git submodule:

   $ git submodule init
   
Every time you git pull an update of the system, you may wish to also:

   $ git submodule update
   
