import unittest

from g_helper import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_rows,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_cols,
        )
    
    def test_maze_create_cells2(self):
        num_cols = 2
        num_rows = 20
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_rows,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_cols,
        )

    def test_maze_create_cells3(self):
        num_cols = 1
        num_rows = 1
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            m1._cells[0][0]._x1,
            0,
        )
        self.assertEqual(
            m1._cells[0][0]._y1,
            0,
        )

    def test_maze_break_entrance_and_exit1(self):
        num_cols = 1
        num_rows = 1
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            m1._cells[0][0].top,
            False,
        )
        self.assertEqual(
            m1._cells[0][0].bottom,
            False,
        )
    
    def test_maze_break_entrance_and_exit2(self):
        num_cols = 5
        num_rows = 20
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            m1._cells[0][0].top,
            False,
        )
        self.assertEqual(
            m1._cells[19][4].bottom,
            False,
        )


if __name__ == "__main__":
    unittest.main()