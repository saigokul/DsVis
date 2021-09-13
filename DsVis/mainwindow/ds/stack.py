from mainwindow.ds.dsgui.stack_gui import STACKgui


class STACK:
    def __init__(self, root):
        self.array = None
        self.length = None
        self.top = -1
        self.gui = STACKgui(root, self)

    def push(self, val):
        if (self.top != self.length - 1):
            self.top += 1
            self.array[self.top] = val
            return True
        return False
