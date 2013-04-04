# coding: utf-8
"""
MV can be represented as an ordered list of baseblades indexes and coefficients (so-called packed representation). Unpacked 

MV representation
1 + 2x + 3(x^y) + 4I
packed: [(0,1), (1,2), (4,3), (7,4)] -- list of pairs (baseblade_index, coefficient)
unpacked: [1,2,0,0,3,0,0,4] -- list such as xs[baseblade_index] == coefficient 
dict: {TODO} -- similar to packed
specialized: ex. rotor, vector -- doesnot store all of the coefficients

def mv: 
	mv is multivector repr whith supports following operations:
		inz, itr, get

	 

"""
from math import factorial as _factorial



# basic operations on unpacked mv repr 

def inz(mv):
	""" Iterate over nonzero index,coeff pairs """
	for i,f in enumerate(mv):
		if f != 0.0:
			yield i,f

def itr(mv):
	""" Iterate over all coeffs """
	return iter(mv)

def get(mv, i):
	""" Get i-th coeff """
	return mv[i]
		
	
def itp(ga, mv, l, grade_slices):
	""" Iterate over l-th grade part """
	if not (0 <= l <= ga.n):
		return
	else:
		i,j = grade_slices[l]
		for k in range(i,j):
			yield get(mv, k)
		


def mv_format(ga, bst, mv):
	
	rs = []
	
	def format_elem(i, a):
		if abs(a) == 1.0:
			if i == 0:
				return ('+' if a >= 0 else '-') + '1.0'
			else:
				return ('+' if a >= 0 else '-') + bst[i]

		else:
			if i == 0:
				return '{0:+}'.format(a)
			else:
				return '{0:+}{1}'.format(a, bst[i])

	ls = [format_elem(i,a) for (i,a) in inz(mv)]
	if ls:
		return ''.join(ls).strip('+')
	else:
		return '0.0'
	

def eq(ga, mv1, mv2):
	return mv1 == mv2

def eqmf(ga, mv1, f):
	return mv1[0] == f and not any(mv1[1:])

def eqfm(ga, f, mv2):
	return f == mv2[0] and not any(mv2[1:])


def blade(ga, lvl, r):
	""" Construct blade by mul on base vectors.
	blade repr -- max-n length tuple
	blade index -- single integer <= N
	"""
	# no need - can be arhived by MV({1:1})*MV({2:1}) -> e12
	pass

def div_scalar(mv, s):
	""" Div mv by scalar 
	mv -- mv
	s -- scalar
	return -- mv
	"""
	return [f/s for f in itr(mv)]

def mv(ga, re):
	""" Construct mv by adding base blades.
	Construct packed repr from various human formats
	Can construct from:
		ordered collections
		unordered collections
	
	unpacked list repr -- [coeff0, coeff1, ..., coeffN]		
	packed dict repr -- {idx: coeff, ...}

	"""
	if isinstance(re, (list, tuple)):
		return re
	else: 
		return mv_unpack(ga, re.items())






def inverse(ga, mv):
	"""
	inv(mv) = rev(mv) / mv_inner(mv,mv)
	"""
	pass


def reverse(ga, mv):
	""" Reverse
	mv -- packed mv
	"""
	brt = ga._brt
	rv = [bf[1]*k for bf,k in zip(brt, itr(mv))]
	return rv


def _ext_to(xs, n, fill):
	return list(xs) + [fill]*(n - len(n))

def vector(ga, args):
	assert len(args) <= ga.n

	a = len(args)
	N = ga.N

	return [0.0] + list(args) + [0.0]*(N-a-1)

def MB(ga, k, fs, grade_slices):
	i,j = grade_slices[k]
	assert len(fs) == j - i
	return [0.0]*i + list(fs) + [0.0]*(N-j)


def take_grade(ga, grade_slices, mv, l):
	if not (0 <= l <= ga.n):
		return [0.0] * ga.N
	else:
		i,j = grade_slices[l]
		
		return [(f if (i<=k<j) else 0.0) for (k,f) in enumerate(itr(mv))]






def _comb(n,k):
	return _factorial(n) / (_factorial(n-k) * _factorial(k))
	
# grade_slices
def _gen_grade_slices(n):
	N = 2**n

	s = 0
	#grade_masks = [None]*(n+1)
	rs = []
	for k in range(n+1):
		d = _comb(n, k)
		rs.append((s,s+d))
		#grade_masks[k] = [0]*s + [1]*d + [0]*(N-s-d)
		s += d

	return rs
	



def mv_pack(ga, unpacked):
	""" Pack multivector
	unpacked -- repr as list, ls[baseblade_index] = scale
	return -- packed repr of mv
	"""
	assert len(unpacked) == ga.N
	return [ka for ka in enumerate(unpacked) if ka[1] != 0.0]

def mv_unpack(ga, packed):
	""" Unpack multivector
	packed -- list of pairs, [(baseblade_index, scale),...]
	return -- unpacked repr of mv
	"""
	unpacked = [0.] * ga.N
	for k,a in packed:
		assert 0 <= k < ga.N
		unpacked[k] = a
	return unpacked

def divmf(ga, mv, f):
	return [c/f for c in itr(mv)]

def mulmf(ga, mv, f):
	return [c*f for c in itr(mv)]

def mulfm(ga, f, mv):
	return [f*c for c in itr(mv)]

def mulmm(ga, mv1, mv2, bmt):
	""" Extendable multiplication

	bmt -- base multiplication table (by bb index)
	mv1,mv2 -- mvs 
	return -- product of mv1 and mv2

	let
		mv1 := ai ei
		mv2 := bj ej
	then
		mv1*mv2 := ai bj (ei*ej)
	where
		ei*ej := bmt[ei][ej]

	"""
	unpacked = [0.] * ga.N

	for k1,a1 in inz(mv1):
		for k2,a2 in inz(mv2):
			i,f = bmt[k1][k2]
			unpacked[i] += f*a1*a2

	return unpacked

def addmf(ga, mv, f, op):
	ls = list(itr(mv))
	ls[0] = op(ls[0], f)
	return ls 

def addfm(ga, f, mv, op):
	ls = list(itr(mv))
	ls[0] = op(f, ls[0])
	return ls 


def addmm(ga, mv1, mv2, op):
	""" Addition on multivectors 
	op -- 
	mv1,mv2 -- packed mvs
	return -- packed sum of mv1 and mv2

	let
		mv1 := ai ei
		mv2 := bj ej
	then
		mv1 `iop` mv2 := (ai `iop` bi) ei

	"""
	return map(op, itr(mv1), itr(mv2))


