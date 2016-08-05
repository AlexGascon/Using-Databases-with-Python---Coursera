class PartyAnimal:
	x = 0

	def party(self):
		self.x = self.x + 1
		print("So far", self.x)

s = PartyAnimal()
s.party()

j = PartyAnimal()
j.party
