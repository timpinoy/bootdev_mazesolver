import time
from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self._root = Tk()
        self._root.title("MazeSolver")
        self._root.protocol("WM_DELETE_WINDOW", self.close)
        self._canvas = Canvas(self._root,
                               width=width,
                               height=height)
        self._canvas.pack()
        self._is_running = False

    def redraw(self):
        self._root.update_idletasks()
        self._root.update()

    def wait_for_close(self):
        self._is_running = True
        while self._is_running:
            self.redraw()

    def close(self):
        self._is_running = False
        
    def draw_line(self, line, fill_color):
        line.draw(self._canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.p1.x, self.p1.y,
                           self.p2.x, self.p2.y,
                           fill=fill_color, width=2)


class Cell:
    def __init__(self, window=None):
        self._window = window
        self.left = True
        self.right = True
        self.top = True
        self.bottom = True
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        if self._window:
            if self.left:
                line = Line(Point(self._x1,self._y1), Point(self._x1,self._y2))
                self._window.draw_line(line, "red")
            if self.right:
                line = Line(Point(self._x2,self._y1), Point(self._x2,self._y2))
                self._window.draw_line(line, "red")
            if self.top:
                line = Line(Point(self._x1,self._y1), Point(self._x2,self._y1))
                self._window.draw_line(line, "red")
            if self.bottom:
                line = Line(Point(self._x1,self._y2), Point(self._x2,self._y2))
                self._window.draw_line(line, "red")

    def draw_move(self, to_cell, undo=False):
        if undo:
            color = "gray"
        else:
            color = "red"
        p1 = Point((self._x1 + self._x2) // 2, (self._y1 + self._y2) //2)
        p2 = Point((to_cell.__x1 + to_cell.__x2) // 2, (to_cell.__y1 + to_cell.__y2) //2)
        self._window.draw_line(Line(p1, p2), color)


class Maze:
    def __init__(self,  x1, y1,
                 num_rows, num_cols,
                 cell_size_x, cell_size_y, window=None):
       self._window = window
       self._x1 = x1
       self._y1 = y1
       self._num_rows = num_rows
       self._num_cols = num_cols
       self._cell_size_x = cell_size_x
       self._cell_size_y = cell_size_y
       self._create_cells()

    def _create_cells(self):
        self._cells = []
        for i in range(self._num_rows):
            line = []
            for j in range(self._num_cols):
                c = Cell(self._window)
                line.append(c)
            self._cells.append(line)
        
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        c = self._cells[i][j]
        x1 = self._x1 + self._cell_size_x * j
        y1 = self._y1 + self._cell_size_y * i
        x2 = self._x1 + self._cell_size_x * (j + 1)
        y2 = self._y1 + self._cell_size_y * (i + 1)
        c.draw(x1, y1, x2, y2)
        c.left = True
        c.top = False

        self._animate()

    def _animate(self):
        if self._window:
            self._window.redraw()
            time.sleep(0.05)