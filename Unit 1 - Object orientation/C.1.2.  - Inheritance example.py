class Animal:
	legs = 0 
	tail = False

	def walk(self):
		print "I'm walking"

class Bird(Animal):
	wings = 2

	def walk(self):
		print "I'm walking, but I'll prefer to fly"

	def fly(self):
		print "I'm flying"