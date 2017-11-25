import json
import search
from nltk.translate import bleu_score

'''
Install nltk through: conda install nltk
'''
filename = 'test.json'
with open(filename, encoding='utf-8') as f:
    dataset = json.load(f)
print(len(dataset))

ix = search.Load("indexdir")

resultdata = [];

for i in range(10):
    # acutal responses
    ref_lists = []
    # candidate responses
    hyps = []

    pair = dataset[i]
    post = pair[0]
    originalresponse = pair[1][0]
    response = search.SearchForTest(querypair=post, ix=ix)
    ref_lists.append([originalresponse.split()])
    hyps.append(response.split())
    score = bleu_score.corpus_bleu(ref_lists, hyps)

    resultdata.append({
        'post': post[0],
        'originalresponse': originalresponse,
        'response': response,
        'score': score,
    })

with open('resultdata.json', 'w', encoding='utf8') as outfile:
    json.dump(resultdata, outfile, ensure_ascii=False)
# print(ref_lists[0])
# print(hyps[0])
# print(score)
