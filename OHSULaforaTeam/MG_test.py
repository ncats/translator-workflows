
## Little throwaway script to demonstrate summary_module functionality

# import libraries
import sys
import shutil
from os import makedirs
import requests
import pandas as pd
from html3.html3 import XHTML

# Adjust path to find custom modules
if '/' in sys.executable:
    pyptha = sys.executable.split('/')
    pyptha[-2]= 'lib'
else:
    pyptha = sys.executable.split('\\')
    pyptha[-2] = 'lib'
pypth='/'.join(pyptha) + '*/site-packages'

# Hack to get around problematic updating of distutils installed PyYAML and a 
# slightly older pandas requiring a compatible numpy
shutil.rmtree(pypth + '/PyYAML*', ignore_errors=True)
shutil.rmtree(pypth + '/numpy*', ignore_errors=True)

sys.path.append("../mvp-module-library")
# Install pip requirements
#!{sys.executable} -m pip install -r requirements.txt

print(pypth)

from Modules.Summary_mod import Summary_mod

# Python 2 vs Python 3 Pickle:
try:
	import _pickle as cPickle
except:
	import cPickle

# Create new Summary_mod object
my_sum = Summary_mod()

# Open pickled objects corresponding to
# - Mod1a results
# - Mod1b results
# - Mod1e results
fh = open("mod1a_pickle.dat","rb")
mod1a_pickle = cPickle.load(fh)
fh.close()

fh = open("mod1b_pickle.dat","rb")
mod1b_pickle = cPickle.load(fh)
fh.close()

fh = open("mod1e_pickle.dat","rb")
mod1e_pickle = cPickle.load(fh)
fh.close()




print("1a")
print(mod1a_pickle.to_string())
print("1b",mod1b_pickle.to_string())
#print(intput_genes_pickle)
print("---------------------------------")

# Add mod1a results to my_sum
my_sum.add1A(mod1a_pickle)

# Print brief and descriptive tables to console
my_sum.get_all()

# Add mod1b results to my_sum
my_sum.add1B(mod1b_pickle)

# Print brief and descriptive tables to console
my_sum.get_all()

# Write brief and descriptive tables to csv and json
my_sum.write_all()
my_sum.write_json()