import curses
from ascii_handler import *


class Widget:

    def __init__(self, clear_window, small_pos=(0, 0), big_pose=(0, 0), on_click_func=None, big_path=None, small_path=None, name=""):
        # new to test atributes
        self.small_pos = small_pos
        self.big_pos = big_pose
        self.name = name if name != "" else str(self.__class__)

        self.img_big = "BIG " + self.name if big_path == None else ascii_loader(big_path)
        self.img_small = "SMALL " + self.name if small_path == None else ascii_loader(small_path)

        self.clear_window = clear_window

        self.is_highlighted = False
        self.stuck_in_widget = False
        self.onclick = on_click_func if on_click_func != None else self.selected
    
    def highlight(self):
        self.is_highlighted = True
    
    def unhighlight(self):
        self.is_highlighted = False

    def clicked(self):
        self.onclick()

    def selected(self):
        self.stuck_in_widget = True

    def update(self, stat_manager):
        pass

    def move(self, key):
        if key == "e":
            self.stuck_in_widget = False
            self.clear_window()
            self.clear_window()
    
    def draw(self, window):
        # base img
        if self.stuck_in_widget:
            self.big_draw(window)
        else:
            if self.is_highlighted:
                self.small_draw(window, [curses.A_REVERSE])
            else:
                self.small_draw(window)

        # additional context img
        self.additional_draw(window)

    def small_draw(self, window, attributes=[]):
        ascii_drawer(window, self.small_pos, self.img_small, attributes)

    def big_draw(self, window, attributes=[]):
        ascii_drawer(window, self.big_pos, self.img_big, attributes)

    def additional_draw(self, window):
        pass
    