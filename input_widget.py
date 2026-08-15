from widget import Widget, ascii_drawer, ascii_loader, curses


class InpputWidget(Widget):

    def __init__(self, clear_window, imgs_path="ascii", img_len={}, exit_key="²", del_key="p", restriction_func=None, small_pos=(0, 0), small_path=None, name=""):
        super().__init__(clear_window, small_pos, (0, 0), None, None, small_path, name)

        self.restriction_func = restriction_func if restriction_func != None else lambda x, y: type(x) == str
        self.imagebank = self.load_img_bank(imgs_path, list(img_len.keys()))
        self.img_len = img_len
        self.del_key = del_key
        self.exit_key = exit_key

        self.text = ""
        self.refresh = False

    def load_img_bank(self, path, names):
        bank = {}
        for name in names:
            bank[name] = ascii_loader(path + "/" + name + ".txt")
        return bank

    def move(self, key: str):
        if key == self.exit_key:
            self.stuck_in_widget = False
            self.clear_window()
            self.clear_window()

        if key == self.del_key and len(self.text) > 0:
            self.text = self.text[:-1]
            self.refresh = True
        elif self.restriction_func(key, self.text):
            self.text += key
            self.refresh = True

    def draw(self, window):
        super().draw(window)

        if self.refresh:
            self.refresh = False
            ascii_drawer(window, self.small_pos, (" "*sum([self.img_len[c] for c in (self.text + "4")]) + "\n")*8)

        current_len = 0
        for ch in self.text:
            if self.is_highlighted and not self.stuck_in_widget:
                ascii_drawer(window, (self.small_pos[0], self.small_pos[1] + current_len), self.imagebank[ch], [curses.A_REVERSE])
            else:
                ascii_drawer(window, (self.small_pos[0], self.small_pos[1] + current_len), self.imagebank[ch])
            current_len += self.img_len[ch]

    def small_draw(self, window, attributes=[]):
        if self.text == "":
            super().small_draw(window, attributes)

    def big_draw(self, window, attributes=[]):
        self.small_draw(window, attributes)