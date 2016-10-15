import numpy as np

def choose_idx(n, k):
    """Basically n choose k, except yeilds each distinct choice of k elements"""
    if k == 0: yield []
    else:
        for i in range(0, n-k+1):
            to_the_right = n-i-1
            for indices in choose_idx(to_the_right, k-1):
                yield [i] + [ i+1+j for j in indices ]

def choose(l, k):
    """Iterate through all k elements of l, yeilding the k element list for each iteration"""
    a = np.array(l)
    for indices in choose_idx(len(l), k):
        yield list(a[indices])
    
def partition(l, k):
    """Iterate through all k elements of l, yeilding (choice, rest) for each iteration"""
    a = np.array(l)
    mask = np.ones(len(a), dtype=bool) # all True
    for indices in choose_idx(len(l), k):
        choice = list(a[indices])
        mask[indices] = False
        rest = list(a[mask])
        mask[indices] = True
        yield (choice, rest)
