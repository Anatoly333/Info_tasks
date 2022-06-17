import copy
class Polynom():
	def __init__(self,coeficients=[]):
		self.coeficients=copy.deepcopy(coeficients)
		for i in self.coeficients:
			if self.coeficients[-1]==0:
				self.coeficients.pop(-1)

	def __repr__(self):
		return"Polynom("+str(self.coeficients)+")"