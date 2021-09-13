from mainwindow.ds.dsgui.arr_gui import ARRgui, convert


class ARR:
    def __init__(self, root):
        self.array = None
        self.length = None
        self.gui = ARRgui(root, self)

    def find_null(self):
        try:
            k = self.array.index('-')
            return k
        except ValueError:
            return -1

    def array_append(self, val):
        k = self.find_null()
        if (k != -1):
            self.array[k] = val
        return k

    def array_search(self, val):
        blink_color = '#0000fc'
        for ind, ele in enumerate(self.array):
            if (ele == val):
                self.gui.blink_highlight(str(ind) + '-b', blink_color)
                return ind
            if (ele == '-'):
                return -1
            self.gui.blink_highlight(str(ind) + '-b')
        return -1

    def array_getat(self, index):
        try:
            val = self.array[index]
            if (val == '-'):
                raise IndexError
            blink_color = '#0000fc'
            self.gui.blink_highlight(str(index) + '-b', blink_color)
            return '\nValue at ' + str(index) + '\nis ' + convert(val)
        except IndexError:
            return '\nIndex out of range!'

    def array_pop(self):
        k = self.find_null() - 1
        if (k == -2):
            k = self.length - 1
        if (k >= 0):
            j = self.array[k]
            self.gui.blink_highlight(str(k) + '-b')
            self.gui.set_data(str(k) + '-t', '-')
            self.array[k] = '-'
            return 'Popped Value :\n' + convert(j)
        else:
            return 'Unable to pop \nan empty array'

    def insert_before(self, act_val, before_val):
        last_index = self.find_null()
        if (last_index == -1):
            return '\nArray is full.'
        index = self.array_search(before_val)
        if (index == -1):
            return '\n' + convert(before_val) + ' does not \nexists'

        for i in range(last_index, index, -1):
            # i is index of hyphen
            # i-1 is index of value
            self.array[i] = self.array[i - 1]
            self.gui.shift(i, i - 1)
        blink_color = '#0000fc'
        self.array[index] = act_val
        self.gui.blink_highlight(str(index) + '-b', blink_color)
        self.gui.set_data(str(index) + '-t', act_val)
        return '\nDone'

    def insert_after(self, act_val, after_val):
        last_index = self.find_null()
        if (last_index == -1):
            return '\nArray is full'
        index = self.array_search(after_val)
        if (index == -1):
            return '\n' + convert(after_val) + ' does not \nexists'
        index += 1
        for i in range(last_index, index, -1):
            # i is index of hyphen
            # i-1 is index of value
            self.array[i] = self.array[i - 1]
            self.gui.shift(i, i - 1)
        blink_color = '#0000fc'
        self.array[index] = act_val
        self.gui.blink_highlight(str(index) + '-b', blink_color)
        self.gui.set_data(str(index) + '-t', act_val)
        return '\nDone'

    def del_at(self, index):
        if (self.length > 0 and self.array[0] == '-'):
            return '\nArray is Empty'
        try:
            k = self.array[index]
            if (k == '-'):
                raise IndexError
        except IndexError:
            return '\nIndex out of Range'
        last_index = self.find_null()
        if (last_index == -1):
            last_index = self.length
        self.array[index] = '-'
        blink_color = '#0000fc'
        self.gui.blink_highlight(str(index) + '-b', blink_color)
        self.gui.set_data(str(index) + '-t', '-')
        for i in range(index, last_index - 1):
            # i is index of hyphen
            # i+1 is index of val
            self.array[i] = self.array[i + 1]
            self.array[i + 1] = '-'
            self.gui.shift(i, i + 1)
        return '\nDone'

    def del_before(self, before_val):
        index = self.array_search(before_val)
        if (index == -1):
            return '\n' + str(before_val) + ' does not exists'
        index -= 1
        if (index == -1):
            return '\n' + str(before_val) + ' is the \nfirst element'
        return self.del_at(index)

    def del_after(self, after_val):
        index = self.array_search(after_val)
        if (index == -1):
            return '\n' + str(after_val) + ' does not exists'
        index += 1
        if (index == self.length or self.array[index] == '-'):
            return '\n' + str(after_val) + ' is the \nlast element'
        return self.del_at(index)
