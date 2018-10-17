
# Parsing SMPDB BioPAX

This notebook contains instructions for extracting molecular relationships from pathways in the small molecule pathway database (SMPDB).  Molecular relationships are sets gene-gene, chemical-gene, and chemical-chemical relationships that make up biological pathways.  This document will take you through the steps of:
1. Downloading and installing software for parsing bioPAX files
2. Downloading BioPax files containing biological pathway information from SMPDB
3. Converting SMPDB BioPAX files to extended simple interaction format (SIF)
4. Generating node and edge tables containing molecules and molecular relationships.

To replicate this protocol as is you will need something with a Unix shell (Bash) and Java installed. This notebook was composed on a macbook pro running Bash 3.2.57 and Java 10.0.2.

## Manual Download and Inspection (Codeine Metabolism)

In this section we will download a BioPAX file and then view it in the Cytoscape browser.  BioPAX is a specification for representing biological pathway information, which you can read more about __[here](https://en.wikipedia.org/wiki/BioPAX)__.  Cytoscape is a java based program for visualizing biological pathways that you can download __[here](https://cytoscape.org/)__.

#### Download Pathway 
First, we will take a look at an example of a biological pathway file in SMPDB - specifically the codeine metabolism pathway.  The SMPDB record for the codeine metabolism pathway can be found by going to http://smpdb.ca and searching for "codeine", or by clicking __[here](http://smpdb.ca/view/SMP0000621)__.  To download the pathway information click on the "Downloads" tab in the upper right hand corner of the screen, and then click the "BioPAX" option.  Or alternatively you can just click on this __[link](http://smpdb.ca/view/SMP0000621/download?type=owl_markup)__.

#### View Pathway in Cytoscape
For this step you will need to have Cytoscape installed.  Open Cytoscape and load in the BioPAX file you just downloaded, either by dragging and dropping into the viewer window, or using the "File" menu.  You will then get a dialog popup giving you a number of options for "Model Mapping".  We are interested in both the "Default" and "SIF" options.  Be sure to view at least once using each option to get a sense of how the pathway is represented using each model type (BioPAX, SIF).  

Going forward our objective will be to convert the more complex BioPAX pathway representations to the simpler SIF format.

## Programatic Download and Parse (Codeine Metabolism)
To convert BioPAX to SIF format, we will be using a java package called __[PaxTools](https://biopax.github.io/Paxtools/)__, and running it from the command line.  For purposes of this tutorial, we will be doing everything in a new folder that we create in the home directory.

### Part 1. Setup
In this part we will download the latest version of Paxtools as well as a copy of the codeine metabolism pathway in BioPAX format using command line tools. 
##### Create Working Directory


```python
! mkdir -p ~/smpdb
```


```python
import os
os.chdir(os.path.expanduser('~/smpdb'))
```

##### Download PaxTools


```bash
%%bash
curl -L -J -O https://sourceforge.net/projects/biopax/files/latest/download
```

    curl: Saved to filename 'paxtools-5.1.0.jar'


      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100   429  100   429    0     0   1967      0 --:--:-- --:--:-- --:--:--  1976
    100   343  100   343    0     0    919      0 --:--:-- --:--:-- --:--:--   919
    100 11.8M  100 11.8M    0     0  2169k      0  0:00:05  0:00:05 --:--:-- 2473k


##### Download Pathway 


```bash
%%bash
curl -L -J -O http://smpdb.ca/view/SMP0000621/download?type=owl_markup
```

    curl: Saved to filename 'PW000597.owl'


      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100 60637    0 60637    0     0  53143      0 --:--:--  0:00:01 --:--:-- 53190


##### Sanity Check
Now we check directory contents.  You should see both the Paxtools jar and the BioPAX file


```python
! ls
```

    PW000597.owl       paxtools-5.1.0.jar


##### PaxTools CLI Documentation


```bash
%%bash
java -jar paxtools-5.1.0.jar help
```

    #logback.classic pattern: %d %-5level [%thread] %logger{25} - %msg%n
    (PaxtoolsMain Console) Available Operations:
    
    merge <file1> <file2> <output>
    	- merges file2 into file1 and writes it into output
    toSIF <input> <output> [-extended] [-andSif] ["include=SIFType,.."] ["exclude=SIFType,.."] ["seqDb=db,.."] ["chemDb=db,.."] [-dontMergeInteractions] [-useNameIfNoId] [<property_accessor> ...]
    	- converts a BioPAX model to SIF (default) or custom SIF-like text format;
    	  will use blacklist.txt (recommended) file in the current directory, if present.
    	- Include or exclude to/from the analysis one or more relationship types by 
    	  using 'include=' and/or 'exclude=', respectively, e.g., exclude=NEIGHBOR_OF,INTERACTS_WITH
    	  (mind using underscore instead of minus sign in the SIF type names; the default is to use all types).
    	- With 'seqDb=' and 'chemDb=', you can specify standard sequence/gene/chemical ID type(s)
    	  (can be just a unique prefix) to match actual xref.db values in the BioPAX model,
    	  e.g., "seqDb=uniprot,hgnc,refseq", and in that order, means: if a UniProt entity ID is found,
    	  other ID types ain't used; otherwise, if an 'hgnc' ID/Symbol is found... and so on;
    	  when not specified, then 'hgnc' (in fact, 'HGNC Symbol') for bio-polymers - 
    	  and ChEBI IDs or name (if '-useNameIfNoId' is set) for chemicals - are selected.
    	- With '-extended' flag, the output will be the Pathway Commons TXT (Extended SIF) format:
    	  two sections separated with one blank line - first come inferred SIF interactions -
    	  'A	relationship-type	B' plus RESOURCE, PUBMED, PATHWAY, MEDIATOR extra columns, 
    	  followed by interaction participants description section).
    	- If '-andSif' flag is present (only makes sense together with '-extended'), then the 
    	  classic SIF output file is also created (will have '.sif' extension).
    	- Finally, <property_accessor>... list is to specify 4th, 5th etc. custom output columns;
    	  use pre-defined column names (accessors): 
    		MEDIATOR,
    		PUBMED,
    		PMC,
    		COMMENTS,
    		PATHWAY,
    		PATHWAY_URI,
    		RESOURCE,
    		SOURCE_LOC,
    		TARGET_LOC
    	  or custom biopax property path accessors (XPath-like expressions to apply to each mediator entity; 
    	  see https://github.com/BioPAX/Paxtools/wiki/PatternBinaryInteractionFramework)
    toSBGN <biopax.owl> <output.sbgn> [-nolayout]
    	- converts model to the SBGN format and applies COSE layout unless optional -nolayout flag is set.
    validate <path> <out> [xml|html|biopax] [auto-fix] [only-errors] [maxerrors=n] [notstrict]
    	- validate BioPAX file/directory (up to ~25MB in total size, -
    	otherwise download and run the stand-alone validator)
    	in the directory using the online validator service
    	(generates html or xml report, or gets the processed biopax
    	(cannot be perfect though) see http://www.biopax.org/validator)
    integrate <file1> <file2> <output>
    	- integrates file2 into file1 and writes it into output (experimental)
    toLevel3 <input> <output> [-psimiToComplexes]
    	- converts BioPAX level 1 or 2, PSI-MI 2.5 and PSI-MITAB to the level 3 file;
    	-psimiToComplexes forces PSI-MI Interactions become BioPAX Complexes instead MolecularInteractions.
    toGSEA <input> <output> <db> [-crossSpecies] [-subPathways] [-notPathway] [organisms=9606,human,rat,..]
    	- converts BioPAX data to the GSEA software format (GMT); options/flags:
    	<db> - gene/protein ID type; values: uniprot, hgnc, refseq, etc. (a name or prefix to match
    	  ProteinReference/xref/db property values in the input BioPAX model).
    	-crossSpecies - allows printing on the same line gene/protein IDs from different species;
    	-subPathways - traverse into sub-pathways to collect all protein IDs for a pathway.
    	-notPathway - also list those protein/gene IDs that cannot be reached from pathways.
    	organisms - optional filter; a comma-separated list of taxonomy IDs and/or names
    
    fetch <input> <output> [uris=URI1,..] [-absolute] 
    	- extracts a self-integral BioPAX sub-model from file1 and writes to the output; options:
    	uri=... - an optional list of existing in the model BioPAX elements' full URIs;
    	-absolute - set this flag to write full/absolute URIs to the output (i.e., 'rdf:about' instead 'rdf:ID').
    getNeighbors <input> <id1,id2,..> <output>
    	- nearest neighborhood graph query (id1,id2 - of Entity sub-class only)
    summarize <input> <output> [--model] [--pathways] [--hgnc-ids] [--uniprot-ids] [--chebi-ids]
    	- (experimental) summary of the input BioPAX model;
     	runs one or several analyses and writes to the output file;
     	'--model' - (default) BioPAX classes, properties and values summary;
     	'--pathways' - pathways and sub-pathways hierarchy;
     	'--hgnc-ids' - HGNC IDs/Symbols that occur in sequence entity references;
     	'--uniprot-ids' - UniProt IDs in protein references;
     	'--chebi-ids' - ChEBI IDs in small molecule references;
     	'--uri-ids' - URI,type,name(s) and standard identifiers (in JSON format) for each physical entity;
     	the options' order defines the results output order.
    blacklist <input> <output>
    	- creates a blacklist of ubiquitous small molecules, like ATP, 
    	from the BioPAX model and writes it to the output file. The blacklist can be used with
     	paxtools graph queries or when converting from the SAME BioPAX data to the SIF formats.
    pattern 
    	- BioPAX pattern search tool (opens a new dialog window)
    help 
    	- prints this screen and exits
    
    Commands can also use compressed input files (only '.gz').
    


### Part 2. Parsing with PaxTools CLI
Provided sanity checks come back clean, we now take a look at the BioPAX command line usage information.

##### Generate Blacklist
We are not interested in frequently occurring cosubstrates and metabolites like ATP, Water, NAD, etc.  Fortunately PaxTools has built in functionality for creating blacklists of these uninteresting metabolites to ignore when parsing the file.  Be sure to check out both the documentation above for the ```blacklist``` and ```toSIF``` commands to see how the blacklist is being used.


```bash
%%bash
java -jar paxtools-5.1.0.jar blacklist PW000597.owl blacklist.txt
```

    #logback.classic pattern: %d %-5level [%thread] %logger{25} - %msg%n


##### Convert BioPAX To Extended SIF
Now that we have generated out blacklist file, we are ready to convert BioPAX to extended SIF format.


```bash
%%bash
java -jar paxtools-5.1.0.jar toSIF PW000597.owl PW000597 \
-extended -andSif -useNameIfNoId \
'seqDb=uniprot' 'chemDb=CHEBI,HMDB,KEGG'
```

    #logback.classic pattern: %d %-5level [%thread] %logger{25} - %msg%n


Now there is a lot going on in the preceeding command.  The first list calls the toSIF utility and specifies the input and output files.  The `extended`, `andSIF`, and `useNameIfNoId` flags on the second line tell the utility to output the files in extended SIF format, also return a normal SIF file, and use chemical or gene names in the output files if no other identifiers are present in the original BioPAX file.  Finally, the ```seqDb``` and ```chemDb``` arguments tell the utility which identifiers it should use (in order of preference) to generate the output file.  So for example, the utility will default to using CHEBI IDs for chemicals, but will use an HMDB ID or if no CHEBI ID is present in the BioPAX file, and a KEGG ID if neither a CHEBI ID or HMDB ID is present.

##### Parse Extended SIF file
The extended SIF file contains two parts, separate by a line of blank space.
1. An edge table containing information about the relationships between molecules (chemicals and genes)
2. A node table containing information about the molecule (chemicals and genes) in the pathway 

Because we already have the relationship information in much cleaner form in the normal SIF file, we only want to keep the node table.  We can use `awk` to split on the blank line and keep only the part that comes after.


```bash
%%bash
awk -v RS=  'NR==2{ print }' PW000597 > PW000597.txt
```

##### Sanity Check
As a quick sanity check we will list the files in the directory.  We should see a `PW000597.sif` file (normal SIF file), and well as a `PW000597` file with no extension (extended SIF file) along with the input file `PW000597.owl` and blacklist file `blacklist.txt`.


```python
!ls
```

    PW000597           PW000597.sif       blacklist.txt
    PW000597.owl       PW000597.txt       paxtools-5.1.0.jar



```python
!head PW000597.sif
```

    CHEBI:15379	reacts-with	CHEBI:16714
    CHEBI:15379	used-to-produce	CHEBI:16842
    CHEBI:15379	used-to-produce	CHEBI:17303
    CHEBI:15379	used-to-produce	HMDB0060657
    CHEBI:15379	consumption-controlled-by	P08684
    CHEBI:15379	consumption-controlled-by	P10635
    CHEBI:16714	used-to-produce	CHEBI:16842
    CHEBI:16714	reacts-with	CHEBI:17200
    CHEBI:16714	used-to-produce	CHEBI:17303
    CHEBI:16714	used-to-produce	CHEBI:17659



```python
!head PW000597.txt
```

    PARTICIPANT	PARTICIPANT_TYPE	PARTICIPANT_NAME	UNIFICATION_XREF	RELATIONSHIP_XREF
    P16662	ProteinReference	UDP-glucuronosyltransferase 2B7	UniProt:P16662	
    HMDB0060464	SmallMoleculeReference	Codeine-6-glucuronide	CAS:20736-11-2;ChemSpider:4590054;HMDB:HMDB0060464;KEGG Compound:C16577;PubChem-compound:5489029	
    CHEBI:15379	SmallMoleculeReference	Oxygen	BioCyc:CPD-6641;CAS:7782-44-7;ChEBI:CHEBI:15379;ChemSpider:952;HMDB:HMDB0001377;KEGG Compound:C00007;PubChem-compound:977	
    CHEBI:16842	SmallMoleculeReference	Formaldehyde	BioCyc:FORMALDEHYDE;CAS:50-00-0;ChEBI:CHEBI:16842;ChemSpider:692;HMDB:HMDB0001426;KEGG Compound:C00067;PubChem-compound:712	
    CHEBI:17303	SmallMoleculeReference	Morphine	CAS:57-27-2;ChEBI:CHEBI:17303;ChemSpider:4450907;HMDB:HMDB0014440;KEGG Compound:C01516;PubChem-compound:5288826	
    P10635	ProteinReference	Cytochrome P450 2D6	UniProt:P10635	
    CHEBI:17200	SmallMoleculeReference	Uridine diphosphate glucuronic acid	BioCyc:UDP-GLUCURONATE;CAS:2616-64-0;ChEBI:CHEBI:17200;ChemSpider:16522;HMDB:HMDB0000935;KEGG Compound:C00167;PubChem-compound:17473	
    P08684	ProteinReference	Cytochrome P450 3A4	UniProt:P08684	
    HMDB0060657	SmallMoleculeReference	Norcodeine	CAS:467-15-2;ChemSpider:8101508;HMDB:HMDB0060657;KEGG Compound:C16576;PubChem-compound:9925873	


### To Be Continued...


```python

```
