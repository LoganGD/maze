import sys
from window import Window
from gui import make_gui

def main():
    sys.setrecursionlimit(4500)
    width, height = 1280, 720
    win = Window(width = width, height = height)
    global maze
    make_gui(win, width, height)
    win.root.mainloop()

if __name__ == "__main__":
    main()