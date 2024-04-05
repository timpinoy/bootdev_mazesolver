from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("MazeSolver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root,
                               width=width,
                               height=height)
        self.__canvas.pack()
        self.__is_running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__is_running = True
        while self.__is_running:
            self.redraw()

    def close(self):
        self.__is_running = False
        
    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)


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
    def __init__(self, window):
        self.__window = window
        self.left = True
        self.right = True
        self.top = True
        self.bottom = True
        self.__x1 = None
        self.__y1 = None
        self.__x2 = None
        self.__y2 = None

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        if self.left:
            line = Line(Point(self.__x1,self.__y1), Point(self.__x1,self.__y2))
            self.__window.draw_line(line, "red")
        if self.right:
            line = Line(Point(self.__x2,self.__y1), Point(self.__x2,self.__y2))
            self.__window.draw_line(line, "red")
        if self.top:
            line = Line(Point(self.__x1,self.__y1), Point(self.__x2,self.__y1))
            self.__window.draw_line(line, "red")
        if self.bottom:
            line = Line(Point(self.__x1,self.__y2), Point(self.__x2,self.__y2))
            self.__window.draw_line(line, "red")

    def draw_move(self, to_cell, undo=False):
        if undo:
            color = "gray"
        else:
            color = "red"
        p1 = Point((self.__x1 + self.__x2) // 2, (self.__y1 + self.__y2) //2)
        p2 = Point((to_cell.__x1 + to_cell.__x2) // 2, (to_cell.__y1 + to_cell.__y2) //2)
        self.__window.draw_line(Line(p1, p2), color)