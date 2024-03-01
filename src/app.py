import wx
from wx import TextCtrl


class SudokuPanel(wx.Panel):

    def __init__(self, parent, rows=9, cols=9):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.grid = wx.GridSizer(rows, cols, 2, 2)
        self.grid_cells = []
        self.actions = {wx.WXK_LEFT: (0, -1), wx.WXK_RIGHT: (0, 1), wx.WXK_UP: (-1, 0), wx.WXK_DOWN: (1, 0)}

        for _ in range(rows):
            cells = []
            for _ in range(cols):
                cell = self.create_number_placeholder()
                cells.append(cell)
                self.grid.Add(cell, 1, wx.EXPAND | wx.ALL | wx.CENTER)
            self.grid_cells.append(cells)

        self.SetSizer(self.grid)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)

    def create_number_placeholder(self):
        text_ctrl = wx.TextCtrl(self)
        text_ctrl.is_invalid_input = False
        text_ctrl.SetMaxLength(1)
        text_ctrl.SetBackgroundColour('white')
        text_ctrl.Bind(wx.EVT_TEXT, self.on_text_change, text_ctrl)
        text_ctrl.SetFont(wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        return text_ctrl

    def on_text_change(self, event):
        number_cell: TextCtrl = event.GetEventObject()
        number: str = event.GetString()
        if number.isdigit() and 0 < int(number) < 10:
            number_cell.is_invalid_input = False
        else:
            number_cell.is_invalid_input = True
        event.Skip()

    def on_key_press(self, event):
        keycode = event.GetKeyCode()

        if keycode in self.actions:
            row, col = self.get_cell_index(keycode, self.FindFocus())
            if row is not None and col is not None:
                self.grid_cells[row][col].SetFocus()

        event.Skip()

    def get_cell_index(self, keycode, current_cell):
        for row_idx in range(self.rows):
            for col_idx in range(self.cols):
                if self.grid_cells[row_idx][col_idx] == current_cell:
                    x, y = self.actions[keycode]
                    return (row_idx + x) % self.rows, (col_idx + y) % self.cols
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
