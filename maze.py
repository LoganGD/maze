import random
import time
from cell import Cell

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