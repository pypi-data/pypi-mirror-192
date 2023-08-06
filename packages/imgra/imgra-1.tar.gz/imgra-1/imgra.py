def grid_incidence(h, w):
	""" Build the signed incidence matrix of a WxH grid graph """
	from scipy.sparse import eye, kron, vstack
	x = eye(w-1, w, 1) - eye(w-1, w)             # path graph of length W
	y = eye(h-1, h, 1) - eye(h-1, h)             # path graph of length H
	p = kron(eye(h), x)                          # H horizontal paths
	q = kron(y, eye(w))                          # W vertical paths
	B = vstack([p, q])                           # union of all paths
	return B

version = 1

__all__ = [ "grid_incidence" ]
