from GeneStore.gene_store import FanconiGeneImporter
from Modules.functional_sim import FunctionalSim
from BioLink.biolink_client import BioLinkWrapper
from OwlSim3.owlsim_wrapper import SimSearch
from Modules.ortholog_traversal import OrthologTraversal
from Modules.BiochemicalReactions import RheaMethods
from pprint import pprint
# MVP1 workflow
input_disease = 'MONDO:0019391'  # Fanconi Anemia


# Module
# blw = BioLinkWrapper()
# fa_phenotypes = blw.disease2phenotypes(disease_curie=input_disease)
# fa_phenotypes = blw.return_objects(fa_phenotypes)
#
# sim = SimSearch()
# sim.phenotype_search(phenotype_set=fa_phenotypes)
#
# pprint(sim.gene_results())

# fa_core = FanconiGeneImporter(gene_set_name='fa_core')
# orthos = OrthologTraversal(gene_set=fa_core.list_gene_ids())
# orthos.ortholog_set_by_taxid(taxon_name='mouse')

rh = RheaMethods()
#  what genes code an enzyme that produces CHEBI:17478?
pprint(rh.product2gene(chebi='CHEBI:17478'))
#  what genes code an enzyme that consumes CHEBI:17478?
pprint(rh.substrate2gene(chebi='CHEBI:17478'))


