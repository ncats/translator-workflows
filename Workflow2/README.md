# Workflow 2 Reimagined

# Background

Workflow 2 was originally conceptualized within a Jupyter Notebook. It is now progressing 
towards a standalone Python script (WF2_automation.py) and evolving towards modular use within a 
Common Workflow Language (CWL) environment.

## TIDBITS

TIDBIT artifacts of WF2 are indexed by disease and archived under the *Tidbit* subfolder.

## Standalone Script

The commandline usage of the Python standalone script may be displayed as follows:

``` 
python WF2_automation.py --help
```

If the '--verbose' flag is used, the script dumps tabular results to the standard output ("console").
Concurrently, the Tidbit subfolder will contain HTML and JSON files. The latter (JSON) files include
an extra column called "shared_terms" which is the list of the intersection set of ontology terms 
identified during Jaccard scoring of the functional (GO term) or phenotype (HP term) overlap 
of the input gene list with the other genes listed in the given row.

## Calling the Code Directly

Examination of the standalone script reveals how to use the code directly in other software.

There is a four step process for similarity searching:

I. Due to the nature of Ontobio, we need to disable the 'cachier' cache in our application by the following:

    from ontobio.config import session
    session.config.ignore_cache = True
    
where the ontobio version we are using is a patched version (look for a version with the _ignore_cache_ flag in the
Ontobio release in the _ontobio/config.yaml_ file).

II. An _in memory_ copy of the relevant ontology and annotation catalogs plus other setup processes are 
triggered by instantiating the following three class objects:

a) ```FunctionalSimilarity('human')``` for GO molecular function and biological process comparisons.
b) ```PhenotypeSimilarity('human')``` for phenotype ontology comparisons.
c) ```GeneInteractions()``` for accessing Monarch Biolink catalog of gene interactions

Note that the object handles returned by each of the three functions are then used to call associated computations on
each kind of catalog.

Note that this catalog is used 'read-only' in the similarity comparisons so only needs to be loaded once, 
at the start of the computation'. Then the comparisons may be done:

III. Next, obtain the "seed" list of (disease) related genes for input to the comparison. This is obtained by running 
the *disease_gene_lookup()* function using the disease name and mondo identifier as input parameters.

IV.  Finally, call the model associated function - similarity() (for the FunctionalSimilarity and PhenotypeSimilarity)
or gene_interactions() (for GeneInteractions()) - with the gene list from III plus other parameters.

Repeat steps III and IV above for each disease you wish to analyze.
