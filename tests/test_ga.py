from ga import GA

def doctest(x, e):
	assert str(x) == e, repr(str(x))

def test_format():
	ga = GA(3)
	
	doctest(
		ga.MV([0., -0.,0.,-0., 0.,-0.,0., -0.]),
		'0.0'	
	)
	doctest(
		ga.MV([1., -1.,1.,-1., 1.,-1.,1., -1.]),
		'1.0-e1+e2-e3+e12-e13+e23-I',
	)
	doctest(
		ga.MV([2., -2.,2.,-2., 2.,-2.,2., -2.]),
		'2.0-2.0e1+2.0e2-2.0e3+2.0e12-2.0e13+2.0e23-2.0I'
	)
	

def test_has_symbols():
	ga = GA(2)
	assert hasattr(ga, '_0')
	assert hasattr(ga, '_1')
	assert hasattr(ga, 'e1')
	assert hasattr(ga, 'e2')
	assert hasattr(ga, 'e12')
	assert hasattr(ga, 'I')

def test_metric():
	ga = GA(1, [-1.0])
	assert ga.e1 * ga.e1 == -1.0


def test_zero_dimensions():
	ga = GA(0)
	assert ga.N == 1

def test_symbol_values():
	ga = GA(2, [1.,1.])	
	assert ga._0 == ga.MV([0.0, 0.0, 0.0, 0.0])
	assert ga._1 == ga.MV([1.0, 0.0, 0.0, 0.0])
	assert ga.e1 == ga.MV([0.0, 1.0, 0.0, 0.0])
	assert ga.e2 == ga.MV([0.0, 0.0, 1.0, 0.0])
	assert ga.I == ga.MV([0.0, 0.0, 0.0, 1.0])
	assert ga.e12 == ga.MV([0.0, 0.0, 0.0, 1.0])
	
def test_zero():
	ga = GA(0)
	assert ga.zero() == ga.MV([0.0])
	
def test_one():
	ga = GA(0)
	assert ga.one() == ga.MV([1.0])


def test_bb_mul():
	ga = GA(3)
	
	doctest(ga.e1 * ga.e2, 'e12')
	doctest(ga.e1 * ga.e2 * ga.e3, 'I')
	doctest(ga.e2 * ga.e1, '-e12')
	doctest(2.0  * ga.e1, '2.0e1')
	doctest(ga.e12 * 2.0, '2.0e12')
	


def test_bb_div():
	ga = GA(3)
	# regress
	mI = -1.0 * ga.I
	doctest(mI/mI, '1.0')
	

def test_bb_add():
	ga = GA(3)
	
	doctest(ga._1 + ga.e1 + ga.e2, '1.0+e1+e2')
	doctest(ga.e1 + ga.e12, 'e1+e12')

	doctest(2.0 + ga.I, '2.0+I')
	doctest(ga.I + 2.0, '2.0+I')


def test_sub():
	ga = GA(3)
	
	# regression e1-e2
	doctest(ga.e1-ga.e2, 'e1-e2')

def test_neg():
	ga = GA(3)
	
	doctest(-ga.e1, '-e1')
	
	

def test_rev():
	ga = GA(3)

	doctest(ga._1.rev(), '1.0')
	doctest(ga.e1.rev(), 'e1')	

	doctest(ga.e12.rev(), '-e12')
	doctest(ga.e12.rev().rev(), 'e12')
	doctest(ga.I.rev(), '-I')
	doctest(ga.I.rev().rev(), 'I')

def test_revop():
	ga = GA(3)
	doctest(~ga.e12, '-e12')

def test_eq_float():
	ga = GA(1)
	assert ga._1 == 1.0
	assert 1.0 == ga._1
	assert not (ga._1 + ga.e1 == 1.0)
	assert not (1.0 == ga._1 + ga.e1)

def test_eq():
	ga = GA(2)

	assert ga._1 == ga._1
	assert ga.e1 == ga.e1
	assert ga.I == ga.I

	assert not(ga.e2 == ga.e1)
	assert not(ga.e1 == ga.e2)




def test_bb_outer():
	ga = GA(3)
	
	# antisymmetry on bb
	doctest(ga.e1 ^ ga.e2, 'e12')
	doctest(ga.e2 ^ ga.e1, '-e12')

	# neutral element
	doctest(ga._1 ^ ga._1, '1.0')
	doctest(ga._1 ^ ga.e12, 'e12')
	doctest(ga.e12 ^ ga._1, 'e12')

	# bb^bb -> 0
	doctest(ga.e1 ^ ga.e1, '0.0')
	doctest(ga.e12 ^ ga.e12, '0.0')
	doctest(ga.I ^ ga.I, '0.0')

	doctest(ga.e12 ^ ga.e23, '0.0')
	doctest(ga.I ^ ga.e1, '0.0')
	doctest(ga.e12 ^ ga.I, '0.0')



def test_inner():
	ga = GA(3)

	doctest(ga._1 | ga._1, '1.0')
	doctest(ga._1 | ga._1, '1.0')

	doctest(ga.e1 | ga.e1, '1.0')
	doctest(ga.e1 | ga.e2, '0.0')
	doctest(ga.e1 | ga.e12, 'e2')
	doctest(ga.e12 | ga.e1, '-e2')

	doctest(ga.e12 | ga.e12, '-1.0')
	doctest(ga.I | ga.I, '-1.0')
	

def test_inv():
	ga = GA(3)

	doctest(ga._1.inv(), '1.0')
	doctest(ga.e1.inv(), 'e1')
	doctest(ga.e12.inv(), '-e12')   # rev(e12) / (e12|e12) == -e12 / -1
	doctest(ga.I.inv(), '-I') 





def test_left():
	ga = GA(3)

	doctest(ga.e2 << ga.e12, '-e1')
	doctest(ga.e3 << ga.e12, '0.0')
	doctest(ga.e12 << ga.e1, '0.0')
	doctest(ga._1 << ga.e1, 'e1')
	doctest(ga.e1 << ga._1, '0.0')
	#doctest(2.0 << ga.e1, '2.0e1')
	#doctest(ga.e1 << 2.0, '0.0')



def test_norm_r2():
	ga = GA(3)

	doctest(ga.e1.norm_r2(), '1.0')
	doctest((2.0 * ga.e1).norm_r2(), '4.0')
	doctest((ga.e12 * 2.0).norm_r2(), '4.0')


def test_rotor():
	ga = GA(3)

	doctest(ga.rotor(), '1.0')
	doctest(ga.rotor(ga.e1^ga.e2, 0.0), '1.0')
	#doctest(ga.rotor(ga.e1^ga.e2, 3.14/4.0), '1.0')


def test_part():
	ga = GA(3)

	x = ga.MV([1., 2.,3.,4., 5.,6.,7., 8.])

	doctest(x.part(-1), '0.0')
	doctest(x.part(0), '1.0')
	doctest(x.part(1), '2.0e1+3.0e2+4.0e3')
	doctest(x.part(2), '5.0e12+6.0e13+7.0e23')
	doctest(x.part(3), '8.0I')
	doctest(x.part(4), '0.0')

	





