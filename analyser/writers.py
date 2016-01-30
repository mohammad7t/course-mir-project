import numpy as np

from settings import CACHE_DIR
from indexer import es

def similarity(s1, s2, mat):
    s = list(s1.union(s2))
    sim = 0.0
    for i in range(len(s)):
        for j in range(i+1,len(s)):
            sim += mat[s[i],s[j]]
    sim /= len(s)*(len(s)-1)/2
    return sim


def cluster_writers(w2d):
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
    n_merges = int(len(w2d) * 2 / 300) * 10
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
        (CACHE_DIR/'writers.progress').write_text('{} / {}'.format(counter+1, n_merges))
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

if __name__ == '__main__':
    pubs = es._get_all_publications()
    authors = {}
    for pub in pubs:
        for author in pub['authors']:
            uid = str(author['uid'])
            authors.setdefault(uid, set())
            authors[uid].add(pub['id'])
    print(cluster_writers(authors))
