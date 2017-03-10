# cq-notebooks
Notebooks for answering competency questions

## Workplan

For now, see the formalized query tab in:
http://bit.ly/fanconi-cq

We may transfer these to github tickets later, and use github projects as a kanban-style way of organizing this.

Each row should link to a notebook demonstrating CQ answering (or lack of answering, where we are identifying gaps). The notebook may be jupyter, zeppelin, ... We may choose to use mybindings to allow editing of these in future.


## Running Locally

### Setup

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

### Live

 * Pharos https://pharos.nih.gov/ (Purple) - drug info
 * Ginas http://ginas.ncats.nih.gov (Purple) - substances
 * BioLink https://api.monarchinitiative.org/api/ (Orange)
 * Biothings (Orange)

### Next

 * Exposure API (Green)
 * Synthetic patient data API (Green)
 * Synthetic patient data API (Orange)

### Hackathon

 * Disease prediction (Grey)
