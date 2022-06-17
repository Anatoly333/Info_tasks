import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
import json as js
import requests
import copy
import time
from special_functions import check_players
from special_functions import clear

pos = [0, 0, 10, 10, 100, 100, 1, 1] # x y size damage hp fire_speed player_speed bullet_charge
url = 'http://192.168.43.186:5000/'
game_id = -1
player_class = ''
player_id = -1
last_bullet = 0
host = False
connect_tr = False

def host_check(dt):
    arg = js.dumps({'act': 'get_games'})
    games = js.loads(requests.get(url, params=arg).text)

    arg = js.dumps({'act': 'get_time'})
    time = js.loads(requests.get(url, params=arg).text)

    check_players(time, games)
    clear(time, games)

    arg = js.dumps({'act': 'update_games', 'games': games})
    js.loads(requests.get(url, params=arg).text)

def connect(window):
    global player_class
    global url
    global game_id
    global player_id
    global host
    global last_bullet
    arg = js.dumps({'act': 'player_is_waiting', 'game_id': -1})
    arr = js.loads(requests.get(url, params=arg).text)
    player_id, game_id = arr[:2]
    if len(arr) > 2:
        host = True
        time.sleep(1)
        arg = js.dumps({'act': 'player_is_waiting', 'game_id': game_id, 'player_id': player_id})
        res = -1
        while res == -1:
            res = js.loads(requests.get(url, params=arg).text)
            time.sleep(1)
    if host:
        # pos[1] = window[1]
        # pos[5] *= -1
        Clock.schedule_interval(host_check, 0.1)
    Clock.schedule_interval(get_updates, 1)
    arg = js.dumps({'act': 'set_class', 'id': game_id, 'player_id': player_id, 'class': player_class})
    per_p = js.loads(requests.get(url, params=arg).text)
    pos[3] = per_p['damage']
    pos[4] = per_p['hp']
    pos[5] = per_p['fire_speed']
    pos[7] = per_p['fire_charge']
    if not host:
        pos[5] *= -1
    pos[6] = per_p['player_speed']
    h_pos = copy.copy(pos)
    h_pos[1] = h_pos[0] / 500 * h_pos[0]
    if host:
        h_pos[1] += 500
    h_pos[0] = h_pos[0] / 500.0 * h_pos[0]
    update_pos(h_pos)
    arg = js.dumps({'act': 'get_time'})
    last_bullet = js.loads(requests.get(url, params=arg).text)

def update_fire(pos, window):
    arg = js.dumps({'act': 'get_special_fires', 'id': game_id, 'player_id': player_id})
    fires = js.loads(requests.get(url, params=arg).text)
    arg = js.dumps({'act': 'get_time'})
    time = js.loads(requests.get(url, params=arg).text)
    h_pos = copy.copy(pos)
    h_pos[1] = h_pos[0] / 500 * h_pos[0]
    if host:
        h_pos[1] += 500
    h_pos[0] = h_pos[0] / 500.0 * h_pos[0]
    fires_p = {}
    fires_p['t'] = time
    fires_p['y'] = window[1] / 500.0 * h_pos[1]
    fires_p['x'] = window[0] / 500.0 * h_pos[0]
    fires_p['speed'] = pos[5]
    fires_p['damage'] = pos[3]
    fires[len([*fires.keys()])] = fires_p
    arg = js.dumps({'act': 'update_special_fires', 'id': game_id, 'player_id': player_id, 'fires': fires})
    js.loads(requests.get(url, params=arg).text)

def update_pos(new_pos):
    arg = js.dumps({'act': 'get_special_player', 'id': game_id, 'player_id': player_id})
    players = js.loads(requests.get(url, params=arg).text)
    h_pos = copy.copy(new_pos)
    h_pos[1] = h_pos[0] / 500 * h_pos[0]
    if host:
        h_pos[1] += 500
    h_pos[0] = h_pos[0] / 500.0 * h_pos[0]
    players['x'] = h_pos[0]
    players['y'] = h_pos[1]
    players['size'] = h_pos[2]
    arg = js.dumps({'act': 'update_special_player', 'id': game_id, 'player_id': player_id, 'players': players})
    js.loads(requests.get(url, params=arg).text)

def get_updates(dt):
    arg = js.dumps({'act': 'get_time'})
    time = js.loads(requests.get(url, params=arg).text)
    arg = js.dumps({'act': 'get_special_player', 'id': game_id, 'player_id': player_id})
    players = js.loads(requests.get(url, params=arg).text)
    pos[4] = players['hp']

