import time
import random

class Line:
    def __init__(self, x1, y1, x2 ,y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=2
        )

class Cell:
    def __init__(self, win, x1, y1, x2, y2):
        self.has_left_wall = 1
        self.has_right_wall = 1
        self.has_top_wall = 1
        self.has_bottom_wall = 1
        self._win = win
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.visited = False
        
    def draw(self):
        bottom_wall = Line(self.x1,self.y2,self.x2,self.y2)
        left_wall = Line(self.x1,self.y1,self.x1,self.y2)        
        right_wall = Line(self.x2,self.y1,self.x2,self.y2)
        top_wall = Line(self.x1,self.y1,self.x2,self.y1)

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
            (self.x1+self.x2)/2,
            (self.y1+self.y2)/2,
            (to_cell.x1+to_cell.x2)/2,(to_cell.y1+to_cell.y2)/2
        )
        move.draw(self._win.canvas, color)

    def draw_center(self, color):
        self._win.canvas.create_oval(
            (self._x1+self._x2)/2-3,
            (self._y1+self._y2)/2-3,
            (self._x1+self._x2)/2+3,
            (self._y1+self._y2)/2+3, 
            fill = color, 
        )

class Maze:
    def __init__(self, win, width, height, num_cols, num_rows, pad):
        self.win = win
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.sizex = (width-2*pad)/num_cols
        self.sizey = (height-2*pad)/num_rows
        self.pad = pad
        self.make_grid()
        self.break_entrance_and_exit()
        self.break_walls_r(0, 0)
        self.posx1 = 0
        self.posy1 = 0
        self.posx2 = 0
        self.posy2 = 0

    def make_grid(self):
        self.cells = []
        for i in range(self.num_cols):
            col_of_cells = []
            for j in range(self.num_rows):
                cell = Cell(
                    self.win,
                    self.pad+i*self.sizex,
                    self.pad+j*self.sizey,
                    self.pad+(i+1)*self.sizex,
                    self.pad+(j+1)*self.sizey,
                )
                cell.draw()
                col_of_cells.append(cell)
            self.cells.append(col_of_cells)
        self.win.redraw()

    def animate(self):
        #if self.speed >= 0:
            self.win.redraw()
            time.sleep(0.05)

    def break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = 0
        self.cells[0][0].draw()
        self.animate()
        self.cells[self.num_cols-1][self.num_rows-1].has_bottom_wall = 0
        self.cells[self.num_cols-1][self.num_rows-1].draw()
        self.animate()

    def break_walls_r(self, i, j):
        self.cells[i][j].visited = True
        while True:
            lst = []
            if 0 < i and self.cells[i-1][j].visited == False:
                lst.append((i-1, j))
            if 0 < j and self.cells[i][j-1].visited == False:
                lst.append((i, j-1))
            if i < self.num_cols - 1 and self.cells[i+1][j].visited == False:
                lst.append((i+1, j))
            if j < self.num_rows - 1 and self.cells[i][j+1].visited == False:
                lst.append((i, j+1))
            if len(lst) == 0:
                break
            
            dest = lst[random.randint(0,len(lst)-1)]

            if dest[0] == i-1:
                self.cells[i][j].has_left_wall = 0
                self.cells[i][j].draw()
                self.cells[i-1][j].has_right_wall = 0
                self.cells[i-1][j].draw()
            if dest[1] == j-1:
                self.cells[i][j].has_top_wall = 0
                self.cells[i][j].draw()
                self.cells[i][j-1].has_bottom_wall = 0
                self.cells[i][j-1].draw()
            if dest[0] == i+1:
                self.cells[i][j].has_right_wall = 0
                self.cells[i][j].draw()
                self.cells[i+1][j].has_left_wall = 0
                self.cells[i+1][j].draw()
            if dest[1] == j+1:
                self.cells[i][j].has_bottom_wall = 0
                self.cells[i][j].draw()
                self.cells[i][j+1].has_top_wall = 0
                self.cells[i][j+1].draw()

            self.animate()
            self.break_walls_r(*dest)

    def update_players(self):
        print(1)
    
    def reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.cells[i][j].visited = False

    def solve(self):
        self.reset_cells_visited()
        ans = self._solve_r(0, 0, color="red", trail_color="gray")
        print(ans)
        return ans
    
    def _solve_r(self, i, j, color, trail_color):
        self.animate()
        self.cells[i][j].visited = True
        if i == self.num_cols - 1 and j == self.num_rows -1:
            return True
        if i < self.num_cols - 1 and self.cells[i+1][j].visited == False and self.cells[i][j].has_right_wall == False:
            self.cells[i][j].draw_move(self.cells[i+1][j], color)
            if self._solve_r(i+1, j, color, trail_color) == True:
                return True
            self.cells[i][j].draw_move(self.cells[i+1][j], trail_color)
        if j < self.num_rows - 1 and self.cells[i][j+1].visited == False and self.cells[i][j].has_bottom_wall == False:
            self.cells[i][j].draw_move(self.cells[i][j+1], color)
            if self._solve_r(i, j+1, color, trail_color) == True:
                return True
            self.cells[i][j].draw_move(self.cells[i][j+1], trail_color)
        if 0 < j and self.cells[i][j-1].visited == False and self.cells[i][j].has_top_wall == False:
            self.cells[i][j].draw_move(self.cells[i][j-1], color)
            if self._solve_r(i, j-1, color, trail_color) == True:
                return True
            self.cells[i][j].draw_move(self.cells[i][j-1], trail_color)
        if 0 < i and self.cells[i-1][j].visited == False and self.cells[i][j].has_left_wall == False:
            self.cells[i][j].draw_move(self.cells[i-1][j], color)
            if self._solve_r(i-1, j, color, trail_color) == True:
                return True
            self.cells[i][j].draw_move(self.cells[i-1][j], trail_color)
        
        return False