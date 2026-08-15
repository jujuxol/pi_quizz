import curses
from time import sleep
from ascii_handler import *
from widget import Widget


class WidgetManager(Widget):

    def __init__(self, clear_window, small_pos=(0, 0), big_pos=(0, 0), big_path=None, small_path=None, name = "", perma_bg = False):
        name = str(self) if name == "" else name
        super().__init__(clear_window, small_pos, big_pos, big_path=big_path, small_path=small_path, name=name)

        self.perma_bg = perma_bg
        self.stuck_in_widget = False
        self.cursor_pos = [0, 0]

        self.widgets = { # exemple
            (0, 0): Widget(clear_window, (25, 50), (0, 0), lambda: self.widgets.pop((1, 1))),
            (1, 0): Widget(clear_window, (25, 75), (0, 0)),
            (1, 1): Widget(clear_window, (30, 75), (0, 0)),
            (-1, -1): Widget(clear_window, (20, 25), (0, 0), lambda: self.move("e"))
        }

    def update(self, stat_manager):
        # widget update
        for widget in self.widgets.values():
            widget.update(stat_manager)

    def movement(self, move):
        if move in "zs":
            # deplacement
            self.cursor_pos[1] -= 1 * {"z": 1,"s": -1}[move]
            if tuple(self.cursor_pos) not in self.widgets.keys(): # regarde si un widget est sur cette pos
                og_x = self.cursor_pos[0] # stoque x original avant de boucler sur les x a coté
                for i in range(2, 6):
                    if (og_x + (-1)*(i%2)*(i//2) + ((i+1)%2)*(i//2), self.cursor_pos[1]) in self.widgets.keys(): # boucle sur les x de -2 a +2
                        self.cursor_pos[0] = og_x + (-1)*(i%2)*(i//2) + ((i+1)%2)*(i//2)
                        break # casse la boucle si on a trouver un widget, (considérer comme le plus proche)

                if self.cursor_pos[0] == og_x: # revient a la position initiale si aucun widget est in range
                    self.cursor_pos[1] += 1 * {"z": 1,"s": -1}[move]

        if move in "qd":
            # deplacement
            self.cursor_pos[0] -= 1 * {"q": 1,"d": -1}[move]
            if tuple(self.cursor_pos) not in self.widgets.keys(): # regarde si un widget est sur cette pos
                og_y = self.cursor_pos[1] # stoque y original avant de boucler sur les y a coté
                for i in range(2, 6):
                    if (self.cursor_pos[0], og_y + (-1)*(i%2)*(i//2) + ((i+1)%2)*(i//2)) in self.widgets.keys(): # boucle sur les y de -2 a +2
                        self.cursor_pos[1] = og_y + (-1)*(i%2)*(i//2) + ((i+1)%2)*(i//2)
                        break # casse la boucle si on a trouver un widget, (considérer comme le plus proche)

                if self.cursor_pos[1] == og_y: # revient a la position initiale si aucun widget est in range
                    self.cursor_pos[0] += 1 * {"q": 1,"d": -1}[move]

    def selected(self):
        self.stuck_in_widget = True
        self.cursor_pos = [0, 0]

    def move(self, key):
        if self.widgets[tuple(self.cursor_pos)].stuck_in_widget:
            self.widgets[tuple(self.cursor_pos)].move(key)

        else:
            if key in "zqsd":
                self.movement(key)
            elif key == "e":
                self.stuck_in_widget = False
                self.clear_window()
            elif key == " ":
                self.clear_window()
                self.widgets[tuple(self.cursor_pos)].clicked()
    
    def draw(self, window):
        if (not self.stuck_in_widget or (self.stuck_in_widget and not self.widgets[tuple(self.cursor_pos)].stuck_in_widget)) or self.perma_bg:
            super().draw(window) # draw BG

        if self.stuck_in_widget: # selected
            # only draw interior of selected module
            if self.widgets[tuple(self.cursor_pos)].stuck_in_widget:
                #window.clear()
                self.widgets[tuple(self.cursor_pos)].draw(window)
            
            # draw all modules
            else:
                on_top = list(self.widgets.values())[-1] # mettre par dessus les autre le selectionner
                for pos, widget in self.widgets.items():
                    if pos == tuple(self.cursor_pos):
                        widget.highlight()
                    else:
                        widget.unhighlight()
                    
                    if widget.stuck_in_widget:
                        on_top = widget
                    else:
                        widget.draw(window)
                on_top.draw(window)


class Main:
    
    def __init__(self, window: curses.window):
        self.run = True
        self.too_small = False
        self.window = window

        self.W = WidgetManager(window.clear, name="Test")

    def event(self):
        try:
            key = self.window.getkey()
            
            if key == "Q":
                self.run = False
            else:
                self.W.move(key)

            sleep(0.1)
        except:
            pass

    def update(self):
        self.W.update(None)

    def draw(self):
        # check if screen is too small to prevent crash (second security cuz it's weird)
        height, width = self.window.getmaxyx()
            
        self.W.draw(self.window)
        if height >= 60 and width >= 230:

            self.window.refresh()

    def loop(self):
        while self.run:
            # check if screen is too small to prevent crash
            height, width = self.window.getmaxyx()
            
            if height < 30 or width < 100:
                if not self.too_small:
                    self.too_small = True
                    self.window.clear()
                self.window.addstr(0, 0, "Screen to small, dezoom the terminal")
                self.window.refresh()
            else:
                if self.too_small:
                    self.too_small = False
                    self.window.clear()
                self.event()
                self.update()
                self.draw()

def a(window: curses.window):
    curses.noecho()
    curses.nocbreak()
    curses.curs_set(False)
    curses.halfdelay(1)
    window.keypad(True)

    M = Main(window)
    M.loop()

if __name__ == "__main__":
    curses.wrapper(a)
