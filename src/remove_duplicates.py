"""
This modules reads corpus.txt, removes duplicate news articles (having same title) and then writes the remaining
news articles to corpus2.txt.
corpus2 can be renamed to corpus if the original data set is no longer required.
"""

import json
path = '/home/rik/Heena/News2/corpus.txt'
data_dict = {}

# create a corpus dictionary

fl = open(path, 'r')
for line in fl:
    linedict = json.loads(line.rstrip())
    data_dict[linedict['title']] = linedict
fl.close()
print('done')

# write it back to another file

path2 = '/home/rik/Heena/News2/corpus2.txt'
fl = open(path2, 'w')
for val in data_dict.itervalues():
    jsondata = json.dumps(val, sort_keys=True)
    fl.write(jsondata + '\n')
print('done')