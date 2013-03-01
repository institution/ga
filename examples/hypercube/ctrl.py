# coding: utf-8
import sys
import pyglet
from pyglet import clock
from model import Model
from view import View
from math import cos, sin
from numpy import pi
from model import Model
from pyglet.gl import *
import sys

n = int(sys.argv[1])

model = Model(n = n)

window = pyglet.window.Window(
	width=400, height=400
)

view = View(model, window)

def update(dt):
	model.update(dt)

clock.schedule_interval(update, 0.001)

def render(dt):
	view.render(dt)

clock.schedule(render)

pyglet.app.run()


