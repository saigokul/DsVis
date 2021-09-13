from mainwindow.ds.dsgui.queue_gui import QUEUEgui, convert


class QUEUE:
    def __init__(self, root):
        self.length = 10
        self.array = ['-'] * self.length
        self.front = -1
        self.rear = -1
        self.gui = QUEUEgui(root, self)

    def enqueue(self, val):
        if (self.rear == self.length - 1):
            return '\nOverflow!'
        elif (self.front == -1 and self.rear == -1):
            self.front = self.rear = 0
        else:
            self.rear += 1
        blink_color = '#0000fc'
        self.array[self.rear] = val
        self.gui.blink_highlight(str(self.rear) + '-b', blink_color)
        self.gui.set_data(str(self.rear) + '-t', int(val))
        return '\nDone'

    def dequeue(self):
        if (self.front == -1 or self.front > self.rear):
            return '\nUnderflow!'
        else:
            j = self.array[self.front]
            self.array[self.front] = '-'
            self.gui.blink_highlight(str(self.front) + '-b')
            self.gui.set_data(str(self.front) + '-t', '-')
            self.front += 1
            if (self.front > self.rear):
                self.front = self.rear = -1
            return '\nValue : ' + convert(j)

    def peek(self):
        if (self.front == -1 or self.front > self.rear):
            return '\nQueue is empty'
        else:
            blink_color = '#0000fc'
            self.gui.blink_highlight(str(self.front) + '-b', blink_color)
            return '\n' + convert(self.array[self.front])
