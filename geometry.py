import time
import random
from tkinter import Tk, BOTH, Canvas
from window import *

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill = fill_color, width = 2)

class Cell:
    def __init__(self, x1, y1, x2, y2, win, has_left_wall = True, has_right_wall = True, has_top_wall = True, has_bottom_wall = True):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        if self._x1 > self._x2:
            t = self._x1
            self._x1 = self._x2
            self._x2 = t
        if self._y1 > self._y2:
            t = self._y1
            self._y1 = self._y2
            self._y2 = t

        self._win = win

        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall

        self.visited = False

    def draw(self):
        if self.has_left_wall:
            left_color = "black"
        else:
            left_color = "white"
        self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), left_color)
        if self.has_right_wall:
            right_color = "black"
        else:
            right_color = "white"
        self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), right_color)
        if self.has_top_wall:
            top_color = "black"
        else:
            top_color = "white"
        self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), top_color)
        if self.has_bottom_wall:
            bottom_color = "black"
        else:
            bottom_color = "white"
        self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), bottom_color)

    def draw_move(self, to_cell, undo = False):
        if undo:
            color = "gray"
        else:
            color = "red"

        start = Point(self._x1 + (self._x2 - self._x1)//2, self._y1 + (self._y2 - self._y1)//2)
        end = Point(to_cell._x1 + (to_cell._x2 - to_cell._x1)//2, to_cell._y1 + (to_cell._y2 - to_cell._y1)//2)

        self._win.draw_line(Line(start, end), color)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win, seed = None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed == None:
            random.seed()
        else:
            random.seed(seed)

        self._create_cells()

    def _create_cells(self):
        self._cells = []
        for i in range(self._num_cols):
            col = []
            for j in range(self._num_rows):
                cx1 = self._x1 + i * self._cell_size_x
                cy1 = self._y1 + j * self._cell_size_y
                cx2 = self._x1 + (i + 1) * self._cell_size_x
                cy2 = self._y1 + (j + 1) * self._cell_size_y
                cell = Cell(cx1, cy1, cx2, cy2, self._win)
                col.append(cell)
            self._cells.append(col)

        for j in range(self._num_rows):
            for i in range(self._num_cols):
                self._draw_cell(i, j)

        self._entrance = self._cells[0][0]
        self._exit = self._cells[self._num_cols - 1][self._num_rows - 1]

    def _break_entrance_and_exit(self):
        self._entrance.has_top_wall = False
        self._draw_cell(0, 0)
        self._exit.has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i = 0, j = 0):
        self._cells[i][j].visited = True

        while True:
            to_visit = []
            if i > 0 and not self._cells[i - 1][j].visited:
                to_visit.append("left")
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                to_visit.append("right")
            if j > 0 and not self._cells[i][j - 1].visited:
                to_visit.append("top")
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                to_visit.append("bottom")

            if len(to_visit) == 0:
                self._draw_cell(i, j)
                break

            direction = random.choice(to_visit)

            if direction == "left":
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
                self._break_walls_r(i - 1, j)
            elif direction == "right":
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
                self._break_walls_r(i + 1, j)
            elif direction == "top":
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
                self._break_walls_r(i, j - 1)
            elif direction == "bottom":
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
                self._break_walls_r(i, j + 1)

    def _reset_cells_visited(self):
        for j in range(self._num_rows):
            for i in range(self._num_cols):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i = 0, j = 0):
        self._animate()

        cell = self._cells[i][j]
        cell.visited = True

        if cell == self._exit:
            return True
        
        to_visit = []
        if not cell.has_left_wall and not self._cells[i - 1][j].visited:
            to_visit.append((i - 1, j))
        if not cell.has_right_wall and not self._cells[i + 1][j].visited:
            to_visit.append((i + 1, j))
        if not cell.has_top_wall and not cell == self._entrance and not self._cells[i][j - 1].visited:
            to_visit.append((i, j - 1))
        if not cell.has_bottom_wall and not self._cells[i][j + 1].visited:
            to_visit.append((i, j + 1))

        for direction in to_visit:
            k, l = direction
            neighbor = self._cells[k][l]
            cell.draw_move(neighbor)
            if self._solve_r(k, l):
                return True
            else:
                cell.draw_move(neighbor, True)

        return False

    def _draw_cell(self, i, j):
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)