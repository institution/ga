# coding: utf-8
"""
ga.mv
ga.blade<N>
ga.rotor
ga.plane
ga.vector

ga.inner  |
ga.outer  ^
ga.mul    *
ga.div    /
ga.add    +
ga.sub    -
ga.left   <<
ga.right  >>
ga.gr
ga.inv
ga.rev     
ga.grinv   
ga.exp
ga.mag2

ga.mirror
ga.rotate
ga.project

"""


import bb
import mv
import operator
from math import sin, cos

epsilon = 0.00000001

class GA(object):
	def __init__(self, n, metric=None):
		# n >= 0
		self.n = n   

		self.metric = [None]+metric if metric is not None else [None]+[1.0]*n

		self.N = 2**n
	
		self._grade_slices = mv._gen_grade_slices(n)
	
		self._init_bmts()
		
		self.MV = self._construct_MV()

		self.e = [None] * self.N
		for i, sym in self._bst.items():
			if sym[0].isdigit():
				sym = '_'+sym

			ei = self.MV({i: 1.})
			self.e[i] = ei

			self.__setattr__(sym, ei)
		
		Isym = 'e' + ''.join(map(str, range(1, n+1)))
		self.__setattr__(Isym, self.I)
		self.__setattr__('_0', self.zero())
			

	def _construct_MV(self):
		ga = self
		class MV(object):
			""" Wrapper over other representation
			"""
			def __init__(self, r):
				self._mv = mv.mv(ga, r)
			
			def get(self, i):
				return self._mv[i]

			def __iter__(self):
				return iter(self._mv)

			def __str__(self):
				return mv.mv_format(ga, ga._bst, self._mv)	


			def __mul__(self, other):
				if isinstance(other, float):
					return MV(mv.mulmf(ga, self._mv, other))
				else: 
					return MV(mv.mulmm(ga, self._mv, other._mv, ga._bmt_geo))

			def __rmul__(self, other):
				assert isinstance(other, float)
				return MV(mv.mulfm(ga, other, self._mv))

			def __lshift__(self, other):
				return MV(mv.mulmm(ga, self._mv, other._mv, ga._bmt_left))

			
			def __add__(self, other):
				if isinstance(other, float):					
					return MV(mv.addmf(ga, self._mv, other, operator.iadd))
				else: 
					return MV(mv.addmm(ga, self._mv, other._mv, operator.iadd))

			def __radd__(self, other):
				assert isinstance(other, float)
				return MV(mv.addfm(ga, other, self._mv, operator.iadd))

			
			def __sub__(self, other):
				if isinstance(other, float):					
					return MV(mv.addmf(ga, self._mv, other, operator.isub))
				else: 
					return MV(mv.addmm(ga, self._mv, other._mv, operator.isub))

			def __rsub__(self, other):
				assert isinstance(other, float)
				return MV(mv.addfm(ga, other, self._mv, operator.isub))
			

			def __div__(self, other):
				if isinstance(other, (float, int)):
					return MV(mv.divmf(ga, self._mv, other))
				else: 
					return MV(mv.mulmm(ga, self._mv, other.inv()._mv, ga._bmt_geo))

				

			def __or__(self, other):
				return MV(mv.mulmm(ga, self._mv, other._mv, ga._bmt_inn))

			def __xor__(self, other):
				return MV(mv.mulmm(ga, self._mv, other._mv, ga._bmt_out))

			def __eq__(self, other):
				if isinstance(other, float):
					return mv.eqmf(ga, self._mv, other)
				return mv.eq(ga, self._mv, other._mv)

			def __req__(self, other):
				assert isinstance(other, float)
				return mv.eqfm(ga, other, self._mv)
				
			def rev(self):
				""" Reverse
				"""
				return MV(mv.reverse(ga, self._mv))

			def __invert__(self):
				""" Reverse
				"""
				return MV(mv.reverse(ga, self._mv))
			
			def __neg__(self):
				return -1.0 * self		

			def __pos__(self):
				return self

			def norm_r2(self):
				return float(self * ~self)

			def __float__(self):
				assert all((f <= epsilon) for f in self._mv[1:])
				return self.get(0)

			def inv(self):
				""" Inverse
				inv(mv) = rev(mv) / mul(mv,mv.rev())
				"""
				X = self
				f = float(X * X.rev())
				return MV(mv.div_scalar(X.rev(), f))

			def part(self, l):
				return MV(mv.take_grade(ga, ga._grade_slices, self._mv, l))

		return MV



	def zero(self):
		return self.MV([0.0]*self.N)

	def one(self):
		return self.MV([1.0] + [0.0]*(self.N-1))

	def add(self, x, y):
		return x + y

	def sub(self, x, y):
		return x - y

	def mul(self, x, y):
		return x * y

	def div(self, x, y):
		return x / y

	def inner(self, x, y):
		return x | y

	def outer(self, x, y):
		return x ^ y

	def left(self, x, y):
		return x << y

	def right(self, x, y):
		return x >> y

	def rev(self, x):
		return ~x

	def neg(self, x):
		return -x

	def pos(self, x):
		return x

	def inv(self, x):
		return x.inv()

	def eq(self, x, y):
		return x == y

	def part(ga, x, l):
		return x.part(l)


	def _init_bmts(self):
		""" Calculate bst and bmt-s
		"""
		n = self.n	
		m = self.metric

		# construct baseblades repr and mapping to indexes
		index_by_repr, repr_by_index = bb.construct_base(n)
		
		# base symbol table
		bst = bb.construct_bst(n, repr_by_index)
		
		# multiplications on bb reprs
		def b_geo(r1,r2): 
			return bb.b_mul(m, r1, r2)

		def b_out(r1,r2):
			r3,f3 = bb.b_mul(m, r1, r2)
			r5,f5 = bb.b_part(r3, bb.b_gr(r1)+bb.b_gr(r2))
			return r5, f5*f3
	
		def b_inn(r1,r2):
			r3,f3 = bb.b_mul(m, r1, r2)
			r5,f5 = bb.b_part(r3, abs(bb.b_gr(r1)-bb.b_gr(r2)))
			return r5, f3*f5

		def b_left(r1,r2):
			r3,f3 = bb.b_mul(m, r1, r2)
			r5,f5 = bb.b_part(r3, bb.b_gr(r2)-bb.b_gr(r1))
			return r5, f3*f5
		
		# fill bmt-s
		bmt_geo = bb.construct_bmt(index_by_repr, repr_by_index, b_geo)
		bmt_out = bb.construct_bmt(index_by_repr, repr_by_index, b_out)
		bmt_inn = bb.construct_bmt(index_by_repr, repr_by_index, b_inn)
		bmt_left = bb.construct_bmt(index_by_repr, repr_by_index, b_left)
		
		brt = bb.construct_brt(repr_by_index)

		self._brt = brt
		self._bst = bst
		self._bmt_geo = bmt_geo
		self._bmt_out = bmt_out
		self._bmt_inn = bmt_inn
		self._bmt_left = bmt_left
		


	
	#def blade(self, k, *xs):
	#	return mv.blade(self, k, *xs)

	def rotor(self, nplane=None, angle=0.0):
		""" Construct rotor """
		assert self.n >= 2
		if angle == 0.0:
			return self._1  # neutral rotor

		assert nplane.norm_r2() - 1.0 <= 0.0000001
		return cos(angle/2.0) - nplane * sin(angle/2.0)


	def vector(self, *args):
		return self.MV(mv.vector(self, args))

	def vec(self, *args):
		return self.vector(*args)




 
#ga.grinv   
#ga.exp







