from g_helper import *

def main():
    win = Window(800, 600)
    maze = Maze(20, 20, 20, 30, 20, 20, window=win)
    maze.solve()
    win.wait_for_close()


main()