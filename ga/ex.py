


def sortbydist(ga, B, q):
	"""
	Sort polygons by distance from plane
	"""		
	def sortbydist_(fs):
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

	return sortbydist_

	
def rotation(ga, plane, angle, origin):
	R = ga.rotor(plane, angle)
	part = origin - R * origin * ~R
	
	def rotation_(x):
		return R * p * ~R + part

	return rotation_
	
def perspective(ga, eye, B, q):
	"""
	t -- point to project
	eye -- eye position
	B -- plane
	q -- plane position
	"""
	
	def perspective_(t):
		v = eye - t
		p = t + ((B ^ (q - t)) / (B ^ v)) * v 
		return p - q

	return perspective_
	 

def projection(ga, B):
	"""
	B -- plane
	"""
	def projection_(x):
		return ((x << B) << ~B)
	return projection_
	

def rejection(x, B):
	pass

