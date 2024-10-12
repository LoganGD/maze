import sys
from window import Window
from gui import make_gui

second_player_active = None

def on_key_press(key = "nope"):
    return None

def main():
    sys.setrecursionlimit(4500)
    width, height = 1280, 720
    win = Window(width = width, height = height)
    win.root.bind('<KeyPress>', on_key_press)
    make_gui(win, width, height)
    win.root.mainloop()

if __name__ == "__main__":
    main()