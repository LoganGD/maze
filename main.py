import tkinter as tk
import time
import random
import sys

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

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )

class Cell:
    def __init__(self, win):
        self.has_left_wall = 1
        self.has_right_wall = 1
        self.has_top_wall = 1
        self.has_bottom_wall = 1
        self._win = win
        self.visited = False
        
    def draw(self):
        bottom_wall = Line(Point(self._x1,self._y2),Point(self._x2,self._y2))
        left_wall = Line(Point(self._x1,self._y1),Point(self._x1,self._y2))
        right_wall = Line(Point(self._x2,self._y1),Point(self._x2,self._y2))
        top_wall = Line(Point(self._x1,self._y1),Point(self._x2,self._y1))

        self.wall(bottom_wall,self.has_bottom_wall)
        self.wall(left_wall,self.has_left_wall)
        self.wall(right_wall,self.has_right_wall)
        self.wall(top_wall,self.has_top_wall)

    def wall(self, line, color):
        if color:
            line.draw(self._win.canvas, "black")
        else:
            line.draw(self._win.canvas, "#d9d9d9")
    
    def draw_move(self, to_cell, color):
        move = Line(
            Point((self._x1+self._x2)/2,(self._y1+self._y2)/2),
            Point((to_cell._x1+to_cell._x2)/2,(to_cell._y1+to_cell._y2)/2)
        )
        move.draw(self._win.canvas, color)

    def draw_center(self, color):
        self._win.canvas.create_oval((self._x1+self._x2)/2-3,(self._y1+self._y2)/2-3,(self._x1+self._x2)/2+3,(self._y1+self._y2)/2+3, fill = color, outline = color)

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
        speed,
        second,
        seed = None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.second = second
        if seed != None:
            random.seed(seed)
        self.set_speed(speed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(num_cols - 1, num_rows - 1)
        self._reset_cells_visited()
        self.posx = 0
        self.posy = 0
        self.posx2 = 0
        self.posy2 = 0
        self.draw_pos()
        if self.second:
            self.draw_pos2()

    def _create_cells(self):
        self._cells = []    
        
        for i in range(self.num_cols):
            col = []
            for j in range(self.num_rows):
                col.append(Cell(self.win))
            self._cells.append(col)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)
                
    def _draw_cell(self, i, j):
        self._cells[i][j]._x1 = self.x1 + self.cell_size_x * i
        self._cells[i][j]._y1 = self.y1 + self.cell_size_y * j
        self._cells[i][j]._x2 = self.x1 + self.cell_size_x * (i + 1)
        self._cells[i][j]._y2 = self.y1 + self.cell_size_y * (j + 1)
        self._cells[i][j].draw()

    def _animate(self):
        if self.speed >= 0:
            self.win.redraw()
            time.sleep(self.speed)
    
    def set_speed(self, speed):
        if speed == 1:
            self.speed = 0.2
        elif speed == 2:
            self.speed = 0.05
        elif speed == 3:
            self.speed = 0.012
        elif speed == 4:
            self.speed = 0.003
        elif speed == 5:
            self.speed = 0.0008
        else:
            self.speed = -1

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = 0
        self._cells[0][0].draw()
        self._animate()
        self._cells[self.num_cols-1][self.num_rows-1].has_bottom_wall = 0
        self._cells[self.num_cols-1][self.num_rows-1].draw()
        self._animate()

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            lst = []
            if 0 < i and self._cells[i-1][j].visited == False:
                lst.append((i-1, j))
            if 0 < j and self._cells[i][j-1].visited == False:
                lst.append((i, j-1))
            if i < self.num_cols - 1 and self._cells[i+1][j].visited == False:
                lst.append((i+1, j))
            if j < self.num_rows - 1 and self._cells[i][j+1].visited == False:
                lst.append((i, j+1))
            if len(lst) == 0:
                break
            
            dest = lst[random.randint(0,len(lst)-1)]

            if dest[0] == i-1:
                self._cells[i][j].has_left_wall = 0
                self._cells[i][j].draw()
                self._cells[i-1][j].has_right_wall = 0
                self._cells[i-1][j].draw()
            if dest[1] == j-1:
                self._cells[i][j].has_top_wall = 0
                self._cells[i][j].draw()
                self._cells[i][j-1].has_bottom_wall = 0
                self._cells[i][j-1].draw()
            if dest[0] == i+1:
                self._cells[i][j].has_right_wall = 0
                self._cells[i][j].draw()
                self._cells[i+1][j].has_left_wall = 0
                self._cells[i+1][j].draw()
            if dest[1] == j+1:
                self._cells[i][j].has_bottom_wall = 0
                self._cells[i][j].draw()
                self._cells[i][j+1].has_top_wall = 0
                self._cells[i][j+1].draw()

            self._animate()
            self._break_walls_r(*dest)
        
    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False
    
    def solve(self, color, trail_color):
        self.erase_pos()
        self.erase_pos2()
        return self._solve_r(0, 0, color, trail_color)
    
    def _solve_r(self, i, j, color, trail_color):
        self._animate()
        self._cells[i][j].visited = True
        if i == self.num_cols - 1 and j == self.num_rows -1:
            return True
        if i < self.num_cols - 1 and self._cells[i+1][j].visited == False and self._cells[i][j].has_right_wall == False:
            self._cells[i][j].draw_move(self._cells[i+1][j], color)
            if self._solve_r(i+1, j, color, trail_color) == True:
                return True
            self._cells[i][j].draw_move(self._cells[i+1][j], trail_color)
        if j < self.num_rows - 1 and self._cells[i][j+1].visited == False and self._cells[i][j].has_bottom_wall == False:
            self._cells[i][j].draw_move(self._cells[i][j+1], color)
            if self._solve_r(i, j+1, color, trail_color) == True:
                return True
            self._cells[i][j].draw_move(self._cells[i][j+1], trail_color)
        if 0 < j and self._cells[i][j-1].visited == False and self._cells[i][j].has_top_wall == False:
            self._cells[i][j].draw_move(self._cells[i][j-1], color)
            if self._solve_r(i, j-1, color, trail_color) == True:
                return True
            self._cells[i][j].draw_move(self._cells[i][j-1], trail_color)
        if 0 < i and self._cells[i-1][j].visited == False and self._cells[i][j].has_left_wall == False:
            self._cells[i][j].draw_move(self._cells[i-1][j], color)
            if self._solve_r(i-1, j, color, trail_color) == True:
                return True
            self._cells[i][j].draw_move(self._cells[i-1][j], trail_color)
        
        return False
    
    def move(self, dir, trail_color):
        self.erase_pos()
        self.erase_pos2()
        if dir == "Right" and self.posx < self.num_cols - 1 and self._cells[self.posx][self.posy].has_right_wall == False:
            self.posx += 1
        if dir == "Down" and self.posy < self.num_rows - 1 and self._cells[self.posx][self.posy].has_bottom_wall == False:
            self.posy += 1
        if dir == "Up" and 0 < self.posy and self._cells[self.posx][self.posy].has_top_wall == False:
            self.posy -= 1
        if dir == "Left" and 0 < self.posx and self._cells[self.posx][self.posy].has_left_wall == False:
            self.posx -= 1
        if self.second and dir == "d" and self.posx2 < self.num_cols - 1 and self._cells[self.posx2][self.posy2].has_right_wall == False:
            self.posx2 += 1
        if self.second and dir == "s" and self.posy2 < self.num_rows - 1 and self._cells[self.posx2][self.posy2].has_bottom_wall == False:
            self.posy2 += 1
        if self.second and dir == "w" and 0 < self.posy2 and self._cells[self.posx2][self.posy2].has_top_wall == False:
            self.posy2 -= 1
        if self.second and dir == "a" and 0 < self.posx2 and self._cells[self.posx2][self.posy2].has_left_wall == False:
            self.posx2 -= 1
        self.draw_pos()
        if self.second:
            self.draw_pos2()
        self._animate()
        if self.posx == self.num_cols - 1 and self.posy == self.num_rows -1:
            self.set_speed(0)
            self.solve("red", trail_color)
        if self.posx2 == self.num_cols - 1 and self.posy2 == self.num_rows -1:
            self.set_speed(0)
            self.solve("blue", trail_color)

    def draw_pos(self):
        self._cells[self.posx][self.posy].draw_center("red")

    def erase_pos(self):
        self._cells[self.posx][self.posy].draw_center("#d9d9d9")
    
    def draw_pos2(self):
        self._cells[self.posx2][self.posy2].draw_center("blue")

    def erase_pos2(self):
        self._cells[self.posx2][self.posy2].draw_center("#d9d9d9")
    
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

def main():
    sys.setrecursionlimit(4500)
    screen = GUI(1280, 720)
    screen.win.root.mainloop()

if __name__ == "__main__":
    main()