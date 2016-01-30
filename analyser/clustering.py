import numpy as np
import math

from indexer.es import get_publications_freq_maps


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

    return cluster

doc_tf_map, df_map = get_publications_freq_maps()
print(get_clustered(doc_tf_map, df_map, 5))