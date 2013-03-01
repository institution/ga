# coding: utf-8
from ga import GA
from hypercube import hypercube
from math import pi, sqrt
from random import random


class Object(object):
	""" Wireframe object """
	def __init__(self, ga, points, lines):
		self.ga = ga
		self.points = [ga.vector(*p) for p in points]
		self.lines = lines
		self.rotor = ga.rotor()
		
	def rotate(self, nplane, angle):
		""" Modify object orientation """
		self.rotor = self.ga.rotor(nplane, angle) * self.rotor





def random_nplane(ga):
	""" Return pseudo-random normalized bivector in ga """
	v1 = ga.vector(*[random() for _ in range(ga.n)])
	v2 = ga.vector(*[random() for _ in range(ga.n)])
	plane = v1 ^ v2
	mag = sqrt(plane.norm_r2())
	if mag == 0.0:
		# w ktoryms wektorze wylosowalo same zera!
		raise Exception('wystapila bardzo pechowa random sequence')
	return plane / mag

	
class Model(object):
	def __init__(self, n):
		# init ga
		ga = GA(n, [1.] * n)	
		
		# prepare hypercube
		points, lines = hypercube(ga.n,-1.,1.)
		box = Object(ga, points, lines)

		# prepare rotation plane
		nplane = random_nplane(ga)
				
		self.ga = ga
		self.box = box
		self.nplane = nplane

	def update(self, dt):
		self.box.rotate(self.nplane, (2.0 * pi) / 500.0)

	def __iter__(self):
		""" Iterate over objects in the scene"""
		yield self.box
		

