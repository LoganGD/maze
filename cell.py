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
            (self.x1+self.x2)/2-3,
            (self.y1+self.y2)/2-3,
            (self.x1+self.x2)/2+3,
            (self.y1+self.y2)/2+3, 
            fill = color, 
            outline = color
        )