class Touch(Widget):
    def __init__(self, **kwargs):
        super(Touch, self).__init__(**kwargs)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        with self.canvas:
            Color(205 / 255, 225 / 255, 199 / 255, mode="rgba")
            Rectangle(pos=(0, 0), size=(2000, 2000))
            global player_class
            f = open('class.txt', 'r')
            player_class = f.read()
            f.close()
            if player_class == 'sniper2':
                Color(253 / 255, 247 / 255, 73 / 255, mode="rgba")
            elif player_class == 'sniper3':
                Color(236 / 255, 126 / 255, 251 / 255, mode="rgba")
            else:
                Color(31 / 255, 153 / 255, 1, mode="rgba")
            self.rect = Rectangle(pos=(0, 0), size=(50, 50))
            self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = pos[:2]
        self.rect.size = [self.size[0] / 10, self.size[1] / 10]

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        global connect_tr
        if pos[4] > 0 and connect_tr:
            if keycode[1] == 'w':
                pos[1] += (self.size[1] / 10 + pos[6])
            elif keycode[1] == 's':
                pos[1] -= (self.size[1] / 10 + pos[6])
            elif keycode[1] == 'a':
                pos[0] -= (self.size[0] / 10 + pos[6])
            elif keycode[1] == 'd':
                pos[0] += (self.size[0] / 10 + pos[6])
            elif keycode[1] == 'spacebar':
                arg = js.dumps({'act': 'get_time'})
                time = js.loads(requests.get(url, params=arg).text)
                global last_bullet
                if time - last_bullet <= pos[7]:
                    update_fire(pos, self.size)
                    last_bullet = time

            self.rect.pos = pos[:2]
            self.rect.size = [self.size[0] / 10, self.size[1] / 10]
            update_pos(pos)
        elif not connect_tr:
            connect(self.size)
            connect_tr = True
        return True

class CanvasApp(App):
    def build(self):
        return Touch()

class ImageButton_1(ButtonBehavior, Image):
    def on_press(self):
        # print('You choose Masha')
        f = open('class.txt', 'w')
        f.write('sniper')
        f.close()

class ImageButton_2(ButtonBehavior, Image):
    def on_press(self):
        # print('You choose Vity')
        f = open('class.txt', 'w')
        f.write('sniper2')
        f.close()

class ImageButton_3(ButtonBehavior, Image):
    def on_press(self):
        # print('You choose Lesha')
        f = open('class.txt', 'w')
        f.write('sniper3')
        f.close()

class ImageButton_4(ButtonBehavior, Image):
    def on_press(self):
        # print('You choose Dimon')
        f = open('class.txt', 'w')
        f.write('sniper4')
        f.close()

Builder.load_string('''
<FirstScreen>:
    BoxLayout:
        canvas:
            Color:
                rgba:(1,1,1,1)
            Rectangle:
                pos:self.pos
                size:self.size
        orientation:'vertical'
        BoxLayout:
            size_hint:(1,0.8)
            Label:
                text:'You can choose a character'
                color:(0,0,0,1)
            Label:
                text:'Push on image. P.S. dont push on Dima'
                color:(0,0,0,1)
        #Button:
            #source:("circle.png")  
            #size_hint:(1,1)
            #on_press:root.manager.current='second'

		ImageButton_1:  
			text: 'You'
			source:'Blue_Rectange.png'  
			size_hint: (1,1)  
			on_press:root.manager.current='second'
		ImageButton_2:  
			source:'Green_Rectangle.png'  
			size_hint: (0.5,0.7)  
			on_press:root.manager.current='second'
		ImageButton_3:  
			source:'Yellow_Rectangle.png'  
			size_hint: (1.5,0.5)  
			on_press:root.manager.current='second'
		ImageButton_4:  
			source:'Perple_Rectangle.png'  
			size_hint: (0.3,0.5)  
			on_press:root.manager.current='second'
''')


class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = Touch()
        self.add_widget(self.game)

    def previous_button(self):
        self.manager.current = 'first'


class TestApp(App):
    def build(self):
        # Р вЂќР С•Р В±Р В°Р Р†Р В»РЎРЏРЎР‹ Р С”РЎР‚Р В°РЎРѓР С‘Р Р†РЎвЂ№Р в„– Р С—Р ВµРЎР‚Р ВµРЎвЂ¦Р С•Р Т‘ FadeTransition
        sm = ScreenManager(transition=FadeTransition())  # Р РЋР С•Р В·Р Т‘Р В°РЎР‹ Р СР ВµР Р…Р ВµР Т‘Р В¶Р ВµРЎР‚ РЎРЊР С”РЎР‚Р В°Р Р…Р С•Р Р† sm
        # Р С•Р В±РЎРЏР В·Р В°РЎвЂљР ВµР В»РЎРЉР Р…Р С• Р Р…РЎС“Р В¶Р Р…Р С• Р Т‘Р В°РЎвЂљРЎРЉ Р С‘Р СРЎРЏ РЎРЊР С”РЎР‚Р В°Р Р…РЎС“, Р Р†Р ВµР Т‘РЎРЉ Р С—Р С• РЎРЊРЎвЂљР С•Р СРЎС“ Р С‘Р СР ВµР Р…Р С‘ Р С‘ Р В±РЎС“Р Т‘Р ВµРЎвЂљ Р С—РЎР‚Р С•Р С‘Р В·Р Р†Р С•Р Т‘Р С‘РЎвЂљРЎРЉРЎРѓРЎРЏ Р С—Р ВµРЎР‚Р ВµР С”Р В»РЎР‹РЎвЂЎР ВµР Р…Р С‘Р Вµ
        # Р Р† kv РЎвЂћР В°Р в„–Р В»Р Вµ Р Т‘Р В»РЎРЏ Р С—РЎР‚Р ВµР С”Р В»РЎР‹РЎвЂЎР ВµР Р…Р С‘РЎРЏ Р Р…РЎС“Р В¶Р Р…Р С• Р С‘РЎРѓР С—Р С•Р В»РЎРЉР В·Р С•Р Р†Р В°РЎвЂљРЎРЉ root.manager.current, Р В° Р Р† Р С”Р С•Р Т‘Р Вµ self.manager.current
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        return sm


if __name__ == "__main__":
    TestApp().run()

#CanvasApp().run()