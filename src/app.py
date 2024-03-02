import wx
from wx import TextCtrl

from validator import SudokuValidator


class SudokuPanel(wx.Panel):

    def __init__(self, parent, rows=9, cols=9):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.grid_sizer = wx.GridSizer(rows, cols, 2, 2)
        self.grid = []
        self.validator = SudokuValidator(self.grid)
        self.actions = {wx.WXK_LEFT: (0, -1), wx.WXK_RIGHT: (0, 1), wx.WXK_UP: (-1, 0), wx.WXK_DOWN: (1, 0)}

        for _ in range(rows):
            cells = []
            for _ in range(cols):
                cell = self.create_number_placeholder()
                cells.append(cell)
                self.grid_sizer.Add(cell, 1, wx.EXPAND | wx.ALL | wx.CENTER)
            self.grid.append(cells)

        self.SetSizer(self.grid_sizer)

    def create_number_placeholder(self):
        text_ctrl = wx.TextCtrl(self, style=wx.TE_NOHIDESEL)
        text_ctrl.SetMaxLength(1)
        text_ctrl.SetBackgroundColour('white')
        text_ctrl.Bind(wx.EVT_CHAR, self.on_char_change)
        text_ctrl.SetFont(wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        text_ctrl.SetValue('')
        text_ctrl.ShowNativeCaret(False)
        return text_ctrl

    def on_char_change(self, event):
        current_cell: TextCtrl = event.GetEventObject()
        keycode = event.GetKeyCode()

        if keycode in self.actions:
            self.on_key_press(keycode)
            return event.Skip()

        if keycode == wx.WXK_BACK:
            current_cell.SetValue('')
            current_cell.SetBackgroundColour('white')

            if self.validator.is_valid():
                self.reset_color()
                current_cell.SetFocus()

            return event.Skip()

        if chr(keycode).isdigit():
            current_cell.SetValue(chr(keycode))
            row, col = self.get_cell_index(self.FindFocus())
            if row is not None and col is not None and not self.validator.is_valid_cell(row, col, chr(keycode)):
                current_cell.SetBackgroundColour('red')
        else:
            current_cell.SetValue('')

        event.Skip()

    def reset_color(self):
        for row in self.grid:
            for cell in row:
                cell.SetFocus()
                cell.SetBackgroundColour('white')

    def on_key_press(self, keycode):
        row, col = self.get_cell_index(self.FindFocus())
        if row is not None and col is not None:
            x, y = self.actions[keycode]
            row, col = (row + x) % self.rows, (col + y) % self.cols
            self.grid[row][col].SetFocus()

    def get_cell_index(self, current_cell):
        for row_idx in range(self.rows):
            for col_idx in range(self.cols):
                if self.grid[row_idx][col_idx] == current_cell:
                    return row_idx, col_idx
        return None, None


class App(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, style=wx.DEFAULT_FRAME_STYLE, title='Sudoku', size=(600, 600))
        self.create_panel()

    def create_panel(self):
        panel = SudokuPanel(self)
        panel.Show()


if __name__ == '__main__':
    app = wx.App()
    frame = App()
    frame.Show()
    app.MainLoop()
