"""
a sample api request is as following
https://api.oadoi.org/10.1038/nature12373?email=b.ranjbarsahraei@tudelft.nl


the input to this code is a dois.txt file that contains one doi per line.

IMPORTANT: don't forget to add your email below.
"""

import urllib
import json

FOLDER = ""

your_email = ""

thread_number = 0
batch_size = 100000  
# please note that the batch_size limit can be increased if you have more than 100,000 dois in your file, 
# or alternatively you can run the file in multiple iterations by increasing the thread_number.

f = "dois.txt"
print f
file = FOLDER + f
f_output = open(FOLDER + f.replace('.txt',str(thread_number)) + "_enriched.txt", "w")
with open(file, "r") as f:

    # making the header
    doi = "10.1038/nature12373"
    requestURL = "http://api.oadoi.org/%s?%s" % (doi, your_email)
    response = urllib.urlopen(requestURL).read()
    results = json.loads((response))["results"][0]
    header = results.keys()
    f_output.write('\t'.join(header) + '\n')
    counter = 0
    all_lines = f.readlines()[thread_number*batch_size: (thread_number+1)*batch_size]
    for i, l in enumerate(all_lines):
        print i + (thread_number*batch_size) , 'out of ', (thread_number+1)*batch_size
        doi = l.replace('\n','')
        if doi:
            row = '%s\t' % doi
            requestURL = "http://api.oadoi.org/%s?%s" % (doi, your_email)
            try:
                response = json.loads((urllib.urlopen(requestURL).read()))
                if "results" in response.keys():
                    results = response["results"][0]
                    for j, h in enumerate(header):
                        content = ''
                        if isinstance(results[h], list):
                            for r in results[h]:
                                content += r.encode('utf-8') + ';'
                        if isinstance(results[h], int):
                            content = str(results[h])
                        if isinstance(results[h], basestring):
                                content = results[h].encode('utf-8')
                        row += content
                        if j == len(header) - 1:
                            row +=  '\n'
                        else:
                            row += '\t'
                    f_output.write(row)
                else:
                    f_output.write(doi + '\n')
            except:
                f_output.write(doi + '\n')
                print 'error with doi' + doi
                print requestURL

                        
        else:
            f_output.write('\n')
