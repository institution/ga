# coding: utf-8
import sys
import pyglet
from pyglet import clock
from math import cos, sin
from numpy import pi
from pyglet.gl import *
from ga import GA

def circle(ga, r, rn):
	"""
	return -- points,lines
	"""
	assert rn >= 2
	

	e12 = ga.e1 ^ ga.e2
	R = ga.rotor(e12, (2.0 * pi) / rn)
	Rr = R.rev()

	ps = []
	ls = []
	p = ga.vector(r, 0., 0.)
	for i in range(rn):
		ps.append(p)		
		ls.append((i, (i+1) % rn))
		p = R * p * Rr
	
	return ps, ls

def cylinder(ga, r, rn, h, hn):
	assert hn >= 2
	assert ga.n >= 3
	ps0, ls0 = circle(ga, r, hn)

	pps = list(ps0)
	lls = list(ls0)
	
	h0 = -h/2.0
	
	for i in range(hn):
		ha = h0 + (float(i)/hn)*h
		ps1 = [(p + ha * ga.e3) for p in ps0]
		ls1 = [(l[0]+rn, l[1]+rn) for l in ls0]

		pps.extend(ps1)
		lls.extend(ls1)

	# connect ps0 with ps1
	ls = zip(range(rn), map(lambda n: n + rn*(hn-1), range(rn)))
	lls.extend(ls)
	return pps, lls


class Model(object):
	def __init__(self):
		self.ga = GA(3, [1.0, 1.0, 1.0])
		#self.circ = circle(self.ga, 1.5, 20, 1.0, 2)
		self.circ = circle(self.ga, 1.5, 20)

	def update(self, dt):
		R = self.ga.rotor(self.ga.e13, pi/210.0)
		R = R * 0.999
		Rr = R.rev()
		self.circ = [R*p*Rr for p in self.circ[0]], self.circ[1]
			

	def __iter__(self):
		yield self.circ



class View(object):
	def __init__(self, model, window):
		self.model, self.window = model, window

	def set_projection(self):
		glEnable(GL_BLEND)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(-2, 2, -2, 2, -2, 2)
		glMatrixMode(GL_MODELVIEW)

	def render_mv(self, mv):
		glVertex3f(mv.get(1), mv.get(2), 0.0)
	
	def render_ob(self, ps, ls):
		for k1,k2 in ls:
			self.render_mv(ps[k1])
			self.render_mv(ps[k2])
	
	def render(self, dt):
		self.window.clear()
		
		self.set_projection()
		
		glBegin(GL_LINES)
		for ob in self.model:
			self.render_ob(*ob)
		glEnd()

		self.window.flip()


def main():
	window = pyglet.window.Window(
		width=400, height=400
	)

	model = Model()
	view = View(model, window)

	clock.schedule_interval(model.update, 0.001)
	clock.schedule(view.render)

	pyglet.app.run()


if __name__ == '__main__':
	main()

