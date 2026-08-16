import curses
from time import sleep
from menu import Menu
from game import Game


class Main:
    
    def __init__(self, window: curses.window):
        self.run = True
        self.too_small = False
        self.window = window

        self.Menu = Menu(window.clear, self.quit, self.start)
        self.Game = Game(window.clear, self.end)

        self.in_menu = True
        self.current_manager = self.Menu

    def quit(self):
        self.run = False

    def start(self):
        self.window.clear()
        self.current_manager = self.Game

        # load param
        self.Game.update_param(self.Menu.get_param())

        self.Game.reset()
        self.Game.cursor_pos = [0, 0]

    def end(self):
        self.window.clear()
        self.current_manager = self.Menu

    def event(self):
        try:
            key = self.window.getkey()

            # non maj number translator
            key = {"&": "1", "©": "2", "\"": "3", "\'": "4", "(": "5", "-": "6", "¨": "7", "_": "8", "§": "9", " ": "0"}.get(key, key)

            if key == "e":
                return

            self.current_manager.move(key)

            if not self.current_manager.stuck_in_widget:
                self.current_manager.stuck_in_widget = True

            #self.window.addch(10, 10, str(self.Game.Quizz.get_previus_digits(5))) # debug
            sleep(0.1)
        except:
            pass

    def update(self):
        self.current_manager.update(None)

    def draw(self):
        # check if screen is too small to prevent crash (second security cuz it's weird)
        height, width = self.window.getmaxyx()
            
        self.current_manager.draw(self.window)
        if height >= 60 and width >= 230:

            self.window.refresh()

    def loop(self):
        while self.run:
            try:
                # check if screen is too small to prevent crash
                height, width = self.window.getmaxyx()
                
                if height < 34 or width < 110:
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
                    #self.update()
                    self.draw()
            except:
                pass

def main_init(window: curses.window):
    curses.noecho()
    curses.nocbreak()
    curses.curs_set(False)
    curses.halfdelay(1)
    window.keypad(True)

    M = Main(window)
    M.loop()

if __name__ == "__main__":
    curses.wrapper(main_init)