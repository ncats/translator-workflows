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

There is a three step process for similarity searching:

*Setup:* Load the _in memory_ ontology and annotation catalog by creating the relevant object:
a) ```FunctionalSimilarity()``` for GO molecular function and biological process comparisons.
b) ```PhenotypeSimilarity()``` for phenotype ontology comparisons.

Note that this catalog is used 'read-only' in the similarity comparisons so only needs to be loaded once, 
at the start of the computation'. Then the comparisons may be done:

1. First, obtain the "seed" list of (disease) related genes for input to the comparison.
2. Second, call the similarity() function with the seed list.

Repeat steps 1 and 2 above for each disease you wish to analyze.
