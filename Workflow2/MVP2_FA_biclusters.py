import urllib.request
import datetime
import json
import requests
from requests.utils import quote
from collections import defaultdict

import sys
#sys.path.insert(0,'/mvp-module-library/Biclusters/bicluster_RNAseqDB_wrapper')


FA_genes_url = "https://raw.githubusercontent.com/NCATS-Tangerine/cq-notebooks/master/FA_gene_sets/FA_1_core_complex.txt"
FA_genes_all_url = "https://raw.githubusercontent.com/NCATS-Tangerine/cq-notebooks/master/FA_gene_sets/FA_4_all_genes.txt"
#https://bicluster.renci.org/apidocs
#https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_gene/43/?include_similar=false
#https://github.com/NCATS-Tangerine/cq-notebooks/tree/master/FA_gene_sets

FA_geneset = []
#for line in urllib2.urlopen(FA_genes_url):
#    FA_geneset.append(line)


#bicluster_test_1 = 'https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_gene/43/?include_similar=true'
#bicluster_response_1 = requests.get(bicluster_test_1)
#print(bicluster_response_1.text)


#print(datetime.datetime.now().time())


with urllib.request.urlopen(FA_genes_all_url) as url:
     FA_geneset.append(url.read().decode().split('\n'))

print(datetime.datetime.now().time())

print(FA_geneset[0])
print(len(FA_geneset[0]))

tissues = []
counts = dict()
multidict_tissue = defaultdict(lambda: defaultdict(set))
#tissue_to_gene_id = defaultdict()
#tissue_to_gene_label = defaultdict()
for i in range(1,len(FA_geneset[0])):
    split = FA_geneset[0][i].split('\t')
    if len(split) <= 1:
        print(split)
        continue
    curid = split[0].lower()
    curlabel = split[1].lower()

    print(curid)
    if(len(curid) > 1):
        #api_url = bicluster_RNAseqDB_wrapper.get_by_gene(curid)  #"https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_gene/"+quote(curid)+"/?include_similar=true"
        api_url = "https://bicluster.renci.org/RNAseqDB_bicluster_gene_to_tissue_gene/"+quote(curid)+"/?include_similar=true"

        print(api_url)
        responses = requests.get(api_url).json()
        #import pudb; pu.db

        for d in responses:
            key = d['col_enrich_all']
            for n in ['MONDO', 'UBERON', 'DOID', 'NCIT']:
                label = d[f'col_enrich_{n}_label']
                if label != '':
                    multidict_tissue[key]['tissue_labels'].add(label)
            for n in ['MONDO', 'UBERON', 'DOID', 'NCIT']:
                label = d[f'col_enrich_{n}']
                if label != '':
                    multidict_tissue[key]['tissue_ids'].add(label)
            multidict_tissue[key]['gene_ids'].add(curid)
            multidict_tissue[key]['gene_labels'].add(curlabel)




        #print(response)
        if(len(responses) > 1):
            for a in range(1, len(responses)):
                #import pudb; pu.db
                #col_enrich_all

                key = responses[a]['col_enrich_all']
                d = responses[0]

                if len(key) > 0:
                    if len(responses[a]['col_enrich_MONDO_label']) > 0:
                        multidict_tissue[key]['tissue_labels'].add(d['col_enrich_MONDO_label'])
                    if len(responses[a]['col_enrich_UBERON_label']) > 0:
                        multidict_tissue[key]['tissue_labels'].add(d['col_enrich_UBERON_label'])
                    if len(responses[a]['col_enrich_DOID_label']) > 0:
                        multidict_tissue[key]['tissue_labels'].add(d['col_enrich_DOID_label'])
                    if len(responses[a]['col_enrich_NCIT_label']) > 0:
                        multidict_tissue[key]['tissue_labels'].add(d['col_enrich_NCIT_label'])

                    if len(responses[a]['col_enrich_MONDO']) > 0:
                        multidict_tissue[key]['tissue_ids'].add(d['col_enrich_MONDO'])
                    if len(responses[a]['col_enrich_UBERON']) > 0:
                        multidict_tissue[key]['tissue_ids'].add(d['col_enrich_UBERON'])
                    if len(responses[a]['col_enrich_DOID']) > 0:
                        multidict_tissue[key]['tissue_ids'].add(d['col_enrich_DOID'])
                    if len(responses[a]['col_enrich_NCIT']) > 0:
                        multidict_tissue[key]['tissue_ids'].add(d['col_enrich_NCIT'])

                    multidict_tissue[key]['gene_ids'].add(curid)
                    multidict_tissue[key]['gene_labels'].add(curlabel)


            #print(response[0]['col_enrich_MONDO_label'])
            #print(response[0]['col_enrich_UBERON_label'])
            #print(response[0]['col_enrich_DOID_label'])
            #print(response[0]['col_enrich_NCIT_label'])



                #print(response.text[0])
        #for i in range(1, len(response.text)):
        #   print(response.text[i])
        #with urllib.request.urlopen(api_url) as url:
        #   data = json.loads(url.read().decode())
        #    print(data)
        #    tissues.append(data)


#print(sort(counts))
#sortcounts = sorted(counts.items(), key=lambda x: x[1])

#print(json.dumps(sortcounts, indent = 4))
#print(len(sortcounts))

for x in multidict_tissue:
    print (x, ':', multidict_tissue[x]['tissue_ids'], multidict_tissue[x]['tissue_labels'],multidict_tissue[x]['gene_ids'], multidict_tissue[x]['gene_labels'])


print("id and label order may not correspond")
#print(json.dumps(list(tissue_to_gene), indent = 4))

#for x in sortcounts:
    #print (x)
#    for y in sortcounts[x]:
#       print (y,':',sortcounts[x][y])


#for key, value in sorted(tissue_to_gene.iteritems(), key=lambda (k,v): (v,k)):
#    print "%s: %s" % (key, value)