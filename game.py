from widget_manager import Widget, WidgetManager, ascii_drawer, ascii_loader
from pi_quizz import PiQuizz


class Game(WidgetManager):

    def __init__(self, clear_window, go_to_menu_func, param: dict = {"type": "classic", "live": 3}):
        super().__init__(clear_window, (0, 0), (0, 0), None, None, "Game")

        self.stuck_in_widget = True
        self.img_big = ""
        self.widgets = {
            (1, 0): Widget(clear_window, (29, 115), on_click_func=go_to_menu_func, small_path="ascii/Menu.txt", name="menu button"),
            (0, 0): Widget(clear_window, name="invisible"),
            (-1, 0): Widget(clear_window, (29, 3), on_click_func=self.reset, small_path="ascii/Restart.txt", name="restart")
        }

        # speccial invisible resting point for selector
        self.widgets[(0, 0)].img_small = ""
        self.widgets[(0, 0)].onclick = lambda: None


        self.Quizz = PiQuizz(param, self.end)
        self.param = param

        # data for visual
        self.current_seq = "3."
        self.digit_len = (12, 6, 11, 11, 13, 11, 11, 11, 11, 11)
        self.stop_loop = False
        self.won = False

        #img loading:
        self.heart_img = ascii_loader("ascii/Heart.txt")
        self.dot_img = ascii_loader("ascii/Dot.txt")
        self.digit_img = [ascii_loader(f"ascii/digit/{i}.txt") for i in range(10)]
        self.gg_img = ascii_loader("ascii/Gg.txt")
        self.lost_img = ascii_loader("ascii/Lost.txt")
        self.end_img = (self.lost_img, self.gg_img)

    def update_param(self, param):
        self.param = param
        self.Quizz.param = param

    def move(self, key:str):
        super().move(key)
        if key.isdigit() and not self.stop_loop:
            progressed = self.Quizz.input(key)

            if progressed:
                self.current_seq += self.Quizz.get_previus_digits(1)
                if len(self.current_seq) > 5:
                    self.current_seq = self.current_seq[1:]
            
            else:
                self.clear_window()
    
    def end(self, state: bool):
        self.clear_window()
        self.stop_loop = True
        self.won = state

    def additional_draw(self, window):
        # necessary reset
        ascii_drawer(window, (15, 65), (" "*62 + "\n")*8)
        ascii_drawer(window, (0, 75), (" "*14*len(str(self.Quizz.pos)) + "\n")*8)

        # draw lives
        if not self.stop_loop:
            for i in range(self.Quizz.live):
                ascii_drawer(window, (0, i*15), self.heart_img)

        # draw "score"
        current_len = 0
        for i in range(len(str(self.Quizz.pos))):
            digit = int(str(self.Quizz.pos)[i])
            ascii_drawer(window, (0, 75 + current_len), self.digit_img[digit])
            current_len += self.digit_len[digit]

        # draw_pi
        current_len = 0
        for i in range(len(self.current_seq)):
            digit = self.current_seq[i]
            
            if digit == ".":
                ascii_drawer(window, (15, 65 + current_len), self.dot_img)
                current_len += 3
            else:
                ascii_drawer(window, (15, 65 + current_len), self.digit_img[int(digit)])
                current_len += self.digit_len[int(digit)]

        if self.stop_loop:
            ascii_drawer(window, (0, 3), self.end_img[int(self.won)])
            if not self.won:
                ascii_drawer(window, (0, 39), self.digit_img[int(self.Quizz.PI[self.Quizz.pos])])

    def reset(self):
        self.clear_window()
        self.Quizz.reset()
        self.current_seq = "3."
        self.stop_loop = False

