class BoardSize:
    cell_size: int = 0
    cols: int = 0
    rows: int = 0
    cell_position_by_index_array: list[list[tuple[int, int]]] = [[]]

    def __init__(self, cell_size: int, window_size: tuple[int, int]):
        self.resize_board(cell_size=cell_size, window_size=window_size)

    def resize_board(self, cell_size: int, window_size: tuple[int, int]):
        self.cell_size: int = cell_size
        self.cols = int(window_size[0] / cell_size)
        self.rows = int(window_size[1] / cell_size)
        self.cell_position_by_index_array: list[list[tuple[int, int]]] = [[(x*cell_size, window_size[1] - (y + 1)*cell_size) for x in range(self.cols)] for y in range(self.rows)]
