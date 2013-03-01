

def rotor3_to_matrix4(rotor):
	""" Convert rotor3 to glMatrix4.
	rotor -- multivector
	return -- opengl (loadable to matrix) list
	"""

	# dorst chapter 7.10.4
	w = rotor[0]
	z, x, y = rotor[1,2,3]
	return [	
		1.-2.*y*y-2.*z*z, 2.*y*x+2.*w*z,    2.*z*x-2.*w*y,    0.,
		2.*x*y-2.*w*z,    1.-2.*z*z-2.*x*x, 2.*z*y+2.*w*x,    0.,
		2.*x*z+2.*w*y,    2.*y*z-2.*w*x,    1.-2.*x*x-2.*y*y, 0.,
		0.,               0.,               0.,               1.,
	]

