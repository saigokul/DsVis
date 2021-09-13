from mainwindow.ds.dsgui.sortselection_gui import SORTSELECTIONgui, Section, SectionTag


class SORTSELECTION:
    def __init__(self, root):
        self.array = None
        self.gui = SORTSELECTIONgui(root, self)

    def selection_sort(self):
        arr = self.array
        n = len(arr)

        Section(self.gui.area, n, self.array, utext='Actual Array : ')

        # Traverse through all array elements
        for i in range(n - 1):

            # Find the minimum element in remaining
            # unsorted array
            Section(self.gui.area, i, arr, utext='pass : ' + str(i + 1))
            self.gui.change_fillcolor(0, i - 1, i)
            min_idx = i
            self.gui.set_info(SectionTag(i).lower(), 'Finding minimum ...')
            for j in range(i, n):
                self.gui.blink_higlight(j, i)
                if arr[min_idx] > arr[j]:
                    min_idx = j
            self.gui.set_info(SectionTag(i).lower(), 'Minimum = ' + str(arr[min_idx]))
            self.gui.blink_higlight(min_idx, i, True)
            # Swap the found minimum element with
            # the first element
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            self.gui.dual_blink(i, min_idx, i, swap=True)
            self.gui.change_fillcolor(0, i, i)
            print(i, self.array)

        Section(self.gui.area, n - 1, self.array, utext='Sorted Array : ')
        self.gui.change_fillcolor(0, n, n - 1)
