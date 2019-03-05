"""Contains paths, API urls, and other configurations for module 3 of Workflow 8"""

import os 

PATHS = {
    "ddot-api-url" : "http://ddot.ucsd.edu/ddot/rest/v1/ontology/",
    "temporary-files-dir" : os.path.join(os.getcwd(), "tmp-files")
}
