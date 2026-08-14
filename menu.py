from widget_manager import WidgetManager, Widget


class Menu(WidgetManager):

    def __init__(self, clear_window, quit_func, start_func):
        super().__init__(clear_window, (0, 20), (0, 20), "ascii/MenuTitle.txt", None, "menu")

        self.widgets = {
            (1, 0): Widget(clear_window, small_pos=(29, 125), small_path="ascii/Quit.txt",  on_click_func=quit_func, name="Quit_button"),
            (0, 0): Widget(clear_window, small_pos=(29, 3), small_path="ascii/Start.txt",  on_click_func=start_func, name="start_button")
        }