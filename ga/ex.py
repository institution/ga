


def sortbydist(ga, fs, B, q):
	"""
	Sort polygons by distance from plane
	"""		
	ts = []
	for ps in fs:
		c = reduce(ga.add, ps, ga._0) / len(ps)
		# rejection and norm
		m = ((c^B)/B).norm_r2()   
		print m
		ts.append((m, ps))

	rs = map(lambda t: t[1],
		sorted(ts, lambda a,b: cmp(b[0], a[0]))
	)
	
	return rs


	
def rotate(ga, x, plane=None, angle=None, origin=None):
	if plane is None:
		plane = ga.e12
	if origin is None:
		origin = ga.vector()
	if angle is None:
		angle = 0.0
		
	R = ga.rotor(plane, angle)
	part = origin - R * origin * ~R
	return R * x * ~R + part

	
def pproj(ga, x, eye, B, q):
	"""
	t -- point to project
	eye -- eye position
	B -- plane
	q -- plane position
	"""
	v = eye - x
	p = x + ((B ^ (q - x)) / (B ^ v)) * v 
	return p - q


def proj(ga, x, B):
	"""
	B -- plane
	"""
	return ((x << B) << ~B)
	

