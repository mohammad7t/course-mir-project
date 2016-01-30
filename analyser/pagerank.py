import numpy as np
from indexer import es

def get_rank(publications):
    n = len(publications)
    cites = np.zeros((n,n))
    ind2id = []
    id2ind = dict()
    for pub in publications:
        id2ind[pub['id']] = len(ind2id)
        ind2id.append(pub['id'])

    for pub in publications:
        for ref_id in pub['reference_ids']:
            if ref_id in id2ind:
                cites[id2ind[pub['id']], id2ind[ref_id]] = 1

    return _get_rank(cites).tolist()[0]


def _get_rank(cites):
    """
    :param cites: np.array presenting citation of i -> j
    :return: array of page ranks
    indices are assumed 0..N
    """
    n = cites.shape[0]
    p = np.array(cites, dtype=np.float64)
    alpha = 0.1

    for i in range(n):
        p[i,:] = p[i,:]*(1-alpha) + np.ones((1,n))*alpha
        p[i,:] /= np.sum(p[i,:])

    a = np.ones((n,n))
    for i in range(50):
        p = np.dot(p,p)
    a = np.dot(a,p)

    return a

if __name__ == '__main__':
    pubs = es._get_all_publications()
    ranks = get_rank(pubs)
    es.update_ranks(pubs, ranks)
    es.refresh()

print(es._get_all_publications()[20]['rank'])