from window import *
from geometry import *

def main():
    win = Window(800, 600)

    print("generating maze...")
    m1 = Maze(5, 5, 10, 12, 10, 10, win, 0)

    m1._break_entrance_and_exit()
    m1._break_walls_r()
    m1._reset_cells_visited()

    m1.solve()

    win.wait_for_close()

main()