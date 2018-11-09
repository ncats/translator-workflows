#!/usr/local/bin/python
#################################
__author__   = 'Nolan Nichols' ##
__created__  = '2011-05-09'    ##
__modified__ = '2011-05-11'    ##
#################################

from httplib2 import Http
from urllib import urlencode
from lxml import etree
from Bio import Entrez
from nltk.corpus import stopwords


# config for NCBO Annotator Web Service
URL = 'http://rest.bioontology.org/obs/annotator'
API_KEY = '' # api keys are available at http://bioportal.bioontology.org/
STOPWORDS = ','.join([word for word in stopwords.words('english')])

# sample annotation text from pubmed
Entrez.email = ''
handle = Entrez.efetch(db="pubmed",rettype='xml',id='20808702')
rawHTML = etree.fromstring(handle.read())
rawXML = etree.fromstring(rawHTML[1][0].text[1:-1])
ABSTRACT = rawXML.xpath('//AbstractText')[0].text

# myText = '''Melanoma is a malignant tumor of melanocytes which are found
#            predominantly in skin but also in the bowel and the eye'''

# create a POST ready Http object
# configure default parameters per user guide
# http://www.bioontology.org/wiki/index.php/Annotator_User_Guide
annotator = Http()
headers = {'Content-type': 'application/x-www-form-urlencoded'}
data = dict(apikey=API_KEY,
            longestOnly='false',
            wholeWordOnly='true',
            filterNumber='true',
            stopWords=STOPWORDS,
            withDefaultStopWords='false',
            isStopWordsCaseSensitive='false',
            minTermSize=3,
            scored='true',
            withSynonyms='true',
            ontologiesToExpand='',
            ontologiesToKeepInResult='44777', # SNOMED-CT --> 44777, RadLex  --> 45589
            isVirtualOntologyID='false',
            semanticTypes='',
            levelMax=0,
            mappingTypes=0,
            textToAnnotate=ABSTRACT, # myText
            format='xml') # parse will not work without an XML format

# parse response
def parse_annotator_response(httpResponse, annotatorXML):
    matchedConcepts = {}
    matchedContext = {}
    if httpResponse['content-type'] == 'text/xml;charset=UTF-8':
        annotatorParse = etree.fromstring(annotatorXML)
        print "Annotated text = ", annotatorParse.xpath('//textToAnnotate')[0].text
        annotatorConcepts = annotatorParse.xpath('/success/data/annotatorResultBean/annotations/annotationBean')
        for node in annotatorConcepts: # examples of using xpath to parse the xml response
            print "################################################## \n"
            print "Concept ID = ", node.xpath('./concept/id')[0].text, "\n"
            print "Concept Name = ", node.xpath('./concept/preferredName')[0].text, "\n"
            print "Concept Semantic Type = ", node.xpath('./concept/semanticTypes/semanticTypeBean/semanticType')[0].text, "\n"
            print "Concept Semantic Type Name = ", node.xpath('./concept/semanticTypes/semanticTypeBean/description')[0].text, "\n"
            print "Concept Score = ", node.xpath('./score')[0].text, "\n"
            print "#### \n"
            print "Context ID = ", node.xpath('./context/term/localConceptId')[0].text, "\n"
            print "Context Name = ", node.xpath('./context/term/name')[0].text, "\n"
            print "Context From = ", node.xpath('./context/from')[0].text, "\n"
            print "Context To = ", node.xpath('./context/to')[0].text, "\n"
            matchedConcepts[node.xpath('./concept/id')[0].text] = node.xpath('./concept/preferredName')[0].text
            matchedContext[node.xpath('./context/term/localConceptId')[0].text] = node.xpath('./context/term/name')[0].text
    else:
        print 'Please choose XML as the Format type'
    return matchedConcepts, matchedContext # returns dict of 'id:preferredName'

# send request and get response
httpResponse, xmlContent = annotator.request(URL, 'POST', headers=headers, body=urlencode(data))

# check the outcome of the response
if httpResponse.status == 200:
    print 'Call successful on ', httpResponse['date']
    concept, context = parse_annotator_response(httpResponse, xmlContent)
else:
    print 'NCBO Annotator Response Status', httpResponse.reason,' on ',httpResponse['date']



  
