
#Project: CS 330 Program Assignment 1
#Program: Dynamic Movement
#Purpose: Intialize dynamic movement algorithms
#Author: Kalyn Stricklin :p
#Email: kms0081@uah.edu
#Created: 2023-09-19
#Modified: 2023-09-05




#define moving dynamic steering behaviors

import math
import numpy as np

#VECTOR MATH!!!!
#calculate the length of two 2D vectors
def vectorLength(vector):
	length = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
	return length

#normalize a 2D vector
def normalize(vector):
	length = vectorLength(vector)
	if length ==0:
		return vector
	result = np.array([vector[0]/length, vector[1]/length])
	return result

#calculate a vector product of two 2D vectors
def multiply(vector, scalar):
	multVec= np.array([vector[0]* scalar, vector[1]* scalar])
	return multVec

#calculate a vector difference of two 2D vectors
def subtract(vector1, vector2):
	sub= np.array([vector1[0]+ (- vector2[0]), vector1[1] + (- vector2[1])])
	return sub

#calculate a scalar dot product of two 2D vectors
def dot(A,B):
	sum = ([A[0]*B[0] + A[1]*B[1]])
	return sum


#Geometry Functions
#calculate the distance between two points in 2D
def distancePointPoint(x,z):
	distance = math.sqrt((z[1]-x[1])**2 + (z[2]-x[2])**2)
	return distance

#calculate the distance from a point to a line in 2D
def distancePointLine(x,z,line):
	pass

#calculate point on line closest to query point in 2D
#q = query point, x and z are distinct poiints on a line as vectors
def closestPointLine(x,z,q):
	point = dot((q - x),(z - x))
	point /= dot((z - x), (z - x))
	point = (x + (point * (z - x)))
	return point

#calculate point on segment closest to query point in 2D
#q = query , x and z are segement endpoints as vectors
def closestPointSegment(x,z,q):
	point = dot((q - x), (z - x))
	point /= dot((z - x), (z - x))
	if (point <= 0):
		return x
	elif (point >= 1):
		return z
	else:
		point = (x + (point * (z - x)))
		return point


#PATH functions
#def pathAssemble(path.id, path.x, path.y):
	
#calculates position on path given path param
def getPosition(param):
		pass

#calculates path parameter given position on or off path
def getParam(path, position):
	pass

#assign the programming assignment 
ASSIGNMENT = 1;

if (ASSIGNMENT == 1):
	simTime = 50 #simulation time

elif (ASSIGNMENT == 2):
	simTime = 125 #simulation time
	
#simulated timesteps for program output
time = 0
deltaTime = 0.5  #duration of time step
numTimeSteps = int(simTime / deltaTime)


#steering behaviors
CONTINUE = 1 
FLEE = 7
SEEK = 6
ARRIVE = 8
FOLLOWPATH = 11


class SteeringOutput:
	def __init__ (self):
		self.linear = np.array ([0.0, 0.0])
		self.angular = 0.0

class Path:
	def __init__(self):
		self.path= 1
		self.pathOffSet = 0.0
		self.segments = 0.0
		self.x = 0.0
		self.z = 0.0



#CLASS DEFINITION
class Character():
	def __init__ (self):
		self.ID = 0
		self.position = np.array([0.0, 0.0])
		self.velocity = np.array([0, 0])
		self.orientation = 0.0
		self.maxVelocity = 0.0
		self.maxAcceleration = 0.0
		self.target = None
		self.targetRadius = 0.0
		self.slowingRadius = 0.0
		self.timeToTarget = 0.0
		self.steering = CONTINUE
		self.collisionStatus = False
		self.linearX = 0.0
		self.linearZ = 0.0
		self.angular = 0.0
		self.maxSpeed = 0.0
		self.pathToFollow = 1
		self.pathOffSet = 0.0

	#CONTINUE: does not move
	def getSteeringContinue(self):
		pass
   
	#FLEE: moves away from target
	def getSteeringFlee(self):
		result ={'linear': np.array([0.0, 0.0]), 'angular': 0.0}
		
		# Set direction to target
		direction = subtract(self.position, self.target.position)
		
		#normalize the direction
		normDirection = normalize(direction)

		# Move along normalized direction to target using max acceleration
		result['linear'] = multiply(normDirection, self.maxAcceleration)

		
		# Output steering
		result['angular'] = 0.0
		return result

		
	#SEEK: moves directly towards target as fast as possible
	def getSteeringSeek(self):
		
		result ={'linear': np.array([0.0, 0.0]), 'angular': 0.0}
	   
		# Set direction to target
		direction = subtract(self.target.position, self.position)
		normDirection =  normalize(direction)
		
		# Move along direction to target using max acceleration
		result['linear'] = multiply(normDirection, self.maxAcceleration)
  
		# Output steering
		result['angular'] = 0.0
		return result

	
		
	#ARRIVE: moves directly towards a target, slowing down when near
	def getSteeringArrive(self):
		result ={'linear': np.array([0.0, 0.0]), 'angular': 0.0}

		#get direction and distance to target
		direction = subtract(self.target.position, self.position)
		distance = vectorLength(direction)

		#set the time to reach target, slow radius, and target radius
		self.timeToTarget = 0.1
	
		self.targetRadius = character.targetRadius
		self.slowingRadius = character.slowingRadius

		#test for arrival, return nothing
		if (distance < self.targetRadius):
			return None

		#outside slowing down radius , move at max speed
		if (distance > self.slowingRadius):
			targetSpeed = self.maxVelocity
		#otherwise calculate at a scaled speed
		else:
			targetSpeed  = self.maxVelocity * distance / self.slowingRadius
	   
		
		#target velocity combines with speed and direction
		targetVelocity =  direction
		targetVelocity = normalize(targetVelocity)

		targetVelocity = multiply(targetVelocity, targetSpeed) 
		
		#accelerate to target velocity
		result['linear'] = subtract(targetVelocity, self.velocity)
		result['linear']  = result['linear'] / self.timeToTarget


		#test for too fast acceleration
		if (vectorLength(result['linear']) > self.maxAcceleration):
			result['linear']=  normalize(result['linear'])
			result['linear'] = multiply(result['linear'], self.maxAcceleration)

		
		#output steering
		result['angular'] = 0.0
		return result

 
	def updatePosOri(self,result):
		if result is not None:
		# Update the position and orientation
			self.position[0] += self.velocity[0] * deltaTime
			self.position[1] += self.velocity[1] * deltaTime
			self.orientation += result['angular'] * deltaTime

			# Update the velocity
			self.velocity[0] += result['linear'][0] * deltaTime
			self.velocity[1] += result['linear'][1] * deltaTime
	   
	   
			# Check for speeding and clip
			currentSpeed = vectorLength(self.velocity)
			if currentSpeed > self.maxVelocity:
				normVel =  normalize(self.velocity)
				self.velocity = multiply(normVel, self.maxVelocity)

			self.linearX = result['linear'][0]
			self.linearZ = result['linear'][1]
		

	def getSteeringFollowPath(self):

		#variable to hold the path to follow
		self.path

		#holds the distance along the path to generate the target (can be negative if char moves in reverse direction)
		self.pathOffSet

		#calculate the target to delegate to face
		currentParam = path.getParam(self.position, currentPos)

		#offset it
		targetParam = currentParam + self.pathOffSet

		#get the target position
		self.target.position = path.getPosition(targetParam)

		#2 delegate to seek
		return self.getSteeringSeek()




