import time
import random
from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self._root = Tk()
        self._root.title("MazeSolver")
        self._root.protocol("WM_DELETE_WINDOW", self.close)
        self._canvas = Canvas(self._root,
                               width=width,
                               height=height,
                               bg="white")
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
        self.visited = False
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
            # left
            line = Line(Point(self._x1,self._y1), Point(self._x1,self._y2))
            if self.left:
                self._window.draw_line(line, "black")
            else:
                self._window.draw_line(line, "white")
            # right
            line = Line(Point(self._x2,self._y1), Point(self._x2,self._y2))
            if self.right:
                self._window.draw_line(line, "black")
            else:
                self._window.draw_line(line, "white")
            # top
            line = Line(Point(self._x1,self._y1), Point(self._x2,self._y1))
            if self.top:
                self._window.draw_line(line, "black")
            else:
                self._window.draw_line(line, "white")
            # bottom
            line = Line(Point(self._x1,self._y2), Point(self._x2,self._y2))
            if self.bottom:
                self._window.draw_line(line, "black")
            else:
                self._window.draw_line(line, "white")

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
                 cell_size_x, cell_size_y,
                 window=None, seed=None):
       self._window = window
       self._x1 = x1
       self._y1 = y1
       self._num_rows = num_rows
       self._num_cols = num_cols
       self._cell_size_x = cell_size_x
       self._cell_size_y = cell_size_y
       if not seed:
           random.seed(seed)
       self._create_cells()
       self._break_entrance_and_exit()
       self._break_walls_r(0, 0)

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

        self._animate()

    def _animate(self):
        if self._window:
            self._window.redraw()
            time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].top = False
        self._draw_cell(0, 0)
        self._cells[self._num_rows-1][self._num_cols-1].bottom = False
        self._draw_cell(self._num_rows-1, self._num_cols-1)

    def _break_walls_r(self, i, j):
        cur_cell = self._cells[i][j]
        cur_cell.visited = True
        while True:
            # get list of possible moves
            possible_move_cells = []
            ## L
            if j > 0:
                if not self._cells[i][j-1].visited:
                    possible_move_cells.append("L")
            ## R
            if j < self._num_cols - 1:
                if not self._cells[i][j+1].visited:
                    possible_move_cells.append("R")
            ## U
            if i > 0:
                if not self._cells[i-1][j].visited:
                    possible_move_cells.append("U")
            ## D
            if i < self._num_rows - 1:
                if not self._cells[i+1][j].visited:
                    possible_move_cells.append("D")
            print(possible_move_cells)
            if len(possible_move_cells) == 0:
                self._draw_cell(i, j)
                break
            else:
                r = random.randrange(len(possible_move_cells))
                direction = possible_move_cells[r]
                if direction == "L":
                    cur_cell.left = False
                    self._cells[i][j-1].right = False
                    self._break_walls_r(i, j-1)
                if direction == "R":
                    cur_cell.right = False
                    self._cells[i][j+1].left = False
                    self._break_walls_r(i, j+1)
                if direction == "U":
                    cur_cell.top = False
                    self._cells[i-1][j].bottom = False
                    self._break_walls_r(i-1, j)
                if direction == "D":
                    cur_cell.bottom = False
                    self._cells[i+1][j].top = False
                    self._break_walls_r(i+1, j)

