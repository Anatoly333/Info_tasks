from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
class LoginScreen(GridLayout):
    def __init__(self):
        super(LoginScreen, self).__init__()
        self.rows=5
        self.cols=2
        lbl1=Label(text="ID :",italic=True, bold=True)
        lbl2=Label(text="Password :",italic=True, bold=True)
        #txt1=TextInput(multiline=False, font_size=200)
        #txt2=TextInput(multiline=False, password=True)
        self.add_widget(lbl1)
        #self.add_widget(txt1)
        self.add_widget(lbl2)
        #self.add_widget(txt2)

class SimpleKivy(App):
    def build(self):
        return LoginScreen()

if __name__ == "__main__":
    SimpleKivy().run()