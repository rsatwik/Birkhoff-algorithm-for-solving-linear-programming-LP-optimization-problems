# Python code used for Birkhoff decomposition
import numpy as np
import itertools
from networkx import from_numpy_matrix
from networkx.algorithms.bipartite.matching import maximum_matching
if __name__=='__main__':
    D = np.matrix([[0.1,0.2,0.7],[0.3,0.4,0.3],[0.6,0.4,0]])
    print(D)
    print()
    D = D.astype('float')
    birk_coeff = []
    birk_permutations = []
    m, n = D.shape
    if m != n:
        raise ValueError('given matrix is not a square matrix'.format(m, n))
    indices = list(itertools.product(range(m), range(n)))
    while not np.all(D == 0):
        replica = np.zeros_like(D)
        replica[D.nonzero()] = 1
        bipartite = np.vstack((np.hstack((np.zeros((m, m)), replica)),
        np.hstack((replica.T, np.zeros((n, n))))))
        bipartite_graph = from_numpy_matrix(bipartite)
        left_nodes = range(n)
        perfect_matching_graph = maximum_matching(bipartite_graph, left_nodes)
        perfect_matching_nodes = {u: v % n for u, v in
        perfect_matching_graph.items() if u < n}
        num = len(perfect_matching_nodes)
        P = np.zeros((num, num))
        P[list(zip(*(perfect_matching_nodes.items())))] = 1
        c = min(D[i, j] for (i, j) in indices if P[i, j] == 1)
        birk_coeff.append(c)
        birk_permutations.append(P)
        D -= c * P
        D[np.abs(D) < np.finfo(np.float).eps * 10.] = 0.0
answer = list(zip(birk_coeff, birk_permutations))
for i in answer:
    print('coeff:',np.around(i[0],2))
    print(i[1])