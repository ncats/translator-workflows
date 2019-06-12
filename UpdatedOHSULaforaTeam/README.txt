##OHSU Lafora Team May/June 2019:

###Automated work

Our automation script:
Lafora_team_final_automation.py

To run our query:
Run run_final.sh (bash script)

Examples of CSV output:
Lafora_BriefSummary.csv 
Lafora_DescriptiveSummary.csv

New Module used in our automation script: Summary_mod.py
The purpose of this script is to create an class to aggregate and display summary data from the automated modules.

Changes to Modules:
generic_similarity.py: also returns a list of the shared labels (human-interpretable labels of the GO terms shared between two genes)
Mod1E_interactions.py: changed the score returned for each interaction to 1 (so it's a count of the interactions). It was 0 before. 

###Enrichment Work: AddingLaforaEnrichment subdirectory
Uses output from ShinyGO, stored in ShinyGOFiles subdirectory
Run python script ShinyGOProcessing.py to create CSVs of output-input pairs with associated enriched terms from Mod1A and Mod1B. 
	FunctEnrichedLaforaOutput.csv and PhenoEnrichedLaforaOutput.csv.
Run python script LaforaEnrichedSummary.py to create final descriptive summary table used by our team
	EnrichedDescLaforaSummary.csv 

###Older work: OlderScripts subdirectory
Writer information: CX is Colleen Xu, JG is Jacob Gutierrez. 
This directory holds the older scripts that we wrote. Before running them, check and change path information so they can access all imported modules correctly. JG files used pickle-output stored in the data subdirectory. 

