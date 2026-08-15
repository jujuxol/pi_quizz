from widget_manager import WidgetManager, Widget
from param import Param


class Menu(WidgetManager):

    def __init__(self, clear_window, quit_func, start_func):
        super().__init__(clear_window, (0, 20), (0, 20), "ascii/MenuTitle.txt", None, "menu")
        self.stuck_in_widget = True

        self.widgets = {
            (2, 0): Widget(clear_window, small_pos=(29, 125), small_path="ascii/Quit.txt",  on_click_func=quit_func, name="Quit_button"),
            (1, 0): Param(clear_window),
            (0, 0): Widget(clear_window, small_pos=(29, 3), small_path="ascii/Start.txt",  on_click_func=start_func, name="start_button")
        }

    def get_param(self):
        return self.widgets[(1, 0)].get_param()