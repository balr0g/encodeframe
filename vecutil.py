from vec import Vec

def list2vec(L):
    """Given a list L of field elements, return a Vec with domain {0...len(L)-1}
    whose entry i is L[i]

    >>> list2vec([10, 20, 30])
    Vec({0, 1, 2},{0: 10, 1: 20, 2: 30})
    """
    return Vec(set(range(len(L))), {k:L[k] for k in range(len(L))})

def vec2list(V):
    """Given a Vector, return list containing the field elements in sorted order
    >>> vec2list(Vec({0, 1, 2},{0: 10, 1: 20, 2: 30}))
    [10, 20, 30]
    """
    return [V.f[k] for k in sorted(V.D)]
    
def zero_vec(D):
    """Returns a zero vector with the given domain
    """
    return Vec(D, {})
