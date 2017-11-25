import json
import os.path
from whoosh import fields
from whoosh import index
from whoosh.fields import *

filename = 'train.json'
with open(filename, encoding='utf-8') as f:
    dataset = json.load(f)

schema = fields.Schema(post=TEXT(stored=True, analyzer=analysis.SimpleAnalyzer()), postemood=NUMERIC(stored=True),
                       reply=TEXT(stored=True), replymood=NUMERIC(stored=True))

if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
exists = index.exists_in("indexdir")
ix = index.create_in("indexdir", schema)

datasetlen = len(dataset)
for i in range(int(datasetlen / 1000) + 1):
    writer = ix.writer()
    start = i * 1000
    end = (i * 1000 + 999) if datasetlen > (i * 1000 + 999) else datasetlen
    for pair in dataset[start:end]:
        post = pair[0][0]
        postemood = pair[0][1]
        reply = pair[1][0]
        replymood = pair[1][1]
        print(start,end)
        i = i + 1
        writer.add_document(post=post, postemood=postemood, reply=reply, replymood=replymood)
    writer.commit()

print('index complete')
