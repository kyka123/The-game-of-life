from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

from widgets.main_layout import MainLayout
from helpers.constants import *

class TheGameOfLifeApp(MDApp):
    title = APP_TITLE

    def build(self):
        self.theme_cls.theme_style = THEME_STYLE
        self.theme_cls.primary_palette = PRIMARY_PALETTE

        Window.size = DEFAULT_WINDOW_SIZE
        
        return MainLayout()
        

if __name__ == '__main__':
    Builder.load_file('style.kv')
    TheGameOfLifeApp().run()
