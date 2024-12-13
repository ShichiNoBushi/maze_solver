import unittest
from geometry import Maze
from window import Window

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        win = Window(800, 600)
        m1 = Maze(5, 5, num_rows, num_cols, 10, 10, win)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

        # win.wait_for_close()

    def test_break_entrance_exit(self):
        num_cols = 12
        num_rows = 10
        win = Window(800, 600)
        m2 = Maze(5, 5, num_rows, num_cols, 10, 10, win)
        m2._break_entrance_and_exit()
        self.assertEqual(m2._cells[0][0].has_top_wall, False)
        self.assertEqual(m2._cells[num_cols - 1][num_rows - 1].has_bottom_wall, False)

        # win.wait_for_close()

    def test_break_walls(self):
        num_cols = 12
        num_rows = 10
        win = Window(800, 600)
        m3 = Maze(5, 5, num_rows, num_cols, 10, 10, win, 0)
        m3._break_entrance_and_exit()
        m3._break_walls_r()
        self.assertEqual(m3._cells[num_cols // 2][num_rows // 2].visited, True)
        m3._reset_cells_visited()
        self.assertEqual(m3._cells[num_cols // 2][num_rows // 2].visited, False)

        # win.wait_for_close()

    def test_solve_maze0(self):
        num_cols = 12
        num_rows = 10
        win = Window(800, 600)
        m4 = Maze(5, 5, num_rows, num_cols, 10, 10, win, 0)
        m4._break_entrance_and_exit()
        m4._break_walls_r()
        m4._reset_cells_visited()

        self.assertEqual(m4.solve(), True)

    def test_solve_maze100(self):
        num_cols = 12
        num_rows = 10
        win = Window(800, 600)
        m4 = Maze(5, 5, num_rows, num_cols, 10, 10, win, 100)
        m4._break_entrance_and_exit()
        m4._break_walls_r()
        m4._reset_cells_visited()

        self.assertEqual(m4.solve(), True)

    def test_solve_maze999(self):
        num_cols = 12
        num_rows = 10
        win = Window(800, 600)
        m4 = Maze(5, 5, num_rows, num_cols, 10, 10, win, 999)
        m4._break_entrance_and_exit()
        m4._break_walls_r()
        m4._reset_cells_visited()

        self.assertEqual(m4.solve(), True)

if __name__ == "__main__":
    unittest.main()