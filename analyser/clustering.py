import numpy as np
import math


def cummulate(dics):
    ans = dict({})
    for tf in dics:
        for key, value in tf.items():
            if ans.__contains__(key):
                ans[key] += value
            else:
                ans[key] = value
    return ans

def normalized(vector):
    norm = 0
    ans = dict({})
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

def get_clustered(dtf, tf, k):
    """
    :param dtf: {doc : {term : freq}}
    :param tf:  {term : freq}
    :param k:   number of clusters
    :return:    {clusterId : {doc}}
    """

    point = map({})             #   {doc:{dim:value}}
    for doc, termFreq in dtf.items():
        v = map({})
        norm = 0
        for term, freq in termFreq.items():
            v[term] = (1+math.log10(freq))*(math.log10(2000/tf[term]))
        point[doc] = normalized(v)


    centers_keys = np.random.permutation(list(dtf.keys()))[0:k]
    center = dict({})           #   {int:{term:freq}}
    for doc in centers_keys:
        center[len(center)] = point[doc]

    cluster = dict({})
    for counter in range(10):

        cluster = dict({})      #   {int:{doc}}
        for i in range(k):
            cluster[i] = set({})

        for doc, vec in point.items():
            dist = []
            for i in range(k):
                dist.append(dic_dot(vec, center[i]))
            cluster[np.argmin(dist)].add(doc)

        for i in range(k):
            center[i] = normalized(cummulate(cluster[i]))

    return cluster