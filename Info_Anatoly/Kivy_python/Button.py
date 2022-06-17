import kivy 
kivy.require("1.9.1") 
from kivy.app import App 
from kivy.uix.button import Button 

class ButtonApp(App): 
	
	def build(self): 
		# use a (r, g, b, a) tuple 
		btn = Button(text ="Characters !", 
			font_size ="20sp", 
			background_color =(1, 1, 1, 1), 
			color =(1, 1, 1, 1), 
			size =(32, 32), 
			size_hint =(.2, .2), 
			pos =(300, 250))
		btn.bind(on_press = self.callback) 
		return btn

	def callback(self, event): 
		print("button pressed") 
		print('Yoooo !!!!!!!!!!!') 	
		
root = ButtonApp() 
root.run()
