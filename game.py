from widget_manager import Widget, WidgetManager, ascii_drawer, ascii_loader
from pi_quizz import PiQuizz


class Game(WidgetManager):

    def __init__(self, clear_window, param: dict = {"type": "classic", "live": 3}):
        super().__init__(clear_window, (0, 0), (0, 0), None, None, "Game")

        self.widgets = {
            (0, 0): Widget(clear_window)
        }

        self.Quizz = PiQuizz(param, self.end)

        self.current_seq = "3."
        self.digit_len = [12, 6, 11, 11, 13, 11, 11, 11, 11, 11]

        #img loading:
        self.heart_img = ascii_loader("ascii/Heart.txt")
        self.dot_img = ascii_loader("ascii/Dot.txt")
        self.digit_img = [ascii_loader(f"ascii/digit/{i}.txt") for i in range(10)]

    def move(self, key:str):
        super().move(key)

        if key.isdigit():
            progressed = self.Quizz.input(key)

            if progressed:
                self.current_seq += self.Quizz.get_previus_digits(1)
                if len(self.current_seq) > 5:
                    self.current_seq = self.current_seq[1:]
            
            else:
                self.clear_window()
    
    def end(self):
        self.clear_window()
    
    def additional_draw(self, window):
        # draw lives
        for i in range(self.Quizz.live):
            ascii_drawer(window, (0, i*15), self.heart_img)

        # clear old pi
        ascii_drawer(window, (10, 30), (" "*62 + "\n")*6)
        # draw_pi
        current_len = 0
        for i in range(len(self.current_seq)):
            digit = self.current_seq[i]
            
            if digit == ".":
                ascii_drawer(window, (10, 30 + current_len), self.dot_img)
                current_len += 3
            else:
                ascii_drawer(window, (10, 30 + current_len), self.digit_img[int(digit)])
                current_len += self.digit_len[int(digit)]