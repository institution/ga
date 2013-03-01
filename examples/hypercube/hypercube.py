# coding: utf-8

'''
def pull(x, v):
	ps + [p+v for p in ps]

	ln = len(ls)
	ls + [l+ln for l in ls]
	+ 

	
	f1,f2 zip(fs1, fs2)
	l1, l2 zip(lines(f1), lines(f2))

	p1,p2 = l1
	p4,p3 = l2
	
	fs.append((p1,p2,p3,p4))

	fs + [(f+fn) for f in fs]
'''


def upcast(ts, f):
	return [(t+(f,)) for t in ts]   # + is concat

def rupcast(f, ts):
	return [((f,)+t) for t in ts]   # + is concat

def hypercube(n,a=0.,b=1.):
	""" Describe hypercube
	n -- dimension, >= 0
	a,b -- edge start and end, hypercube(1,a,b) -> ([(a,), (b,)], [(0, 1)])
	return -- pair (points,lines)
		points -- list of n-tuples, vertices of hypercube
		lines -- list of pairs (p1_index, p2_index) descripting edges
	
	Hypercube properties:
		number_of_vertices(n) = 2**n
		number_of_edges(n) = (2**n-1)*n
	
	Examples:
	n=0: 
		points = [[]]
		lines = [[]]
	n=1: 
		points = [[0] [1]]
		lines = [[0 1]]
	n=2: 
		points = [[0,0], [1,0], [0,1] [1,1]]
		lines = [[0 1] [2 3] [0 2] [1 3]]
	"""
	assert n >= 0   

	if n == 0:   
		# czy to mialoby sens dla n < 0?
		return [()],[]

	# rekurencyjnie
	ps, ls = hypercube(n-1, a, b)
	num_p = len(ps)
	num_l = len(ls)

	# nowa lista n-wymiarowych punktow,
	# punkty wyciagniete raz do a i raz do b
	points = upcast(ps, a) + upcast(ps, b)     

	# nowa lista par indexow tworzacych krawedzie,
	# punkty wyciagniete do b maja nowa numeracje tym do a nie zmienia sie
	lines = ls + [(q+num_p, p+num_p) for (q,p) in ls]   

	# polacz punkty wyciagniete do a z odpowiadającymi wyciagnietymi do b,
	# (rozne tylko na nowej wspolrzednej)
	lines += [(i, i+num_p) for i in range(num_p)]  

	return points, lines   
		








def rotor3_to_matrix4(rotor):
	""" Convert rotor3 to glMatrix4.
	rotor -- (mv)
	"""

	# dorst chapter 7.10.4
	w = rotor.mv[0][0]
	z, x, y = rotor.mv[2]
	return [	
		1.-2.*y*y-2.*z*z, 2.*y*x+2.*w*z,    2.*z*x-2.*w*y,    0.,
		2.*x*y-2.*w*z,    1.-2.*z*z-2.*x*x, 2.*z*y+2.*w*x,    0.,
		2.*x*z+2.*w*y,    2.*y*z-2.*w*x,    1.-2.*x*x-2.*y*y, 0.,
		0.,               0.,               0.,               1.,
	]


