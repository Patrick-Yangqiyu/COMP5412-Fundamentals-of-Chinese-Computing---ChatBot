from whoosh import qparser, scoring
from whoosh.index import open_dir
from emotion.senti_python import calculate_emotion
from whoosh.qparser import QueryParser, OrGroup
import jieba

# indexdir = "indexdirtest"


def Load(indexdir):
    ix = open_dir(indexdir)
    return ix


def SearchForTest(querypair, ix):
    with ix.searcher(weighting=scoring.BM25F()) as searcher:
        query = querypair[0]
        emotion = querypair[1]
        parser = QueryParser("post", schema=ix.schema, group=OrGroup)
        seg_list = jieba.cut_for_search(query)
        querystring = " ".join(seg_list)
        print(querystring)
        query = parser.parse(querystring)
        results = searcher.search(query, limit=20)
        if len(results) == 0:
            answer = ""
        else:
            candidates = []
            for result in results:
                candidate = {'post': result['post'], 'reply': result['reply'], 'score': result.score,
                             'postemood': result['postemood']}
                print(candidate)
                candidates.append(candidate)
            print(len(candidates))
            bestresult = RankForTest(candidates, emotion)
            answer = bestresult['reply']
            print(answer)
        return answer


def Search(query, ix):
    with ix.searcher(weighting=scoring.BM25F()) as searcher:
        parser = QueryParser("post", schema=ix.schema, group=OrGroup)
        seg_list = jieba.cut_for_search(query)
        querystring = " ".join(seg_list)
        print(querystring)
        query = parser.parse(querystring)
        results = searcher.search(query, limit=20)
        if len(results) == 0:
            answer = "啊？我不太明白，换一种问法看看？"
        else:
            candidates = []
            for result in results:
                candidate = {'post': result['post'], 'reply': result['reply'].replace(" ", ""), 'score': result.score,
                             'postemood': result['postemood']}
                print(candidate)
                candidates.append(candidate)
            print(len(candidates))
            bestresult = Rank(candidates, querystring)
            answer = bestresult['reply']
            print(answer)
        return answer


def Rank(candidates, querystring):
    querymood = calculate_emotion(querystring)
    print("querymood", querymood)
    scores = []
    emotionscore = []
    for i in range(len(candidates)):
        scores.append(candidates[i]['score'])
        emotionscore.append(emotion_maching(candidates[i]['postemood'], int(querymood)))
    print(scores)
    # Nomarlize
    scoresmax = max(scores)
    scoresmin = min(scores)
    normalscores = list(map((lambda x: (x - scoresmin) / (scoresmax - scoresmin)), scores))

    finalscores = list(map(lambda x: x[0] * 0.9 + x[1] * 0.1, zip(normalscores, emotionscore)))

    print(normalscores)
    print(emotionscore)
    print(finalscores)
    bestindex = finalscores.index(max(finalscores))
    return candidates[bestindex]


def RankForTest(candidates, emotion):
    querymood = emotion
    scores = []
    emotionscore = []
    for i in range(len(candidates)):
        scores.append(candidates[i]['score'])
        emotionscore.append(emotion_maching(candidates[i]['postemood'], int(querymood)))
    print(scores)
    # Nomarlize
    scoresmax = max(scores)
    scoresmin = min(scores)
    normalscores = list(map((lambda x: (x - scoresmin) / (scoresmax - scoresmin)), scores))

    finalscores = list(map(lambda x: x[0] * 0.9 + x[1] * 0.1, zip(normalscores, emotionscore)))

    bestindex = finalscores.index(max(finalscores))
    return candidates[bestindex]


def emotion_maching(int1, int2):
    if int1 == int2:
        return 1
    if int2 in [2, 3, 4]:
        if int1 in [0, 1, 5]:
            return 0
        else:
            return 0.5
    else:
        if int1 in [0, 1, 5]:
            return 0.5
        else:
            return 0

# ix = Load(indexdir)
# Search("你是我的朋友", ix)
