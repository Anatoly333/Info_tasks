class Man(object):
  def __init__(self, surname):
    self.surename = surname
  def name(self):
    print('My name is man')
  def shadow(self):
    print('I am shadow?')

class BatMan(Man):
  def name(self):
    print('My name is BatMan')
  def shadow(self):
     super().shadow()
     print('Oh,my shadow')