import time

from mainwindow.ds.dsgui.sortinsertion_gui import SORTINSERTIONgui, Section, Tag


class SORTINSERTION:
    def __init__(self, root):
        self.array = None
        self.gui = SORTINSERTIONgui(root, self)

    def insertion_sort(self):
        arr = self.array
        n = len(arr)

        Section(self.gui.area, n, self.array, utext='Actual Array : ')
        self.gui.change_fillcolor(0, 0, n)

        for i in range(1, n):
            self.gui.area.update()
            time.sleep(0.5)
            Section(self.gui.area, i - 1, arr, utext='Pass : ' + str(i))
            self.gui.change_fillcolor(0, i - 1, i - 1)
            self.gui.area.itemconfigure(Tag(i, i - 1).box(), fill='#e0a29d')
            key = arr[i]

            # Move elements of arr[0..i-1], that are
            # greater than key, to one position ahead
            # of their current position
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                self.gui.dual_blink(j, j + 1, i - 1)
                j -= 1
            arr[j + 1] = key
            print(i, self.array)

        Section(self.gui.area, n - 1, self.array, utext='Sorted Array : ')
        self.gui.change_fillcolor(0, n, n - 1)
