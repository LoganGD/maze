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
