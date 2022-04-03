from p5 import *
from random import *

class Boid:
	global width, height
	def __init__(self, position):
		self.position = position
		angle = random() * 2 * PI
		self.velocity = Vector(cos(angle), sin(angle))
		self.acceleration = Vector(0, 0)
		self.size = 4
		self.maxSpeed = 8
		self.maxForce = 0.1
		self.visualRange = 50

	# renders boid on screen
	def draw(self):
		with push_matrix():
			no_stroke()
			fill(152, 195, 121)
			translate(self.position.x, self.position.y)
			rotate(self.velocity.angle)
			begin_shape()
			vertex(self.size * 3, 0)
			vertex(0, self.size)
			vertex(0, -self.size)
			end_shape()

	# adds acceleration
	def add_force(self, force):
		self.acceleration += force
	
	# update the boid variables
	def update(self):
		self.velocity += self.acceleration
		self.velocity.limit(self.maxSpeed)
		self.position += self.velocity
		# reset acceleration
		self.acceleration *= 0

	# boid bounces when it encounters a wall
	def bounce(self):
		if self.position.x < -self.size: self.velocity.x *= -1
		if self.position.y < -self.size: self.velocity.y *= -1
		if self.position.x > width + self.size: self.velocity.x *= -1
		if self.position.y > height + self.size: self.velocity.y *= -1

	# boid appears on other side of the screen
	def wraparound(self):
		if self.position.x < -self.size: self.position.x = width + self.size
		if self.position.y < -self.size: self.position.y = height + self.size
		if self.position.x > width + self.size: self.position.x = -self.size
		if self.position.y > height + self.size: self.position.y = -self.size