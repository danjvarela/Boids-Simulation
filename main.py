from flock import *

flock = None

def setup():
	size(640, 364)
	global flock
	flock = Flock()
	for i in range(15):
		randx = randrange(int(width / 3), int(2 * width / 3))
		randy = randrange(int(width / 3), int(2 * width / 3))
		randPosition = Vector(randx, randy) # random position at the middle of the screen
		boid = Boid(randPosition)
		# the follosing boid properties can be changed according to preference
		# boid.size = 4
		# boid.maxSpeed = 8
		# boid.maxForce = 0.1
		# boid.visualRange = 50
		flock.add_boid(Boid(randPosition))	

def draw():
	background(40, 44, 52)
	global flock
	# change the coefficients according to preference
	# coefficients = (separation, cohesion, alignment)
	# mode = "wraparound" or "bounce"
	flock.run(coefficients = (1, 2, 2), mode = "bounce")

# click on screen to add a boid
def mouse_pressed():
	global flock
	boid = Boid(Vector(mouse_x, mouse_y))
	flock.add_boid(boid)


if __name__ == "__main__":
	builtins.title = "Boids Simulation"
	run(frame_rate=120)