#initalize all characters for assignment 1 
char1 = Character()
char1.ID = 2601
char1.steering = CONTINUE
char1.position = np.array([0.0,0.0])
char1.velocity = np.array([0.0,0.0])
char1.orientation = 0.0
char1.maxVelocity = 0.0
char1.maxAcceleration = 0.0
char1.target = None
char1.targetRadius = 0.0
char1.slowingRadius = 0.0
char1.timeToTarget = 0.0

char2 = Character()
char2.ID = 2602
char2.steering = FLEE
char2.position = np.array([-30.0, -50.0])
char2.velocity = np.array([2.0, 7.0])
char2.orientation = math.pi/4
char2.maxVelocity = 8.0
char2.maxAcceleration = 1.5
char2.target = char1
char2.targetRadius = 0.0
char2.slowingRadius = 0.0
char2.timeToTarget = 0.0

char3 = Character()
char3.ID = 2603
char3.steering = SEEK
char3.position = np.array([-50.0, 40.0])
char3.velocity = np.array([0.0, 8.0])
char3.orientation = 3*math.pi/2
char3.maxVelocity = 8.0
char3.maxAcceleration = 2.0
char3.target = char1
char3.targetRadius = 0.0
char3.slowingRadius = 0.0
char3.timeToTarget = 0.0

char4 = Character()
char4.ID = 2604
char4.steering = ARRIVE
char4.position = np.array([50.0, 75.0])
char4.velocity = np.array([-9.0, 4.0])
char4.orientation = math.pi 
char4.maxVelocity = 10.0
char4.maxAcceleration = 2.0
char4.target = char1
char4.targetRadius = 4.0
char4.slowingRadius = 32.0
char4.timeToTarget = 1.0


char5 = Character()
char5.ID = 2701
char5.steering = FOLLOWPATH
char5.position = np.array([20.0, 95.0])
char5.velocity = np.array([0.0, 0.0])
char5.orientation = 0.0
char5.maxVelocity = 4.0
char5.maxAcceleration= 2.0
char5.pathToFollow = 1
char5.pathOffSet = 0.04


#put characters into a list
characters = [char1, char2, char3, char4]
#characters = [char1, char2, char3, char4, char5]


#Write conditions of characters to trajectory file
f = open("trajectory.txt", 'w')
for character in characters:
	print (
			time, 
			character.ID, 
			character.position[0], 
			character.position[1], 
			character.velocity[0], 
			character.velocity[1], 
			character.linearX, 
			character.linearZ, 
			character.orientation, 
			character.steering,
			character.collisionStatus, 
			sep = ",",
			end = "\n",
			file = f
			)

while (time <= simTime):
	time = time + deltaTime
	for character in characters:
		if character.steering == CONTINUE:
			result = character.getSteeringContinue()
		elif character.steering == FLEE:
			result = character.getSteeringFlee()
		elif character.steering == SEEK:
			result = character.getSteeringSeek()
		elif character.steering == ARRIVE:
			result = character.getSteeringArrive()


		character = character.updatePosOri(result)

	with open("trajectory.txt", 'a') as f:
		for character in characters:
	   
			print (time, 
			character.ID, 
			character.position[0], 
			character.position[1], 
			character.velocity[0], 
			character.velocity[1], 
			character.linearX, 
			character.linearZ, 
			character.orientation, 
			character.steering,
			character.collisionStatus, 
			sep = ",",
			end = "\n",
			file = f
			)
		



