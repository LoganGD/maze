from tkinter import Tk, Canvas

class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title = "Maze"
        self.canvas = Canvas(width = width, height = height, bg="#d9d9d9")
        self.canvas.pack()

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()