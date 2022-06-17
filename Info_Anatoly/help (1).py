import copy
class Polynom():
	def __init__(self,coefficients=[]):
		self.coefficients=copy.deepcopy(coefficients)
		for i in range(len(self.coefficients)):
			if self.coefficients[-1]==0:
				self.coefficients.pop(-1)

	def __repr__(self):
		return"Polynom("+str((self.coefficients))+")"