[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ncats/translator-workflows/tree/master/WorkFlow9/master)

This is the repo for all things related to Workflow 9. The current diagram for Workflow 9 can be found [here](https://www.lucidchart.com/documents/edit/22689882-2099-4acb-961a-fa6202f2cfd8/0).

"GeneCoocurrenceByBicluster_notebook.ipynb" is the first module developed for this workflow and will serve as a template for tissue and combined tissue-gene search modules.
This notebook uses the [smartBag API service] [here](https://smartbag.ncats.io/apidocs/) or [here](https://bicluster.renci.org/apidocs/) for [RNAseqDB biclusters](https://github.com/realmarcin/MAK_results/tree/master/results/RNAseqDB) computed with the [MAK algorithm](https://www.osti.gov/biblio/1347092-massive-associative-biclustering-mak-v1).

The primary contact for this is Marcin Joachimiak (MJoachimiak@lbl.gov), with great help from Colin Curtis (ckcurtis@renci.org).

* Note - An additional notebook has been added to the repo, titled "Tissue_Coocurrence_by_Bicluster.ipynb". This is an effort to take a tissue ID and then proceed through bicluster enrichment for it. -- Colin C., Feb 5, 2019
