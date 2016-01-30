import numpy as np


def similarity(s1, s2, mat):
    s = list(s1.union(s2))
    sim = 0.0
    for i in range(len(s)):
        for j in range(i+1,len(s)):
            sim += mat[s[i],s[j]]
    sim /= len(s)*(len(s)-1)/2
    return sim


def cluster_writers(w2d, n_merges):
    ind2id = []
    id2ind = dict()
    for key in w2d.keys():
        id2ind[key] = len(ind2id)
        ind2id.append(key)

    d2w = dict()
    for writer, docs in w2d.items():
        for doc in list(docs):
            if not d2w.__contains__(doc):
                d2w[doc] = set()
            d2w[doc].add(id2ind[writer])

    n = len(ind2id)
    adj = np.zeros((n, n), dtype=np.float64)
    for doc, writers in d2w.items():
        w = list(writers)
        for i in range(len(w)):
            for j in range(i+1,len(w)):
                adj[w[i]][w[j]] += 1
                adj[w[j]][w[i]] += 1

    # to strengthen the weights
    for i in range(n):
        for j in range(n):
            adj[i][i] *= adj[i][j]

    clusters = []
    for i in range(n):
        clusters.append(set({i}))

    for counter in range(n_merges):
        m = n-counter
        best_i = set()
        best_j = set()
        best_sim = -1

        for i in range(m):
            for j in range(i+1,m):
                sim = similarity(clusters[i], clusters[j], adj)
                if sim > best_sim:
                    best_sim = sim
                    best_i = i
                    best_j = j

        cluster = clusters[best_i].union(clusters[best_j])
        del clusters[best_j]
        del clusters[best_i]

        clusters.append(cluster)
    ans = []
    for item in clusters:
        s = set()
        for ind in item:
            s.add(ind2id[ind])
        ans.append(s)
    return ans

# To test:
print(cluster_writers({'a':{1,2,3}, 'b':{2,3}, 'c':{4,5}, 'd':{5,6}}, 2))