from boid import *

class Flock:
	def __init__(self):
		self.__boidFlock = []

	def add_boid(self, boid):
		self.__boidFlock.append(boid)
		return self.__boidFlock

	def remove_boid(self, boid):
		self.__boidFlock.remove(boid)
		return self.__boidFlock
	
	def get_flock(self):
		return self.__boidFlock

	# adjust boid velocity so it follows the following rules:
	# 1. it steers towards the avg position of boids within its visual range
	# 2. it steers away from neighboring boids if they are at a certain distance from each other
	#	3. it matches the velocity of boids within its visual range 
	# this algorithm is naive and inefficient. will research more about optimization
	def run(self, coefficients, mode):
		flock = self.get_flock()

		for boid in flock:
			# render boid on screen
			boid.draw()

			steerToPosition = matchVelocity = steerAway = Vector(0, 0) # initial vectors
			neighborBoids = 0 # keeps track of the number of boids within 30% of visual range
			withinVRBoids = 0 # keeps track of the number of boids within visual range

			for otherBoid in flock:
				distance = boid.position.distance(otherBoid.position)
				if distance > 0:
					# if boid is within the visualRange
					if distance < boid.visualRange:
						# otherBoid is within 25% of the visualRange
						if distance < 0.25 * boid.visualRange:
							# calculate the vector pointing from the other boid to this boid's position
							diff = boid.position - otherBoid.position
							diff.normalize()
							# weight by distance
							diff /= distance 
							steerAway += diff
							neighborBoids += 1
						matchVelocity += otherBoid.velocity
						steerToPosition += otherBoid.position
						withinVRBoids += 1

			# if there are boids within the visual range
			if withinVRBoids > 0:
				steerToPosition /= withinVRBoids # average position of neighbor boids
				matchVelocity /= withinVRBoids # average velocity of neighbor boids

				# adjust to maximum speed
				steerToPosition.magnitude = boid.maxSpeed
				matchVelocity.magnitude = boid.maxSpeed

				# vector pointing to the desired one
				steerToPosition -= boid.position
				matchVelocity -= boid.velocity

				matchVelocity.limit(boid.maxForce)
				steerToPosition.limit(boid.maxForce)

			# get the average steerAway vector
			if neighborBoids > 0:
				steerAway = steerAway / neighborBoids
				if steerAway.magnitude > 0:
					steerAway.magnitude = boid.maxSpeed
					steerAway -= boid.velocity
					steerAway.limit(boid.maxForce)
			
			if len(coefficients) == 3:
				boid.add_force(steerAway * coefficients[0] + steerToPosition * coefficients[1] + matchVelocity * coefficients[2])
			else: 
				boid.add_force(steerAway * 2 + steerToPosition + matchVelocity * 2)
			boid.update()
			if mode == "wraparound": boid.wraparound()
			if mode == "bounce": boid.bounce()