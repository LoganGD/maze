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
    tab = "                   "
    info = f"{info_cols}{tab}{info_rows}{tab*11}"
    tk.Label(text=info).pack(pady=10)
    cols_input = create_input("Number of columns", "9")
    rows_input = create_input("Number of rows", "5")

    label2 = tk.Label(text="WASD to move")
    second_player_active = tk.IntVar()
    def switch_second_player():
        global maze
        global solved
        if maze != None:
            if not solved:
                maze.draw_players(True, second_player_active.get())
            if second_player_active.get():
                label2.config(text="Player 1: WASD, Player 2:Arrows")
            else:
                label2.config(text="WASD to move")
    check = tk.Checkbutton(
        text="Second player", 
        variable=second_player_active, 
        command=switch_second_player
    )
    global maze
    global solved
    global processing
    maze = None
    solved = False
    processing = False
    def generate():
        global maze
        global solved
        global processing
        if not processing:
            try:
                cols = int(cols_input.get())
                rows = int(rows_input.get())
                if cols < 4 or cols > 90 or rows < 4 or rows > 50:
                    raise Exception
            except:
                return None
            processing = True
            win.canvas.delete("all")
            maze = Maze(win,
                width, 
                heigth, 
                int(cols_input.get()),
                int(rows_input.get()),
                pad = 20
            )
            maze.draw_players(True, second_player_active.get())
            win.redraw()
            solved = False
            processing = False
    def solve():
        global maze
        global solved
        global processing
        if not processing and maze != None and solved == False:
            solved = True
            processing = True
            maze.solve("green")
            processing = False
    def on_key_press(key = "nope"):
        global maze
        global solved
        global processing
        if not processing and not solved and maze != None:
            maze.draw_players(False, False)
            solved = maze.move_first(key.keysym)
            if not solved and second_player_active.get():
                solved = maze.move_second(key.keysym)
            if not solved:
                maze.draw_players(True, second_player_active.get())
            win.redraw()
    win.root.bind('<KeyPress>', on_key_press)
    button1 = tk.Button(text="Generate", command=generate)
    button2 = tk.Button(text="Solve", command=solve)
    check.pack(side=tk.LEFT, padx=10, pady=10)
    button2.pack(side=tk.RIGHT, padx=10, pady=10)
    button1.pack(side=tk.RIGHT, padx=10, pady=10)
    label2.pack(side=tk.TOP, padx=10, pady=15) 