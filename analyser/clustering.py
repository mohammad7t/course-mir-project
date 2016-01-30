import numpy as np
import math

from indexer.es import get_publications_freq_maps


def IJ(term):
    for x in '.0123456789*-/':
        if term.__contains__(x):
            return True;
    return False


def cummulate(dics, point):
    ans = dict()
    for tf in dics:
        for key, value in point[tf].items():
            if ans.__contains__(key):
                ans[key] += value
            else:
                ans[key] = value
    return ans


def normalized(vector):
    norm = 0
    ans = dict()
    for key, value in vector.items():
        norm += value*value
    norm = math.sqrt(norm)
    for key, value in vector.items():
        ans[key] = value/norm
    return ans


def dic_dot(v1, v2):
    ans = 0
    for key, value in v1.items():
        if v2.__contains__(key):
            ans += value*v2[key]
    return ans


def get_clustered(dtf, df, k):
    """
    :param dtf: {doc : {term : freq}}
    :param df:  {term : freq}
    :param k:   number of clusters
    :return:    {clusterId : {doc}}
    """
    stp = False
    if k > 7:
        stp = True

    point = dict()             # {doc:{dim:value}}
    for doc, termFreq in dtf.items():
        v = dict()
        for term, freq in termFreq.items():
            v[term] = (1+math.log10(freq))*(math.log10(2000 / df[term]))
        point[doc] = normalized(v)

    centers_keys = np.random.permutation(list(dtf.keys()))[0:k]
    center = dict()           # {int:{term:freq}}
    for doc in centers_keys:
        center[len(center)] = point[doc]

    for counter in range(10):

        cluster = dict()      # {int:{doc}}
        for i in range(k):
            cluster[i] = set()

        for doc, vec in point.items():
            dist = []
            for i in range(k):
                dist.append(dic_dot(vec, center[i]))
            cluster[np.argmax(dist)].add(doc)

        for i in range(k):
            center[i] = normalized(cummulate(cluster[i], point))

    label = [0 for i in range(k)]
    for i in range(k):
        score = dict()
        for term, N1_ in df.items():
            N = len(df)
            N11 = 0
            for doc in cluster[i]:
                if term in dtf[doc]:
                    N11 += 1
            N_1 = len(cluster[i])
            N01 = max(0, N_1-N11)
            N0_ = len(df)-N1_
            N10 = max(0, N1_-N11)
            N_0 = len(dtf)-len(cluster[i])
            N00 = max(0, N_0-N10)
            score[term] = 0
            if IJ(term):
                continue
            score[term] += N11/N * math.log2(1+N*N11/(N1_*N_1))
            score[term] += N01/N * math.log2(1+N*N01/(N0_*N_1))
            #score[term] += N10/N * math.log2(1+N*N10/(N1_*N_0))
            score[term] += N00/N * math.log2(1+N*N00/(N0_*N_0))

        score_list = sorted(list(score.items()), key= lambda x : (-x[1], x[0]))
        label[i] = []
        for t in score_list[:10]:
            label[i].append(t[0])

    return cluster, label, stp

if __name__ == '__main__':
    doc_tf_map, df_map = get_publications_freq_maps()

    """ for k in range(10):
        cluster, label, stp = get_clustered(doc_tf_map, df_map, k)
        if stp == True:
            break
            """
    k = 7
    cluster, label, stp = get_clustered(doc_tf_map, df_map, k)
    print(k)
    for i in range(k):
        print(len(cluster[i]))
        print(label[i])
