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

These do not contain any information about the functional significance of the PTMS. This information is often in text ("Phosphorylation by CHEK1 and CHEK2 regulates interaction with RAD51 ... etc ... "). It does contain evidence code to differentiate between experimentally supported and computationally predicted sites. Sometimes, the description containes text like "Phosphoserine; by CDK1 and CDK2", so the PTM enzyme can possibly be parsed out.

**iPTMnet**

iPTMnet (can) contain more [information](http://research.bioinformatics.udel.edu/iptmnet/about).
But... None of the download links work!!!

For [BRCA2](http://research.bioinformatics.udel.edu/iptmnet/entry/P51587/) it contains information about: PTM Enzyme (enzyme performing the PTM), additional PTMs from other sources,
PTM-dependent PPI, and Proteoform PPIs.

Completeness assessment (compared to text from uniprot summary):

- "Phosphorylated by ATM upon irradiation-induced DNA damage" : No
- "Phosphorylation by CHEK1 and CHEK2 regulates interaction with RAD51": "Phosphorylation	P51587 (BRCA2)	S3291	Q06609 (RAD51)	inhibitedassociation	efip	22084686" and "T3387	Phosphorylation	O14757 (CHEK1)" and "T3387	Phosphorylation	O96017 (CHEK2)". These entries aren't explicity linked though..
- "Phosphorylation at Ser-3291 by CDK1 and CDK2 is low in S phase when recombination is active, but increases as cells progress towards mitosis; this phosphorylation prevents homologous recombination-dependent repair during S phase and G2 by inhibiting RAD51 binding.": "S3291	Phosphorylation	P06493 (CDK1)", "S3291	Phosphorylation	P24941 (CDK2)", "Phosphorylation	P51587 (BRCA2)	S3291	Q06609 (RAD51)	inhibitedassociation". This complex relationship isn't captured though
- "Ubiquitinated in the absence of DNA damage; this does not lead to proteasomal degradation. In contrast, ubiquitination in response to DNA damage leads to proteasomal degradation": It has Ubiquitination sites listed, but no outcome or response is indicated.





### Proposed Data Types, Sources, and Access Endpoints:
  1. Uniprot Proteins endpoint: http://www.ebi.ac.uk/proteins/api/doc/
  2. iPTMnet: http://research.bioinformatics.udel.edu/iptmnet (No programmatic access, download links down. Sent email inquiring Jun 28th 2017)
  
### Proposed Sub-Queries/Tasks:
   
  1. Retrieve PTMs on BRCA2, including: PTM type (phosphoserine, phosphorylation, etc.), location/residue, determination method (ECO), evidence (PubMed Id)
  2. Retrieve PTM enzymes, PTM-dependent PPIs (not possible at the moment)
  3. ...

 
 ### Stretch Queries
