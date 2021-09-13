from mainwindow.ds.dsgui.bs_gui import BSgui


class BS:
    def __init__(self, root):
        self.array = None
        self.gui = BSgui(root, self)

    def binary_search(self, x):
        blinks = 5
        blink_color = '#0000fc'
        arr = self.array
        low = 0
        high = len(arr) - 1

        while low <= high:
            mid = (high + low) // 2
            if arr[mid] == x:
                text = str(arr[mid]) + ' = ' + str(x) + '\n\nFound'
                self.gui.set_info(self.gui.info_tag, text)
                self.gui.nblinks(blinks, str(mid) + '-b', blink_color)
                print('\nFound at index : ' + str(mid))
                return

            # If x is greater, ignore left half
            elif arr[mid] < x:
                text = str(x) + ' > ' + str(arr[mid]) + ' so search in the right half'
                self.gui.set_info(self.gui.info_tag, text)
                self.gui.nblinks(blinks, str(mid) + '-b')
                self.gui.change_fillcolor(low, mid)
                low = mid + 1

            # If x is smaller, ignore right half
            elif arr[mid] > x:
                text = str(x) + ' < ' + str(arr[mid]) + ' so search in the left half'
                self.gui.set_info(self.gui.info_tag, text)
                self.gui.nblinks(blinks, str(mid) + '-b')
                self.gui.change_fillcolor(mid, high)
                high = mid - 1

        text = '\nNot Found'
        self.gui.set_info(self.gui.info_tag, text)
        print('\nNot Found')
        return
