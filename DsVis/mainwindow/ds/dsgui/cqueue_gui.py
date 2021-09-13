from tkinter import *
from tkinter import ttk
from mainwindow.homescreen import Home
import re
import time


def convert(data):
    a = '+'
    if (data < 0):
        data = -data
        a = '-'
    data = str(data)
    data = data.zfill(4)
    return a + data[len(data) - 4:]


class CQUEUEgui:
    def __init__(self, root, arr):
        self.arr = arr
        self.root = root
        self.main_frame = None
        self.content_frame = None
        self.area = None
        self.size_var = StringVar()
        self.push_var = StringVar()
        self.size = None
        self.details_box = None
        self.buttons = None
        self.size_btn = None
        self.size_entry = None
        self.anim_time = 0.25
        self.size = arr.length
        self.enqueue_var = StringVar()
        self.setup(root)
        self.setupcanvas()

    def setup(self, root):
        valcomm = (root.register(self.check_input), '%P')

        main_frame = ttk.Frame(root, padding=5)
        main_frame.grid(column=0, row=0, sticky=(N, S, E, W))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame = main_frame

        toolbar = ttk.Frame(main_frame, padding=5, borderwidth=5, relief='ridge')
        toolbar.grid(column=1, row=0, sticky=(N, S, E, W), padx=5, pady=5)
        back_btn = ttk.Button(toolbar, text="Home", command=self.gohome, cursor='hand2')
        back_btn.grid(column=0, row=0, columnspan=2, sticky=(N, S, E, W))

        # enqueue entry
        enqueue_entry = ttk.Entry(toolbar, textvariable=self.enqueue_var, width=8, validate='key',
                                  validatecommand=valcomm)
        enqueue_entry.grid(column=0, row=2, sticky=E)

        # enqueue button
        enqueue_btn = ttk.Button(toolbar, text='Enqueue', cursor='hand2', width=8, command=self.enqueue)
        enqueue_btn.grid(column=1, row=2, sticky=W)

        # peek button
        peek_btn = ttk.Button(toolbar, text="Peek", command=self.peek, width=8, cursor='hand2')
        peek_btn.grid(column=0, row=3, sticky=E)

        # dequeue button
        dequeue_btn = ttk.Button(toolbar, text="Dequeue", command=self.dequeue, width=8, cursor='hand2')
        dequeue_btn.grid(column=1, row=3, sticky=W)

        # details frame
        details_frame = ttk.Labelframe(toolbar, text='Details', padding=5)
        details_frame.grid(column=0, row=4, columnspan=2, padx=3, pady=5, sticky=(N, S, E, W))

        # details label
        details_label = Text(details_frame, width=20, height=100, bg='black', fg='#8ceb6c')
        details_label.grid(column=0, row=0)
        sb = ttk.Scrollbar(details_frame, orient=VERTICAL, command=details_label.yview)
        sb.grid(column=1, row=0, sticky=(N, S))
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(0, weight=1)
        details_label['yscrollcommand'] = sb.set
        self.details_box = details_label
        toolbar.rowconfigure(4, weight=1)

        for widget in toolbar.winfo_children():
            widget.grid_configure(pady=5, padx=3)

        # content Frame
        content_frame = ttk.Frame(main_frame, borderwidth=5, relief='ridge')
        content_frame.grid(column=0, row=0, sticky=(N, S, E, W), padx=5, pady=5)
        self.content_frame = content_frame
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self.buttons = [enqueue_btn, peek_btn, dequeue_btn, back_btn]

        # self.switch()
        # back_btn.state(['!disabled'])
        self.details_box.delete('1.0', 'end')
        self.details_box.insert('end -1 chars', 'Circular Queue \n\nSize : ' + str(self.size) +
                                '\n Rear : ' + str(self.arr.rear) +
                                '\n Front : ' + str(self.arr.front)
                                )

    def enqueue(self):
        val = self.enqueue_var.get()
        if (self.isinputvalid(val)):
            self.switch()
            print('Enqueue data entry : ', val)
            self.enqueue_var.set('')
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Enqueue( ' + convert(int(val)) + ' ) ...')
            k = self.arr.enqueue(int(val))
            k += '\n Rear : ' + str(self.arr.rear) + '\n Front : ' + str(self.arr.front)
            self.details_box.insert('end -1 chars', k)
            print('length : ', self.arr.length, '\nCircular Queue:', self.arr.array)
            self.switch()

    def peek(self):
        self.switch()
        self.details_box.delete('1.0', 'end')
        self.details_box.insert('end -1 chars', 'Peek ...')
        k = self.arr.peek()
        k += '\n Rear : ' + str(self.arr.rear) + '\n Front : ' + str(self.arr.front)
        self.details_box.insert('end -1 chars', k)
        print('length : ', self.arr.length, '\nCircular Queue:', self.arr.array)
        self.switch()

    def dequeue(self):
        self.switch()
        self.details_box.delete('1.0', 'end')
        self.details_box.insert('end -1 chars', 'Dequeue ...')
        k = self.arr.dequeue()
        k += '\n Rear : ' + str(self.arr.rear) + '\n Front : ' + str(self.arr.front)
        self.details_box.insert('end -1 chars', k)
        print('length : ', self.arr.length, '\nCircular Queue:', self.arr.array)
        self.switch()

    def setupcanvas(self):
        content_frame = self.content_frame
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        pageobj = Page(content_frame)
        pageobj.page.grid(column=0, row=0, sticky=(N, S, E, W))
        self.area = pageobj.area
        self.draw(self.area)

    '''def set_size(self):
        val = self.size_var.get()
        if (val != ''):
            self.size = int(val)
            self.size_btn.state(['disabled'])
            print('Array Size : ', val)
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Stack Size : ' + val)
            self.size_var.set('')
            self.size_entry.state(['disabled'])
            self.draw(self.area)
            self.arr.array = ['-'] * self.size
            self.arr.length = self.size
            print('length : ', self.arr.length, '\nArray:', self.arr.array)
            self.switch()'''

    def gohome(self):
        self.main_frame.destroy()
        Home(self.root, 'DsVis')

    def focus_box(self, box_tag):
        canvas = self.area
        canvas.update()
        k = 100000.0
        extra = 56.0
        coor = canvas.coords(box_tag)
        x1 = canvas.canvasx(0)
        y1 = canvas.canvasy(0)
        x2 = x1 + canvas.winfo_width()
        y2 = y1 + canvas.winfo_height()
        # focusing x-axis
        if (coor[0] > x1):
            # right
            if (coor[2] > x2):
                canvas.xview_moveto((x1 + coor[2] + extra - x2) / k)
        else:
            # left
            canvas.xview_moveto((coor[0] - extra) / k)

        # focusing y-axis
        if (coor[1] > y1):
            # down
            if (coor[3] > y2):
                canvas.yview_moveto((y1 + coor[3] + extra - y2) / k)
        else:
            # up
            canvas.yview_moveto((coor[1] - extra) / k)

    def blink_highlight(self, box_tag, blink_color='#ff0000'):
        self.focus_box(box_tag)
        canvas = self.area
        outline_color = '#046604'
        canvas.itemconfigure(box_tag, outline=blink_color, width=5)
        canvas.update()
        time.sleep(self.anim_time)
        canvas.itemconfigure(box_tag, outline=blink_color, width=4)
        canvas.update()
        time.sleep(self.anim_time)
        canvas.itemconfigure(box_tag, outline=blink_color, width=5)
        canvas.update()
        time.sleep(self.anim_time)
        canvas.itemconfigure(box_tag, outline=outline_color, width=1)

    def set_data(self, text_tag, val):
        if (val != '-'):
            val = convert(val)
        self.area.itemconfigure(text_tag, text=val)

    def check_input(self, val):
        return re.match('^([+-]?[0-9]{1,4})?$', val) is not None or re.match('^([+-]?)?$',
                                                                             val) is not None

    '''def check_input2(self, val):
        return re.match('^([1-9])?$', val) is not None or re.match('^10$', val) is not None'''

    def isinputvalid(self, val):
        return re.match('^[+-]?[0-9]{1,4}$', val) is not None

    def switch(self):
        k = '!disabled' if (self.buttons[0].instate(['disabled'])) else 'disabled'
        for btn in self.buttons:
            btn.state([k])
        return 1

    def draw(self, canvasobj):
        self.switch()
        x = y = 0
        w = h = 56.0
        s = 14.0
        fill_color = '#ccebcc'
        outline_color = text_color = '#046604'
        for i in range(self.size):
            canvasobj.update()
            time.sleep(0.2)
            if (i % 11 == 0):
                x = w
                y += h + h + s
            box_tag = str(i) + '-b'
            text_tag = str(i) + '-t'
            key_tag = str(i) + '-k'
            canvasobj.create_rectangle(x, y, x + w, y + w, outline=outline_color, fill=fill_color, tags=(box_tag),
                                       width=1)
            canvasobj.create_text(x + w / 2.0, y + h / 2.0, fill=text_color, text='-', tags=(text_tag))
            canvasobj.create_text(x + w / 2.0, y + h + h / 2.0, fill=text_color, text=i, tags=(key_tag))
            self.focus_box(box_tag)
            x += w + 5
        self.switch()


class Page:
    def __init__(self, content_frame):
        self.memory = None
        page = ttk.Frame(content_frame)
        # h = ttk.Scrollbar(page, orient=HORIZONTAL)
        # v = ttk.Scrollbar(page, orient=VERTICAL)
        area = Canvas(page, scrollregion=(0, 0, 100000, 100000),
                      # yscrollcommand=v.set, xscrollcommand=h.set,
                      bg='white', cursor='fleur')
        # h['command'] = area.xview
        # v['command'] = area.yview
        area.grid(column=0, row=0, sticky=(N, W, E, S))
        self.page = page
        self.area = area
        area.bind('<ButtonPress-1>', self.scroll_start)
        area.bind('<B1-Motion>', self.scroll_move)
        # h.grid(column=0, row=1, sticky=(W, E))
        # v.grid(column=1, row=0, sticky=(N, S))
        page.columnconfigure(0, weight=1)
        page.rowconfigure(0, weight=1)

    def scroll_start(self, event):
        self.area.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.area.scan_dragto(event.x, event.y, gain=1)
