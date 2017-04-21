# cq-notebooks

Notebooks for answering competency questions

Our goal here is to create a catalog of working examples that demonstrate how to access, transform, integrate and visualize the diverse data sources we intend to use for projects like Translator.

We are currently using Jupyter notebooks as our means of documenting, prototyping, and sharing code. As some of these experiments mature into working prototype pipelines, we intend to extract this functionality from the notebooks and migrate it into a production pipeline.

## Workplan

For now, we are collecting orange-team queries here:
http://bit.ly/orange_cq

We may transfer these to github tickets later, and use github projects as a kanban-style way of organizing this.

Each row should link to a notebook demonstrating CQ answering (or lack of answering, where we are identifying gaps). The notebook may be jupyter, zeppelin, ... We may choose to use mybindings to allow editing of these in future.


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
