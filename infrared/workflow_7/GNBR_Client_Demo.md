
# GNBR Query Notebook

This notebook has code stubs showing how to query GNBR REST API using the client library.  It is meant to serve as general repository of starter code stubs that can be copied and then modified for various applications.  This library will be updated as changes are made to the RESY API and client.

## Client installation
The GNBR python library can be installed using the python package manager (pypi).  I recommend installing in a virtual environemnt as the clent library will be subject to frequent modification. This way you won't get any wierd package dependency conflicts. If you already have a virtual environment set up, you can skip the following section.

##### Set Up Virtual Environment
To set up a virtual environment make sure that you have virtualenv installed in whatever version of python you are using (Python 3+ recommended).  Note that this example assumes you are using bash unix, and uses the user's home directory as root. 

Open a terminal window and enter the following commands to create a directory for your virtual environments.

```sh
cd ~
mkdir virtual-environments
```

Enter the following command to create a virtual environment.

```sh
virtualenv gnbr-client
```

Activate the virtual environment and upgrade the pip package manager

```sh
cd gnbr-client
source bin/activate
pip install --upgrade pip
```

##### Install the Client Libaray
Use the pip package manager to install the gnbr-client package.

```sh
pip install git+https://github.com/NCATS-Infrared/gnbr-client-python.git
```

More detailed instructions for installation and testing along with usage documentmentation can be found in the gnbr-client [github repository](https://github.com/NCATS-Infrared/gnbr-client-python).

## Testing Endpoints

##### Lookup Concept by Name


```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ConceptsApi()
keywords = ['Codeine'] # list[str] | (Optional) array of keywords or substrings against which to match concept names and synonyms (optional)

try:
    api_response = api_instance.get_concepts(keywords=keywords)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConceptsApi->get_concepts: %s\n" % e)
```

    [{'categories': ['Entity', 'Chemical'],
     'description': None,
     'id': 'MESH:D003061',
     'name': 'codeine'}]


##### Lookup Concept by ID


```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# create an instance of the API class
api_instance = swagger_client.ConceptsApi()
concept_id = 'MESH:D003061' # str | (url-encoded) CURIE identifier of concept of interest

try:
    api_response = api_instance.get_concept_details(concept_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConceptsApi->get_concept_details: %s\n" % e)
```

    {'categories': ['Chemical', 'Entity'],
     'description': None,
     'details': None,
     'exact_matches': None,
     'id': 'MESH:D003061',
     'name': 'codeine',
     'symbol': None,
     'synonyms': ['codeine',
                  'Codeine',
                  'codeine phosphate',
                  'N-methylmorphine',
                  'Codeine phosphate',
                  'N-methyl morphine',
                  'codeine/dextropropoxyphen'],
     'uri': 'MESH:D003061'}


##### Get Statements


```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# create an instance of the API class
api_instance = swagger_client.StatementsApi()
s = ['MESH:D003061'] # str | (url-encoded) CURIE identifier of concept of interest

try:
    api_response = api_instance.get_statements(s=s)
    pprint(api_response[0])
except ApiException as e:
    print("Exception when calling ConceptsApi->get_concept_details: %s\n" % e)
```

    {'id': '37580296',
     'object': {'categories': ['Entity', 'Gene'],
                'id': 'ncbigene:81668',
                'name': 'growth_hormone'},
     'predicate': {'edge_label': 'affects expression of',
                   'negated': None,
                   'relation': 'affects expression'},
     'subject': {'categories': ['Entity', 'Chemical'],
                 'id': 'MESH:D003061',
                 'name': 'codeine'}}


##### Get Supporting Evidence


```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.StatementsApi()
statement_id = '37580296' # str | (url-encoded) CURIE identifier of the concept-relationship statement (\"assertion\", \"claim\") for which associated evidence is sought 

try:
    api_response = api_instance.get_statement_details(statement_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatementsApi->get_statement_details: %s\n" % e)
```

    {'annotation': None,
     'evidence': [{'date': None,
                   'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000204',
                   'id': '3035598',
                   'name': 'N-methylmorphine caused increases in the release of '
                           'growth_hormone and prolactin , but serum levels of '
                           'corticosterone , luteinizing hormone and thyroid '
                           'stimulating hormone were unaffected .',
                   'uri': None}],
     'id': '37580296',
     'is_defined_by': None,
     'provided_by': None,
     'qualifiers': None}



```python

```
