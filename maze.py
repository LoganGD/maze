import time
import random
from cell import Cell

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
        self.draw()
        self.reset_cells_visited()
        self.posx1 = 0
        self.posy1 = 0
        self.posx2 = 0
        self.posy2 = 0

    def make_grid(self):
        self.cells = []
        for i in range(self.num_cols):
            self.cells.append(self.create_col_of_cells(i))

    def create_col_of_cells(self, i):
        col_of_cells = []
        for j in range(self.num_rows):
            cell = Cell(
                self.win,
                self.pad+i*self.sizex,
                self.pad+j*self.sizey,
                self.pad+(i+1)*self.sizex,
                self.pad+(j+1)*self.sizey,
            )
            col_of_cells.append(cell)
        return col_of_cells

    def break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = 0
        self.cells[self.num_cols-1][self.num_rows-1].has_bottom_wall = 0

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
                self.cells[i-1][j].has_right_wall = 0
            if dest[1] == j-1:
                self.cells[i][j].has_top_wall = 0
                self.cells[i][j-1].has_bottom_wall = 0
            if dest[0] == i+1:
                self.cells[i][j].has_right_wall = 0
                self.cells[i+1][j].has_left_wall = 0
            if dest[1] == j+1:
                self.cells[i][j].has_bottom_wall = 0
                self.cells[i][j+1].has_top_wall = 0
            
            self.break_walls_r(*dest)

    def draw_players(self, player1, player2):
        if player2:
            self.cells[self.posx2][self.posy2].draw_center("blue")
        else:
            self.cells[self.posx2][self.posy2].draw_center("#d9d9d9")
        if player1:
            self.cells[self.posx1][self.posy1].draw_center("red")
        else:
            self.cells[self.posx1][self.posy1].draw_center("#d9d9d9")
    
    def reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.cells[i][j].visited = False

    def draw(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.cells[i][j].draw()

    def solve(self, color):
        self.draw_players(False, False)
        return self._solve_r(0, 0, color=color)
    
    def _solve_r(self, i, j, color, trail_color = "#d9d9d9"):
        self.cells[i][j].visited = True
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True
        if self.valid(i+1,j,"right") and self.cells[i+1][j].visited == False:
            self.cells[i][j].draw_move(self.cells[i+1][j], color)
            if self._solve_r(i+1, j, color, trail_color) == True:
                return True
            self.cells[i][j].draw_move(self.cells[i+1][j], trail_color)
        if self.valid(i,j+1,"bottom") and self.cells[i][j+1].visited == False:
            self.cells[i][j].draw_move(self.cells[i][j+1], color)
            if self._solve_r(i, j+1, color, trail_color) == True:
                return True
            self.cells[i][j].draw_move(self.cells[i][j+1], trail_color)
        if self.valid(i,j-1,"top") and self.cells[i][j-1].visited == False:
            self.cells[i][j].draw_move(self.cells[i][j-1], color)
            if self._solve_r(i, j-1, color, trail_color) == True:
                return True
            self.cells[i][j].draw_move(self.cells[i][j-1], trail_color)
        if self.valid(i-1,j,"left") and self.cells[i-1][j].visited == False:
            self.cells[i][j].draw_move(self.cells[i-1][j], color)
            if self._solve_r(i-1, j, color, trail_color) == True:
                return True
            self.cells[i][j].draw_move(self.cells[i-1][j], trail_color)
        return False
    
    def move_first(self, key):
        i, j = self.posx1, self.posy1
        if self.valid(i+1,j,"right") and key == "d":
            self.posx1 += 1
        if self.valid(i,j+1,"bottom") and key == "s":
            self.posy1 += 1
        if self.valid(i,j-1,"top") and key == "w":
            self.posy1 -= 1
        if self.valid(i-1,j,"left") and key == "a":
            self.posx1 -= 1
        if self.posx1 == self.num_cols - 1 and self.posy1 == self.num_rows - 1:
            self.solve("red")
            return True
        return False

    def move_second(self, key):
        i, j = self.posx2, self.posy2
        if self.valid(i+1,j,"right") and key == "Right":
            self.posx2 += 1
        if self.valid(i,j+1,"bottom") and key == "Down":
            self.posy2 += 1
        if self.valid(i,j-1,"top") and key == "Up":
            self.posy2 -= 1
        if self.valid(i-1,j,"left") and key == "Left":
            self.posx2 -= 1
        if self.posx2 == self.num_cols - 1 and self.posy2 == self.num_rows - 1:
            self.solve("blue")
            return True
        return False
    
    def valid(self, i, j, dir):
        if i < 0 or self.num_cols <= i or j < 0 or self.num_rows <= j:
            return False
        if dir == "right" and self.cells[i][j].has_left_wall == True:
            return False
        if dir == "bottom" and self.cells[i][j].has_top_wall == True:
            return False
        if dir == "top" and self.cells[i][j].has_bottom_wall == True:
            return False
        if dir == "left" and self.cells[i][j].has_right_wall == True:
            return False
        return True