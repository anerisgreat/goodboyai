import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import math, sys, random

class simworld(object):
	def __init__(self):

		self.width = 600
		self.height = 600

		self.space = pymunk.Space()
		self.space.gravity = (0.0, -10.0)

	def load_world(self):
		static_body = self.space.static_body
		self.floor = pymunk.Segment(static_body, (0, 10), (self.width, 10), 0)

		self.space.add(self.floor)

		self.load_test_ball()

	def load_test_ball(self):
		mass = 1
		radius = 14
		inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
		body = pymunk.Body(mass, inertia)
		x = random.randint(120, 380)
		body.position = (x, 550)
		shape = pymunk.Circle(body, radius, (0, 0))

		self.test_body = body

		self.space.add(body, shape)


	def init_screen(self):
		pygame.init()
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.clock = pygame.time.Clock()
		self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
		self.running = True

	def run(self):
		while self.running:
			for event in pygame.event.get():
				if event.type == QUIT:
					self.running = False
				if event.type == KEYDOWN and event.key == K_ESCAPE:
					self.running = False
				if event.type == KEYDOWN and event.key == K_UP:
					self.test_body.cpv(0, -10)

			self.screen.fill(THECOLORS["white"])

			self.space.debug_draw(self.draw_options)
			dt = 1.0/60.0
			for x in range(1):
				self.space.step(dt)

			pygame.display.flip()
