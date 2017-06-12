"""
a sample api request is as following
https://api.oadoi.org/10.1038/nature12373?email=b.ranjbarsahraei@tudelft.nl

"""

import urllib

import json

import simplejson as simplejson


FOLDER = "DOIs/"

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(FOLDER) if isfile(join(FOLDER, f)) and ".txt" in f]
onlyfiles = [onlyfiles[12]]
for f in onlyfiles:
    print f
    file = FOLDER + f
    f_output = open(FOLDER + f + "_enriched.txt", "w")
    with open(file, "r") as f:

        # making the header
        doi = "10.1038/nature12373"
        requestURL = "http://api.oadoi.org/%s?email=b.ranjbarsahraei@tudelft.nl" % doi
        response = urllib.urlopen(requestURL).read()
        results = simplejson.loads((response))["results"][0]
        header = results.keys()
        f_output.write('\t'.join(header) + '\n')
        counter = 0
        all_lines = f.readlines()
        for i, l in enumerate(all_lines):
            print i , 'out of ', len(all_lines)
            doi = l
            if doi:
                row = ''
                requestURL = "http://api.oadoi.org/%s?email=b.ranjbarsahraei@tudelft.nl" % doi
                response = simplejson.loads((urllib.urlopen(requestURL).read()))
                if "results" in response.keys():
                    results = response["results"][0]
                    for j, h in enumerate(header):
                        content = ''
                        if isinstance(results[h], list):
                            for r in results[h]:
                                content += r.encode('utf-8') + ';'
                        if isinstance(results[h], int):
                            content = str(results[h])
                        if isinstance(results[h], str):
                                content = results[h].encode('utf-8')

                        row += content
                        if j == len(header) - 1:
                            row +=  '\n'
                        else:
                            row += '\t'
                    f_output.write(row)
                else:
                    f_output.write('\n')
            else:
                f_output.write('\n')

