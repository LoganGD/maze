import sys
from gui import GUI

def main():
    sys.setrecursionlimit(4500)
    screen = GUI(1280, 720)
    screen.win.root.mainloop()

if __name__ == "__main__":
    main()