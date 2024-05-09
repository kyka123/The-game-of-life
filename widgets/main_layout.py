import math as math

from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView

from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty

from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer, MDDialogContentContainer
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.gridlayout import MDGridLayout

from widgets.board_layout import BoardLayout
from widgets.built_in_object_card import BuiltInObjectCard
from widgets.rule_text_field import RuleTextField

from models.rule import Rule
from models.board import Board
from models.board_size import BoardSize
from models.built_in_object import BuiltInObject
from models.cell_size import CellSize

from helpers.constants import *
from helpers.load_built_in_objects import load_buit_in_objects

class MainLayout(MDRelativeLayout):
    left_rule_text_field = ObjectProperty(None)
    right_rule_text_field = ObjectProperty(None)
    select_board_size_button = ObjectProperty(None)
    speed_slider = ObjectProperty(None)
    start_stop_btn = ObjectProperty(None)

    is_playing = BooleanProperty(False)
    is_settings_open = BooleanProperty(True)
    size_name = StringProperty(DEFAULT_CELL_SIZE.name)

    rule: Rule = DEFAULT_RULE
    default_speed: float = DEFAULT_SPEED_PER_SECOND
    selected_object: BuiltInObject | None = None
    last_mouse_position_index = (-1, -1)

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.built_in_objects = load_buit_in_objects()

        self.left_rule_text_field.text = self.rule.left
        self.right_rule_text_field.text = self.rule.right

        self.dialog = MDDialog()

        self.board_layout = BoardLayout(click_handler=self.board_layout_click_handler)
        self.add_widget(self.board_layout, len(self.children))

        self.board_size = BoardSize(cell_size=DEFAULT_CELL_SIZE.size, window_size=DEFAULT_WINDOW_SIZE)
        self.board = Board(size=self.board_size)

        self.md_bg_color = BOARD_BG_COLOR

        Window.bind(size=self.on_resize)
        Window.bind(mouse_pos=self.mouse_pos)

        menu_items = [
            {
                "text": cell_size.name,
                "trailing_icon_color": "grey",
                "trailing_text_color": "grey",
                "on_release": self.on_board_size_pic(cell_size)
            } for cell_size in cell_sizes
        ]

        self.menu = MDDropdownMenu(
            md_bg_color="#bdc6b0",
            caller=self.select_board_size_button,
            items=menu_items,
        )

    def on_speed_slider_touch_down(self, *args):
        if self.is_playing:
            self.stop_game()


    def on_resize(self, obj, size):
        self.clear_canvas()
        self.board_size.resize_board(cell_size=self.board_size.cell_size, window_size=size)
        self.board.set_board_size(self.board_size)

    def on_object_selected(self, built_in_object: BuiltInObject):
        self.close_dialog()
        self.selected_object = built_in_object

    def close_dialog(self, *args):
        self.dialog.dismiss()

    def open_built_in_objects_dialog(self):
        scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height / 2), do_scroll_y=True)
        grid = MDGridLayout(cols=3, spacing="10dp", adaptive_height=True)

        for built_in_object in self.built_in_objects:
            grid.add_widget(BuiltInObjectCard(built_in_object=built_in_object, on_object_selected=self.on_object_selected))

        scroll.add_widget(grid)

        self.dialog = MDDialog(
            MDDialogHeadlineText(
                text="Wybierz wbudowane objekty (latające)",
            ),
            MDDialogContentContainer(
                scroll,
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Cofnij"),
                    style="text",
                    on_press = self.close_dialog
                ),
                spacing="8dp",
            ),
            size_hint=(None, None),
            width="850dp",
        )

        self.dialog.open()

    def add_rectange_to_layout(self, x: int, y: int, color: tuple[float] = ALIVE_CELL_COLOR, to_after: bool = False) -> Rectangle | None:
        if x > self.board_size.cols - 1 or y > self.board_size.rows - 1 or x < 0 or y < 0:
            return None
        rect = Rectangle(pos=self.board_size.cell_position_by_index_array[y][x], size=(self.board_size.cell_size, self.board_size.cell_size))
        if to_after:
            self.board_layout.canvas.after.add(Color(*color))
            self.board_layout.canvas.after.add(rect)
        else:
            self.board_layout.canvas.add(Color(*color))
            self.board_layout.canvas.add(rect)

        return rect

    def get_board_indexes_by_position(self, pos: tuple[float]) -> tuple[int]:
        index_x = int(pos[0] / self.board_size.cell_size)
        index_y = math.floor((self.height - pos[1]) / self.board_size.cell_size)
        return index_x, index_y

    def get_built_in_object_indexes_by_center_index(self, index_x:int, index_y:int, built_in_object: BuiltInObject) -> tuple[tuple[int, int]]:
        built_in_object_indexes: tuple[tuple[int, int]] = []
        for obj_index_y, row in enumerate(built_in_object.object_matrix):
            for obj_index_x, cell in enumerate(row):
                if cell:
                    built_in_object_indexes.append((index_x + obj_index_x - int(
                            self.selected_object.width / 2), index_y + obj_index_y - int(
                            self.selected_object.height / 2),))
        return built_in_object_indexes

    def mouse_pos(self, window, pos):
        if self.selected_object is None:
            return

        index_x, index_y = self.get_board_indexes_by_position(pos)

        if self.last_mouse_position_index[0] == index_x and self.last_mouse_position_index[1] == index_y:
            return
        
        self.last_mouse_position_index = (index_x, index_y)
        self.board_layout.canvas.after.clear()
        object_indexes = self.get_built_in_object_indexes_by_center_index(index_x, index_y, built_in_object=self.selected_object)

        color = (*ALIVE_CELL_COLOR, .5)

        for x, y in object_indexes:
            self.add_rectange_to_layout(x, y, color = color, to_after = True)

    def remove_rectangle_from_layout(self, x, y):
        self.board_layout.canvas.remove(self.board.of(y, x))

    def board_layout_click_handler(self, touch):
        if self.is_playing: return
        index_x, index_y = self.get_board_indexes_by_position(touch.pos)
    
        if self.selected_object != None:
            object_indexes = self.get_built_in_object_indexes_by_center_index(index_x, index_y, built_in_object=self.selected_object)

            for x, y in object_indexes:
                rect = self.add_rectange_to_layout(x, y)
                if rect != None:
                    self.board.set(y, x, rect)

            self.selected_object = None
            self.board_layout.canvas.after.clear()

            return

        if self.board.of(index_y, index_x) != False:
            self.remove_rectangle_from_layout(index_x, index_y)
            self.board.set(index_y, index_x, False)
            return
        
        rect = self.add_rectange_to_layout(index_x, index_y)
        if rect!= None:
            self.board.set(index_y, index_x, rect)

    def clear_canvas(self):
        self.board_layout.canvas.clear()

    def on_board_size_pic(self, cell_size: CellSize):
        def set_board_size():
            self.clear_canvas()
            self.board_size.resize_board(cell_size.size, window_size=(self.width, self.height))
            self.size_name = cell_size.name
            self.board.set_board_size(board_size = self.board_size)
            self.menu.dismiss()

        return set_board_size

    def start_stop_game(self):
        if self.is_playing:
            self.stop_game()
        else:
            self.start_game()

    def clear_board(self):
        self.clear_canvas()
        self.board.clear()

    def start_game(self):
        self.is_playing = True
        self.rule.update(left=self.left_rule_text_field.text, right=self.right_rule_text_field.text)
        Clock.unschedule(self.update)
        Clock.schedule_interval(self.update, 1/self.speed_slider.value)

    def stop_game(self):
        self.is_playing = False
        Clock.unschedule(self.update)

    def update(self, instance):
        self.board_layout.canvas.clear()
        self.board.refresh_board(self.rule, self.add_rectange_to_layout)