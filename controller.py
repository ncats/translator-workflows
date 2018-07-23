from GeneStore.gene_store import FanconiGeneImporter
from Modules.functional_sim import FunctionalSim
from BioLink.biolink_client import BioLinkWrapper
from OwlSim3.owlsim_wrapper import SimSearch
from pprint import pprint

# MVP1 workflow
input_disease = 'MONDO:0019391'  # Fanconi Anemia

phenotype_blacklist = ['HP:0025023']

blw = BioLinkWrapper()
fa_phenotypes = blw.disease2phenotypes(disease_curie=input_disease)
fa_phenotypes = blw.return_objects(fa_phenotypes)
for elem in phenotype_blacklist:
    fa_phenotypes.remove(elem)
sim = SimSearch()
diseases = sim.phenotypes2disease(phenotype_set=fa_phenotypes)

pprint(diseases['disease_curies'])


