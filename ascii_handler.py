
def ascii_loader(path):
    text = ""
    with open(path) as f:
        for line in f:
            text += line
    return text

def ascii_drawer(window, pos, text, attribute=[]):
    text = text.split("\n")
    for i in range(len(text)):
            window.addstr(pos[0] + i, pos[1], text[i], *attribute)