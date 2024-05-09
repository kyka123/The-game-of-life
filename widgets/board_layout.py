from kivymd.uix.floatlayout import MDFloatLayout

from helpers.constants import  BOARD_BG_COLOR


class BoardLayout(MDFloatLayout):
    def __init__(self, click_handler, **kwargs):
        super(BoardLayout, self).__init__(**kwargs)
        self.md_bg_color = BOARD_BG_COLOR
        self.click_handler = click_handler

    def on_touch_down(self, touch):
        self.click_handler(touch)