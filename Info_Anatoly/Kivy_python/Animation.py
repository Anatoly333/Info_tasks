'''
Widget animation
================
This example demonstrates creating and applying a multi-part animation to
a button widget. You should see a button labelled 'plop' that will move with
an animation when clicked.
'''

import kivy
kivy.require('1.0.7')

from kivy.animation import Animation
from kivy.app import App
from kivy.uix.button import Button


class TestApp(App):

	def animate_in_big(self, focus_input=True):
		self.size = self.big_size
		self.selected_size = 'big'
		if self.pos_multiplier < 1.0:
			if self.pos_multiplier:
				d = self.anim_speed * (1.0 - (self.pos_multiplier))
            else:
                d = self.anim_speed
            anim = Animation(pos_multiplier=1.0, d=d, t='out_quad')
            anim.start(self)
            self.ids.rv.scroll_to_end()
        else:
            d = 0.05
        self.ids.inputw.is_focusable = True
        if focus_input:
            Clock.schedule_once(self.focus_input, d * 3.0) 
        #return button


if __name__ == '__main__':
    TestApp().run()