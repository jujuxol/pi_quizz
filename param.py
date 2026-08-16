from widget_manager import Widget, WidgetManager, ascii_drawer, ascii_loader, curses
from input_widget import InpputWidget


class Param(WidgetManager):

    def __init__(self, clear_window):
        super().__init__(clear_window, (29, 60), (0, 0), None, "ascii/Param.txt", "param")
        self.img_big = ""

        self.limit_lives = (1, 3)

        self.param = {
            "mode": "classic",
            "limit": None,
            "start": 0,
            "jump": 1,
            "live": 3
        }

        self.scroll = -10
        self.scroll_limit = (1, 3)
        self.space_between_param = 10
        self.og_offset = 0

        self.jump_img = ascii_loader("ascii/Jump.txt")
        self.limit_img = ascii_loader("ascii/Limit.txt")
        self.lives_img = ascii_loader("ascii/Lives.txt")
        self.mode_img = ascii_loader("ascii/Mode.txt")
        self.start_img = ascii_loader("ascii/Start.txt")
        self.digit_img = [ascii_loader(f"ascii/digit/{i}.txt") for i in range(10)]
        self.game_modes_img = {"classic": ascii_loader("ascii/Classic.txt"), "training": ascii_loader("ascii/Training.txt"), "geo": ascii_loader("ascii/Geoguesser.txt")}

        digit_len = {"0": 12, "1": 6, "2": 11, "3": 11, "4": 13, "5": 11, "6": 11, "7": 11, "8": 11, "9": 11}
         
        self.widgets = {
            (0, -5): Widget(clear_window, (0, 50), small_path="ascii/Left.txt", name="left gamemode select", on_click_func=lambda: self.change_mode(-1)),
            (1, -5): Widget(clear_window, (0, 125), small_path="ascii/Right.txt", name="right gamemode select", on_click_func=lambda: self.change_mode(1)),
            (0, -4): InpputWidget(clear_window, "ascii/digit", digit_len, "²", "p", lambda x, y: x in "0123456789" and len(y) < 5, (0, 55), "ascii/Underscore.txt", "input limit"),
            (0, -3): InpputWidget(clear_window, "ascii/digit", digit_len, "²", "p", lambda x, y: x in "0123456789" and len(y) < 5, (0, 65), "ascii/Underscore.txt", "input start"),
            (0, -2): InpputWidget(clear_window, "ascii/digit", digit_len, "²", "p", lambda x, y: x in "0123456789" and len(y) < 3, (0, 60), "ascii/Underscore.txt", "input jump"),
            (0, -1): Widget(clear_window,(0, 50), small_path="ascii/Left.txt", name="left live select", on_click_func=lambda: self.change_live(-1)),
            (1, -1): Widget(clear_window, (0, 80), small_path="ascii/Right.txt", name="right live select", on_click_func=lambda: self.change_live(1)),
            (0, 0): Widget(clear_window, (29, 60), on_click_func=lambda: self.move("e"), small_path="ascii/Return.txt", name="return")
        }

        self.widgets[(0, -3)].text = "0"
        self.widgets[(0, -2)].text = "1"

        self.move("P")

    def get_param(self):
        self.param["limit"] = self.widgets[(0, -4)].text
        self.param["limit"] = None if self.param["limit"] == "" else int(self.param["limit"])
        self.param["start"] = int(self.widgets[(0, -3)].text)
        self.param["jump"] = int(self.widgets[(0, -2)].text)

        return self.param

    def change_mode(self, offset):
        self.param["mode"] = ["classic", "training", "geo"][(["classic", "training", "geo"].index(self.param["mode"]) + offset)%3]

        if self.param["mode"] == "classic":
            self.widgets[(1, -5)].small_pos = (self.widgets[(1, -5)].small_pos[0], 125)

        elif self.param["mode"] == "training":
            self.widgets[(1, -5)].small_pos = (self.widgets[(1, -5)].small_pos[0], 140)

        elif self.param["mode"] == "geo":
            self.widgets[(1, -5)].small_pos = (self.widgets[(1, -5)].small_pos[0], 158)

    def change_live(self, offset):
        self.param["live"] = min(self.limit_lives[1], max(self.limit_lives[0], self.param["live"] + offset))

    def move(self, key):
        super().move(key)

        if self.widgets[(0, -3)].text == "" and not self.widgets[(0, -3)].stuck_in_widget: self.widgets[(0, -3)].text = "0"  
        if self.widgets[(0, -2)].text == "" and not self.widgets[(0, -2)].stuck_in_widget: self.widgets[(0, -2)].text = "1"  

        old_scroll = self.scroll
        self.scroll = max(self.scroll_limit[0], min(self.scroll_limit[1], abs(self.cursor_pos[1]) - 1))
        if old_scroll != self.scroll:
            self.clear_window()

    def draw(self, window):
        self.bg_draw(window)

        if self.stuck_in_widget: # selected
            # draw all modules
            on_top = list(self.widgets.values())[-1] # mettre par dessus les autre le selectionner
            for pos, widget in self.widgets.items():
                if pos != (0, 0) and abs(abs(pos[1]) - 1 - self.scroll) > 1:
                    continue
                elif pos != (0, 0):
                    widget.small_pos = (self.og_offset + abs(abs(pos[1]) - 2 - self.scroll)*self.space_between_param, widget.small_pos[1])

                if pos == tuple(self.cursor_pos):
                    widget.highlight()
                else:
                    widget.unhighlight()
                
                if widget.stuck_in_widget:
                    on_top = widget
                else:
                    widget.draw(window)
            on_top.draw(window)

    def bg_draw(self, window):
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

    def additional_draw(self, window):
        if self.stuck_in_widget:
            if abs(5 - 1 - self.scroll) <= 1: 
                ascii_drawer(window, (self.og_offset + abs(5 - 2 - self.scroll)*self.space_between_param, 5), self.mode_img)
                ascii_drawer(window, (self.og_offset + abs(5 - 2 - self.scroll)*self.space_between_param, 65), self.game_modes_img[self.param["mode"]])
            if abs(4 - 1 - self.scroll) <= 1: ascii_drawer(window, (self.og_offset + abs(4 - 2 - self.scroll)*self.space_between_param, 5), self.limit_img)
            if abs(3 - 1 - self.scroll) <= 1: ascii_drawer(window, (self.og_offset + abs(3 - 2 - self.scroll)*self.space_between_param, 5), self.start_img)
            if abs(2 - 1 - self.scroll) <= 1: ascii_drawer(window, (self.og_offset + abs(2 - 2 - self.scroll)*self.space_between_param, 5), self.jump_img)
            if abs(1 - 1 - self.scroll) <= 1: 
                ascii_drawer(window, (self.og_offset + abs(1 - 2 - self.scroll)*self.space_between_param, 5), self.lives_img)
                ascii_drawer(window, (self.og_offset + abs(1 - 2 - self.scroll)*self.space_between_param, 65), self.digit_img[self.param["live"]])