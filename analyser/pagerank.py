import numpy as np

def get_rank(cites):
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
    for i in range(15):
        p = np.dot(p,p)
    a = np.dot(a,p)

    return a
