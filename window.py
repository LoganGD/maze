import tkinter as tk

class Window:
    def __init__(self, width, height):
        self.root = tk.Tk()
        self.root.title = "Maze"
        self.canvas = tk.Canvas(width = width, height = height, bg="#d9d9d9")
        self.canvas.pack()

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)