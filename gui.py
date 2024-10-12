import tkinter as tk
from maze import Maze

def create_input(text, default=""):
    tk.Label(text=text).pack(side=tk.LEFT, padx=10, pady=10)
    button = tk.Entry(width=5)
    button.pack(side=tk.LEFT, padx=10, pady=10)
    button.insert(0, default)
    return button 

def make_gui(win, width, heigth):
    info_rows = "Number of rows: 4-50"
    info_cols = "Number columns: 4-90"
    info_speed = "Speeds: 1 (slow) to 5 (fast), 0 for off"
    tab = "               "
    info = f"{info_cols}{tab}{info_rows}{tab}{info_speed}"
    tk.Label(text=info).pack(pady=10)
    cols_input = create_input("Number of columns", "9")
    rows_input = create_input("Number of rows", "5")
    speed_input = create_input("Speed","0")

    label2 = tk.Label(text="WASD to move")
    second_player_active = tk.IntVar()
    def switch_second_player():
        if second_player_active.get():
            label2.config(text="Player 1: WASD, Player 2:Arrows")
        else:
            label2.config(text="WASD to move")
    check = tk.Checkbutton(
        text="Second player", 
        variable=second_player_active, 
        command=switch_second_player
    )
    global processing
    processing = False
    def generate():
        global maze
        global processing
        if not processing:
            processing = True
            win.canvas.delete("all")
            maze = Maze(win,
                width, 
                heigth, 
                int(cols_input.get()),
                int(rows_input.get()),
                pad = 20
            )
            processing = False
    def solve():
        try:
            global maze
            global processing
            if not processing:
                processing = True
                maze.solve()
                processing = False
        except NameError:
            raise NameError("No maze")
    button1 = tk.Button(text="Generate", command=generate)
    button2 = tk.Button(text="Solve", command=solve)
    check.pack(side=tk.LEFT, padx=10, pady=10)
    button2.pack(side=tk.RIGHT, padx=10, pady=10)
    button1.pack(side=tk.RIGHT, padx=10, pady=10)
    label2.pack(side=tk.TOP, padx=10, pady=15)