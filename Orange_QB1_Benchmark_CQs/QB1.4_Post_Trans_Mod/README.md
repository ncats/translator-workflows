## Orange QB1.4

### Query:
Return sequences of FA genes associated with functional post-translational modifications.

#### Refined Query:
What sequence features within the BRCA2 protein are post-translationally modified?

### Goal:
A benchmarking query to assess information in the Translator system about protein post-translational modification. 

### Notes:
Different sources may provide PTM data with different levels of evidence.  E.g. some curate literature for experimentally-supported modifications, others may give computationally predicted sites that have not been experimentally validated.

**Uniprot** ([link](http://www.uniprot.org/uniprot/P51587#ptm_processing))

Uniprot contains information about modified residues on a protein. Example [entry](http://www.uniprot.org/uniprot/P51587.xml):
```
<feature type="modified residue" description="Phosphoserine" evidence="4">
<location><position position="70"/></location>
</feature>
```
where evidence 4 is:
```
<evidence key="4" type="ECO:0000244">
<source><dbReference type="PubMed" id="23186163"/></source>
</evidence>
```

You can also get the same information from the [proteins endpoint](http://www.ebi.ac.uk/proteins/api/doc/) [here](https://www.ebi.ac.uk/proteins/api/features?offset=0&size=100&accession=P51587&categories=PTM).

These do not contain any information about the functional significance of the PTMS. This information is often in text ("Phosphorylation by CHEK1 and CHEK2 regulates interaction with RAD51 ... etc ... "). It does contain evidence code to differentiate between experimentally supported and computationally predicted sites.

**iPTMnet**
iPTMnet (can) contain more [information](http://research.bioinformatics.udel.edu/iptmnet/about).

For [BRCA2](http://research.bioinformatics.udel.edu/iptmnet/entry/P51587/) it contains information about: PTM Enzyme (enzyme performing the PTM), additional PTMs from other sources,
PTM-dependent PPI, and Proteoform PPIs.



### Proposed Data Types, Sources, and Access Endpoints:
  1. ...
  2. ...
  
### Proposed Sub-Queries/Tasks:
   
**Input:** 
  1. ...
  2. ...
  3. ...

**Output:**

 -----
 
 ### Stretch Queries
