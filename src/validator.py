# noinspection PyMethodMayBeStatic
class SudokuValidator:
    def __init__(self, grid):
        self.grid = grid

    @property
    def size(self):
        return len(self.grid)

    def is_valid(self):
        return self.is_rows_valid() and self.is_columns_valid() and self.is_subgrids_valid()

    def is_rows_valid(self):
        for row in self.grid:
            if not self.is_valid_group(row):
                return False
        return True

    def is_columns_valid(self):
        for col in range(self.size):
            column = [self.grid[row][col] for row in range(self.size)]
            if not self.is_valid_group(column):
                return False
        return True

    def is_subgrids_valid(self):
        subgrid_size = int(self.size ** 0.5)
        for i in range(0, self.size, subgrid_size):
            for j in range(0, self.size, subgrid_size):
                subgrid = [self.grid[x][y] for x in range(i, i + subgrid_size) for y in range(j, j + subgrid_size)]
                if not self.is_valid_group(subgrid):
                    return False
        return True

    def is_valid_group(self, group):
        return len(set(value for cell in group if (value := cell.GetValue()) != '')) == self.size

    def is_valid_cell(self, row_idx, col_idx, value):
        if any(value in cell.GetValue() for idx, cell in enumerate(self.grid[row_idx]) if idx != col_idx):
            return False

        if any(row[col_idx].GetValue() == value for idx, row in enumerate(self.grid) if idx != row_idx):
            return False

        subgrid_size = int(self.size ** 0.5)
        start_row = (row_idx // subgrid_size) * subgrid_size
        start_col = (col_idx // subgrid_size) * subgrid_size

        for r_idx in range(subgrid_size):
            for c_idx in range(subgrid_size):
                if start_row + r_idx == row_idx and start_col + c_idx == col_idx:
                    continue
                if self.grid[start_row + r_idx][start_col + c_idx].GetValue() == value:
                    return False

        return True
