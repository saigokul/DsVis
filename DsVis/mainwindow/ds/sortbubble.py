from mainwindow.ds.dsgui.sortbubble_gui import SORTBUBBLEgui, Section, SectionTag


class SORTBUBBLE:
    def __init__(self, root):
        self.array = None
        self.gui = SORTBUBBLEgui(root, self)

    def bubble_sort(self):
        arr = self.array
        n = len(arr)

        Section(self.gui.area, n, self.array, utext='Actual Array : ')

        # Traverse through all array elements
        for i in range(n - 1):
            swaps = 0
            Section(self.gui.area, i, self.array, utext='Pass : ' + str(i + 1))
            self.gui.change_fillcolor(n - i, n - 1, i)
            tag = SectionTag(i).lower()
            # Last i elements are already
            #  in place
            for j in range(0, n - i - 1):
                # traverse the array from 0 to
                # n-i-1. Swap if the element
                # found is greater than the
                # next element
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.gui.dual_blink(j, j + 1, i, swap=True)
                    swaps += 1
                else:
                    self.gui.dual_blink(j, j + 1, i)
                self.gui.set_info(tag, 'Swaps = ' + str(swaps), mode='overwrite')
            self.gui.change_fillcolor(n - i - 1, n - 1, i)

            print(i, self.array)

        Section(self.gui.area, n - 1, self.array, utext='Sorted Array : ')
        self.gui.change_fillcolor(0, n, n - 1)
