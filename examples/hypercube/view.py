# coding: utf-8
from pyglet.gl import *
import ctypes
from PIL import Image

def pproj(t, eye, B, q):
	v = eye - t
	p = t + ((B^(q-t))/(B^v)) * v
	return p - q

class View(object):
	def __init__(self, model, window):
		super(View, self).__init__()
		
		self.window = window
		self.model = model
		self.i = 1   # frame number
				

	def set_projection(self):
		#glDisable(GL_TEXTURE_2D)
		#glShadeModel(GL_SMOOTH)
		#glEnable(GL_LINE_SMOOTH)
		#glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
		#glHint(GL_LINE_SMOOTH_HINT,GL_NICEST)

		glEnable(GL_BLEND)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(-2, 2, -2, 2, -2, 2)
		glMatrixMode(GL_MODELVIEW)

	def render_obj(self, obj):
		""" Render (points,lines) type object 
		obj -- obj with attrs: points, lines, rotor
		"""		
		ga = self.model.ga

		# prepare plane x^y 
		B = ga.e1 ^ ga.e2
		
		# eye and B plane position 		
		eye = ga.vector(0.0, 0.0, 10.0)
		q = ga.vector(0.0, 0.0, 2.0)
		
		# prepare rotor
		R = obj.rotor
		
		# first half in red, second in blue
		half_index = len(obj.points)/2.

		# rotate and project points, save to temporary
		temp_ps = [None] * len(obj.points)
		for i,p in enumerate(obj.points):
			rp = R * p * ~R
			
			tp = pproj(rp, eye, ga.e12, q)
			#tp = (rp << B) << ~B
			temp_ps[i] = tp

		
		# render lines using remembered points
		for k1,k2 in obj.lines:
			mv1 = temp_ps[k1]
			mv2 = temp_ps[k2]
			
			self.set_color(half_index, k1)
			glVertex3f(mv1.get(1), mv1.get(2), 0.0)

			self.set_color(half_index, k2)
			glVertex3f(mv2.get(1), mv2.get(2), 0.0)

	def set_color(self, half_index, i):
		if i < half_index:
			glColor3f(1,0,0)
		else:
			glColor3f(0,0,1)
	
	def render(self, dt):
		""" Render model """
		
		self.window.clear()
		self.set_projection()
		
		glBegin(GL_LINES)
		for obj in self.model:
			self.render_obj(obj)
		glEnd()

		if False:
			# http://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
			# save to png
			mem = ctypes.create_string_buffer(400*400*4)
		
			glReadPixels(GLint(0), GLint(0), 
				GLsizei(400), GLsizei(400), 
				GL_RGBA, GL_UNSIGNED_BYTE, 
				mem);

			img = Image.fromstring("RGBA", (400,400), mem)
			img.save('vid/foo-{0:05d}.png'.format(self.i))

		self.i += 1
		self.window.flip()


