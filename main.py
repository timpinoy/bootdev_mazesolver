from g_helper import *

def main():
    win = Window(800, 600)
    
    #cell1 = Cell(win)
    #cell1.draw(20, 20, 40, 40)
    #cell2 = Cell(win)
    #cell2.right = False
    #cell2.draw(60, 20, 100, 40)
    #cell3 = Cell(win)
    #cell3.bottom = False
    #cell3.draw(20, 60, 40, 80)
    #cell1.draw_move(cell3)
    #cell2.draw_move(cell3, undo=True)

    maze = Maze(20, 20, 8, 8, 20, 20, window=win)

    win.wait_for_close()


main()