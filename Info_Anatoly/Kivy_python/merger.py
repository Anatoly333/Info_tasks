import os 
import sys 

from random import choice 

from kivy.app import App 
from kivy.uix.screenmanager import Screen, SlideTransition, SwapTransition 
from kivy.core.window import Window 
from kivy.config import ConfigParser 
from kivy.clock import Clock 
from kivy.utils import get_hex_from_color, get_color_from_hex 
from kivy.properties import ObjectProperty, NumericProperty 

from Libs.uix.kdialog import KDialog, BDialog, Dialog 
from Libs.uix.startscreen import StartScreen 
from Libs.uix.custommenu import CustomMenuItem 
from Libs.uix.navigationmenu import NavigationMenu 

from Libs.uix.garden.navigationdrawer import NavigationDrawer 

# Классы программы. 
from Libs import programclass as prog_class 

from Libs import programdata as core 
from Libs.manifest import Manifest 

# Графика для диалоговых окон. 
Dialog.background_image_buttons = core.image_buttons 
Dialog.background_image_shadows = core.image_shadows 
Dialog.background = core.decorator 

class Program(App, prog_class.ShowPlugin, prog_class.ShowBanners, 
              prog_class.SearchShop, prog_class.ShowLicense, 
              prog_class.ShowLocations): 
    '''Функционал программы.''' 

    start_screen = ObjectProperty(None) 
    ''':attr:`start_screen` is a :class:`~Libs.uix.startscreen.StartScreen`''' 

    screen = ObjectProperty(None) 
    ''':attr:`screen` is a :class:`~Libs.uix.startscreen.StartScreen`''' 

    window_text_size = NumericProperty(15) 

    def __init__(self, **kvargs): 
        super(Program, self).__init__(**kvargs) 
        Window.bind(on_keyboard=self.events_program) 

        # Для области видимомти в programclass. 
        self.Screen = Screen 
        self.Clock = Clock 
        self.CustomMenuItem = CustomMenuItem 
        self.KDialog = KDialog 
        self.BDialog = BDialog 
        self.Manifest = Manifest 
        self.SwapTransition = SwapTransition 
        self.choice = choice 
        self.get_color_from_hex = get_color_from_hex 
        self.get_hex_from_color = get_hex_from_color 
        self.core = core 
        self.name_program = core.string_lang_title 
        self.navigation_drawer = NavigationDrawer(side_panel_width=230) 
        self.current_open_tab = core.string_lang_tabbed_menu_shops 
        self.shop = False  # выбранный магазин 
        self.open_dialog = False  # открыто диалоговое окно 

        self.effects_transition = (SlideTransition, SwapTransition) 
        # Список магазинов. 
        self.shops = core.dict_shops.keys() 
        # Список локаций. 
        self.locations = [ 
            location.split('.')[0].lower() for location in os.listdir( 
                '{}/Data/Images/locations'.format(core.prog_path))] 

    def build_config(self, config): 
        config.adddefaultsection('General') 
        config.setdefault('General', 'language', 'Русский') 
        config.setdefault('General', 'theme', 'default') 

    def build(self): 
        self.title = self.name_program  # заголовок окна программы 
        self.icon = 'Data/Images/logo.png'  # иконка окна программы 
        self.use_kivy_settings = False 

        self.config = ConfigParser() 
        self.config.read('{}/program.ini'.format(core.prog_path)) 
        self.set_var_from_file_settings() 

        # Главный экран программы. 
        self.start_screen = StartScreen( 
            color_action_bar=core.color_action_bar, 
            color_body_program=core.color_body_program, 
            color_tabbed_panel=core.color_tabbed_panel, 
            tabbed_text=core.string_lang_tabbed_menu.format( 
                TEXT_SHOPS=core.string_lang_tabbed_menu_shops, 
                TEXT_LOCATIONS=core.string_lang_tabbed_menu_locations, 
                COLOR_TEXT_SHOPS=get_hex_from_color(core.color_action_bar), 
                COLOR_TEXT_LOCATIONS=core.theme_text_color), 
            title_previous=self.name_program[1:], 
            events_callback=self.events_program, core=core 
        ) 

        self.screen = self.start_screen 
        navigation_panel = NavigationMenu( 
            events_callback=self.events_program, 
            items=core.dict_navigation_items 
        ) 

        Clock.schedule_interval(self.show_banners, 4) 

        self.navigation_drawer.add_widget(navigation_panel) 
        self.navigation_drawer.anim_type = 'slide_above_anim' 
        self.navigation_drawer.add_widget(self.start_screen) 

        return self.navigation_drawer 

    def set_var_from_file_settings(self): 
        '''Установка значений переменных из файла настроек program.ini.''' 

        self.language = core.select_locale[ 
            self.config.get('General', 'language') 
        ] 

    def set_current_item_tabbed_panel(self, color_current_tab, color_tab): 
        self.screen.ids.custom_tabbed.text = 
            core.string_lang_tabbed_menu.format( 
                TEXT_SHOPS=core.string_lang_tabbed_menu_shops, 
                TEXT_LOCATIONS=core.string_lang_tabbed_menu_locations, 
                COLOR_TEXT_SHOPS=color_tab, 
                COLOR_TEXT_LOCATIONS=color_current_tab 
            ) 

    def events_program(self, *args): 
        '''Обработка событий программы.''' 

        if self.navigation_drawer.state == 'open': 
            self.navigation_drawer.anim_to_state('closed') 

        if len(args) == 2:  # нажата ссылка 
            event = args[1] 
        else:  # нажата кнопка программы 
            try: 
                _args = args[0] 
                event = _args if isinstance(_args, str) else _args.id 
            except AttributeError:  # нажата кнопка девайса 
                event = args[1] 

        if core.PY2: 
            if isinstance(event, unicode): 
                event = event.encode('utf-8') 

        if event == core.string_lang_settings: 
            pass 
        elif event == core.string_lang_exit_key: 
            self.exit_program() 
        elif event == core.string_lang_license: 
            self.show_license() 
        elif event == core.string_lang_plugin: 
            self.show_plugins() 
        elif event in self.locations: 
            print(event) 
        elif event == 'search_shop': 
            self.search_shop() 
        elif event == 'navigation_drawer': 
            self.navigation_drawer.toggle_state() 
        elif event == core.string_lang_tabbed_menu_locations: 
            self.show_locations() 
        elif event == core.string_lang_tabbed_menu_shops: 
            self.back_screen(event) 
        elif event == 'obi_banner': 
            self.press_banner(event) 
        elif event in (1001, 27): 
            self.back_screen(event) 
        elif event in self.shops: 
            print(event) 
        return True 

    def back_screen(self, event): 
        '''Менеджер экранов.''' 

        # Нажата BackKey на главном экране. 
        if self.screen.ids.screen_manager.current == '': 
            if event in (1001, 27): 
                self.exit_program() 
            return 
        if len(self.screen.ids.screen_manager.screens) != 1: 
            self.screen.ids.screen_manager.screens.pop() 
        self.screen.ids.screen_manager.current = \ 
            self.screen.ids.screen_manager.screen_names[-1] 
        # Устанавливаем имя предыдущего экрана. 
        #self.screen.ids.action_previous.title =  self.screen.ids.screen_manager.current 
        # Устанавливаем активный пункт в item_tabbed_panel. 
        self.set_current_item_tabbed_panel( 
                core.theme_text_color, get_hex_from_color(core.color_action_bar) 
        ) 

    def exit_program(self, *args): 
        def dismiss(*args): 
            self.open_dialog = False 

        def answer_callback(answer): 
            if answer == core.string_lang_yes: 
                sys.exit(0) 
            dismiss() 

        if not self.open_dialog: 
            KDialog(answer_callback=answer_callback, on_dismiss=dismiss, 
                    separator_color=core.separator_color, 
                    title_color=get_color_from_hex(core.theme_text_black_color), 
                    title=self.name_program).show( 
                text=core.string_lang_exit.format(core.theme_text_black_color), 
                text_button_ok=core.string_lang_yes, 
                text_button_no=core.string_lang_no, param='query', 
                auto_dismiss=True 
            ) 
            self.open_dialog = True 

    def on_pause(self): 
        '''Ставит приложение на 'паузу' при выхоже из него. 
        В противном случае запускает программу заново''' 

        return True 

    def on_resume(self): 
        print('on_resume') 

    def on_stop(self): 
        print('on_stop')