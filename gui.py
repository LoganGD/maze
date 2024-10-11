import tkinter as tk
from window import Window
from maze import Maze

class GUI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.win = Window(width, height)
        self.win.root.bind('<KeyPress>', self.on_key_press)
        self.active = False
        self.maze = None
        self.trail_color = "#d9d9d9"
        self.second = False

        tab = "               "
        tk.Label(text=f"Number of rows: 4-50{tab}Number columns: 4-90{tab}Speeds: 0 for off, 1 for very slow, 2 for slow, 3 for medium, 4 for fast, 5 for very fast").pack(pady=10)
        self.rows = self.create_input("Number of rows", "10")
        self.cols = self.create_input("Number of columns", "18")
        self.speed = self.create_input("Speed","3")
        self.trail = tk.IntVar()
        self.players = tk.IntVar()
        tk.Checkbutton(text="Show trail", variable=self.trail, command=self.change_trail).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Checkbutton(text="Second player", variable=self.players, command=self.change_players).pack(side=tk.LEFT, padx=10, pady=10)
        self.button1 = tk.Button(text="Solve", command=self.solve).pack(side=tk.RIGHT, padx=10, pady=10)
        self.button2 = tk.Button(text="Generate", command=self.generate).pack(side=tk.RIGHT, padx=10, pady=10)

    def create_input(self, text, default):
        tk.Label(text=text).pack(side=tk.LEFT, padx=10, pady=10)
        button = tk.Entry(width=5)
        button.pack(side=tk.LEFT, padx=10, pady=10)
        button.insert(0, default)
        return button  
    
    def solve(self):
        if not self.active and self.maze != None:
            self.active = True
            try:
                speed = int(self.speed.get())
                self.maze.set_speed(speed)
                self.maze.solve("green", self.trail_color)
                self.maze = None
                self.active = False
            except:
                self.active = False
    
    def generate(self):
        if not self.active:
            self.active = True
            try:
                num_rows = int(self.rows.get())
                num_cols = int(self.cols.get())
                speed = int(self.speed.get())
                if num_rows < 4 or num_rows > 50 or num_cols < 4 or num_cols > 90 or speed < 0 or speed > 5:
                    raise ValueError
                self.win.canvas.delete("all")
                self.maze = Maze(20, 20, num_rows, num_cols, (self.width-40)/num_cols, (self.height-40)/num_rows, self.win, speed, self.second)
                self.maze.second = self.second
                self.active = False
            except:
                self.active = False

    def change_trail(self):
        if self.trail_color == "gray":
            self.trail_color = "#d9d9d9"
        else:
            self.trail_color = "gray"
    
    def on_key_press(self, event):
        if not self.active and self.maze != None:
            self.maze.move(event.keysym, self.trail_color)

    def change_players(self):
        if self.second:
            self.second = False
            if not self.active and self.maze != None:
                self.maze.second = False
                self.maze.erase_pos2()
        else:
            self.second = True
            if not self.active and self.maze != None:
                self.maze.second = True
                self.maze.draw_pos2()