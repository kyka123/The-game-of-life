from kivy.graphics import Rectangle

from models.board_size import BoardSize
from models.rule import Rule

class Board:
    def __init__(self, size: BoardSize):
        self.size: BoardSize = size
        self.board: list[list[bool | Rectangle]] = [[False for _ in range(self.size.cols)] for _ in range(self.size.rows)]
        self.not_empty_rows: set[int] = set()

    def of(self, i: int, j: int) -> bool | Rectangle:
        if i > self.size.rows - 1 or j > self.size.cols - 1 :
            return False
        return self.board[i][j]

    def set(self, i: int, j: int, value: bool | Rectangle) -> None:
        self.board[i][j] = value
        if value == False and i in self.not_empty_rows and not any(self.board[i]):
            self.not_empty_rows.remove(i)
        if value != False:
            self.not_empty_rows.add(i)
            self.not_empty_rows = set(sorted(self.not_empty_rows))

    def clear(self) -> None:
        self.board = [[False]*self.size.cols for _ in range(self.size.rows)].copy()
        self.not_empty_rows: set[int] = set()

    def set_board_size(self, board_size: BoardSize) -> None:
        self.size = board_size
        self.clear()


    def refresh_board(self, rule: Rule, add_rectangle_to_layout) -> None:
        new_not_empty_rows = set()
        prev_row = [False for _ in range(self.size.cols)]  
        prev_prev_row = [False for _ in range(self.size.cols)]
        rows_to_iter = set()

        if rule.right_boolen_list[0]:
            rows_to_iter = range(self.size.rows)
        else:
            for not_empty_row in self.not_empty_rows:
                rows_to_iter.add(not_empty_row)
                if not_empty_row > 0:
                    rows_to_iter.add(not_empty_row - 1)
                if not_empty_row < self.size.rows - 1:
                    rows_to_iter.add(not_empty_row + 1)
        
        sorted_rows_to_iter = sorted(rows_to_iter)
        for y in sorted_rows_to_iter:
            prev_prev_row = self.board[y].copy()
            prev_val = False
            is_row_empty = True
            
            for x in range(self.size.cols):
                alive_neighbours = 0

                if x > 0:
                    alive_neighbours  += 1 if prev_row[x - 1] != False else 0
                    alive_neighbours  += 1 if prev_val != False else 0
                    if y < self.size.rows - 1:
                        alive_neighbours  += 1 if self.board[y + 1][x - 1] != False else 0
                
                if x < self.size.cols - 1:
                    alive_neighbours  += 1 if prev_row[x + 1] != False else 0
                    alive_neighbours  += 1 if self.board[y][x + 1] != False else 0
                    if y < self.size.rows - 1:
                        alive_neighbours  += 1 if self.board[y + 1][x + 1] else 0

                if y < self.size.rows - 1:
                    alive_neighbours  += 1 if self.board[y + 1][x] else 0

                alive_neighbours += 1 if prev_row[x] != False else 0

                prev_val = self.board[y][x]

                if ((not self.board[y][x]) and rule.right_boolen_list[alive_neighbours]) or (self.board[y][x] and rule.left_boolen_list[alive_neighbours]):
                    self.board[y][x] = add_rectangle_to_layout(x, y)
                else:
                    self.board[y][x] = False

                if is_row_empty:
                    is_row_empty = self.board[y][x] == False
            if not is_row_empty:
                new_not_empty_rows.add(y)

            prev_row = prev_prev_row.copy()

        self.not_empty_rows = new_not_empty_rows

