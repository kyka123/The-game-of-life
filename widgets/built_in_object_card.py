import math as math

from kivy.graphics import Rectangle, Color
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from models.built_in_object import BuiltInObject
from helpers.constants import ALIVE_CELL_COLOR, BOARD_BG_COLOR


class BuiltInObjectCard(MDBoxLayout):
    name = StringProperty('')
    prefer_rule = StringProperty('')

    def __init__(self, built_in_object: BuiltInObject, on_object_selected, **kwargs):
        super(BuiltInObjectCard, self).__init__(**kwargs)
        self.built_in_object = built_in_object
        self.name = built_in_object.name
        self.prefer_rule = f"{built_in_object.prefer_rule.left}/{built_in_object.prefer_rule.right}"
        bottom_bar_size = 100
        cell_size = min(self.width / built_in_object.width, (self.height - bottom_bar_size) / built_in_object.height)
        self.theme_bg_color = "Custom"
        self.click_handler = on_object_selected

        self.md_bg_color = BOARD_BG_COLOR

        for index_y, row in enumerate(built_in_object.object_matrix):
            for index_x, cell in enumerate(row):
                if cell:
                    with self.ids.board.canvas:
                        Color(*ALIVE_CELL_COLOR)
                        self.rect = Rectangle(pos=(index_x * cell_size, (self.height) - (index_y + 1) * cell_size),
                                              size=(cell_size, cell_size))

    def add_obj_handler(self):
        self.click_handler(self.built_in_object)

