from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title = "game"
        self.canvas = Canvas(width = width, height = height, bg="#d9d9d9")
        self.canvas.pack()
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()
    
    def wait_for_close(self):
        self.running = True 
        while self.running:
            self.redraw()
        
    def close(self):
        self.running = False

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
    
    def draw_move(self, to_cell, undo=False):
        move = Line(
            Point((self._x1+self._x2)/2,(self._y1+self._y2)/2),
            Point((to_cell._x1+to_cell._x2)/2,(to_cell._y1+to_cell._y2)/2)
        )
        if undo:
            move.draw(self._win.canvas,"gray")
        else:
            move.draw(self._win.canvas,"red")

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
        seed = None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed != None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

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
        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.001)
    
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
    
    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self.num_cols - 1 and j == self.num_rows -1:
            return True
        if 0 < i and self._cells[i-1][j].visited == False and self._cells[i][j].has_left_wall == False:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j) == True:
                return True
            self._cells[i][j].draw_move(self._cells[i-1][j], True)
        if 0 < j and self._cells[i][j-1].visited == False and self._cells[i][j].has_top_wall == False:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1) == True:
                return True
            self._cells[i][j].draw_move(self._cells[i][j-1], True)
        if i < self.num_cols - 1 and self._cells[i+1][j].visited == False and self._cells[i][j].has_right_wall == False:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r(i+1, j) == True:
                return True
            self._cells[i][j].draw_move(self._cells[i+1][j], True)
        if j < self.num_rows - 1 and self._cells[i][j+1].visited == False and self._cells[i][j].has_bottom_wall == False:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1) == True:
                return True
            self._cells[i][j].draw_move(self._cells[i][j+1], True)
        return False

def main():
    width, height = 1280, 720
    num_rows, num_cols = 20, 36
    win = Window(width, height)

    maze = Maze(20, 20, num_rows, num_cols, (width-40)/num_cols, (height-40)/num_rows, win)
    maze.solve()
    win.wait_for_close()

if __name__ == "__main__":
    main()