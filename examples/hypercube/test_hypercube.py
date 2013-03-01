from ga.extra import hypercube
from ga import GA


def test_hypercube():
	
	t0 = hypercube(0,0,1)
	print t0
	assert t0 == ([()], [])
	
	t1 = hypercube(1,0,1)
	print t1
	assert t1 == ([(0,),(1,)], [(0,1)])

	t2 = hypercube(2,0,1)
	print t2	
	assert t2 == ([(0,0),(1,0),(0,1),(1,1)], [(0,1),(2,3),(0,2),(1,3)])







def test_X():
	x = X(ps = [(0,0,0)])
	
	x = x.pull(e1=1).pull(e2=1)

	assert x.ps == [(0,0),(0,1),(1,0),(0,1)]

	

	
