# Troubleshooting the WF_automation.py script

Iterations to debug the script uncovered a few grubs under rocks:

## Script runs in PyCharms without Modules relative paths

PyCharms complains about the missing "Modules" subfolder, 
Adding a period '.' in front of the "Modules" name clears this issue but triggers a '__main__ is not a package" issue. 

This seems to be a PyCharms quirk since the script otherwise finds its modules locally when running: when the 
script runs, those modules get imported without an error.

## (As of May 21st, 2019) the mygenes pip (pypi) module is outdated

... and has an empty **mygenes.py/mygenes/\_\_init\_\_.py** file, which was filled in December 2018 (but the pypi not updated?) 
so *pip* installation of _mygenes.py_ module doesn't work. The hacky workaround is to cut-and-paste the missing text
from the master repository, into the **\_\_init.py\_\_** file.

Resolved: we applied the change recommended in https://github.com/biothings/mygene.py/issues/7
