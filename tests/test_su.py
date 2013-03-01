


def pproj(t, eye, B, q):
	v = eye - t
	p = t + ((B^(q-t))/(B^v)) * v
	return p

def test_pproj():
	from ga import GA
	ga = GA(3, [1., 1., 1.])
	t = ga.vector(1., 0., 0.)
	eye = ga.vector(0., 0., 1.0)
	B = ga.e1 ^ ga.e2
	q = ga.vector(0., 0., 0.5)

	x = pproj(t, eye, B, q)
	assert x == ga.vector(0.5, 0.0, 0.5), str(x)

def test_pproj():
	from random import random
	from ga import GA
	ga = GA(3, [1., 1., 1.])
	t = ga.vector(1., 0., 0.)
	eye = ga.vector(0., 0., 1.0)
	B = ga.e1 ^ ga.e2
	q = ga.vector(0., 0., 0.5)

	for _ in range(100):
		t = ga.vector(random()*100.0, random()*100.0, (random()-1.0)*100.0)
		x = pproj(t, eye, B, q)
		assert x._mv[3] - 0.5 < 0.0000000000001, (str(x), x._mv[3])

