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


class BSgui:
    def __init__(self, root, bsobj):
        self.root = root
        self.bsobj = bsobj
        self.main_frame = None
        self.content_frame = None
        self.area = None
        self.inputs = None
        self.input_vars = None
        self.info_tag = 'info'
        self.search_var = StringVar()
        self.back_btn = None
        self.search_btn = None
        self.submit_btn = None
        self.anim_time = 0.25
        self.size = None
        self.setup(root)
        self.setupcanvas()

    def search(self):
        fill_color = '#ccebcc'
        val = self.search_var.get()
        if (self.isinputvalid(val)):
            self.back_btn.state(['disabled'])
            self.search_btn.state(['disabled'])
            self.search_var.set('')
            self.set_info(self.info_tag, 'Searching for ' + convert(int(val)), 'overwrite')
            self.bsobj.binary_search(int(val))
            # time.sleep(2.0)
            self.change_fillcolor(0, len(self.bsobj.array), fill_color)
            self.search_btn.state(['!disabled'])
            self.back_btn.state(['!disabled'])

    def submit(self):
        arr = [i.get() for i in self.input_vars]
        arr2 = []
        for i in arr:
            if (self.isinputvalid(i)):
                arr2.append(int(i))
        if (len(arr2) != 0):
            self.back_btn.state(['disabled'])
            self.submit_btn.state(['disabled'])
            self.bsobj.array = sorted(arr2)
            print(self.bsobj.array)
            self.inputs.clear()
            self.inputs.disable()
            self.draw(self.area)
            self.back_btn.state(['!disabled'])
            self.search_btn.state(['!disabled'])

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

        # Input frame
        input_frame = ttk.Labelframe(toolbar, text='Input', padding=5)
        input_frame.grid(column=0, row=1, columnspan=2, padx=3, pady=5, sticky=(N, S, E, W))

        self.inputs = Entryset(input_frame)
        self.input_vars = self.inputs.input_vars

        # submit button
        submit_btn = ttk.Button(toolbar, text="submit", command=self.submit, cursor='hand2')
        submit_btn.grid(column=0, row=2, sticky=(N, S, E, W), columnspan=2)

        # search entry
        search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=8, validate='key',
                                 validatecommand=valcomm)
        search_entry.grid(column=0, row=3, sticky=E)

        # search button
        search_btn = ttk.Button(toolbar, text='Search', cursor='hand2', width=8, command=self.search)
        search_btn.grid(column=1, row=3, sticky=W)

        for widget in toolbar.winfo_children():
            widget.grid_configure(pady=5, padx=3)

        # content Frame
        content_frame = ttk.Frame(main_frame, borderwidth=5, relief='ridge')
        content_frame.grid(column=0, row=0, sticky=(N, S, E, W), padx=5, pady=5)
        self.content_frame = content_frame
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self.search_btn = search_btn
        self.back_btn = back_btn
        self.submit_btn = submit_btn
        search_btn.state(['disabled'])

    def setupcanvas(self):
        content_frame = self.content_frame
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        pageobj = Page(content_frame)
        pageobj.page.grid(column=0, row=0, sticky=(N, S, E, W))
        self.area = pageobj.area
        self.area.create_text(100, 230, anchor='nw', tags=(self.info_tag))
        k = 'Binary Search \n'
        self.set_info(self.info_tag, k, 'overwrite')

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
        canvas = self.area
        canvas.update()
        self.focus_box(box_tag)
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
        canvas.update()

    def nblinks(self, n, box_tag, blink_color='#ff0000'):
        for i in range(n):
            self.blink_highlight(box_tag, blink_color)

    def check_input(self, val):
        return re.match('^([+-]?[0-9]{1,4})?$', val) is not None or re.match('^([+-]?)?$',
                                                                             val) is not None

    def isinputvalid(self, val):
        return re.match('^[+-]?[0-9]{1,4}$', val) is not None

    def draw(self, canvasobj):
        x = y = 100
        w = h = 56.0
        fill_color = '#ccebcc'
        outline_color = text_color = '#046604'
        for i in range(len(self.bsobj.array)):
            canvasobj.update()
            time.sleep(0.2)
            box_tag = str(i) + '-b'
            text_tag = str(i) + '-t'
            key_tag = str(i) + '-k'
            canvasobj.create_rectangle(x, y, x + w, y + w, outline=outline_color, fill=fill_color, tags=(box_tag),
                                       width=1)
            canvasobj.create_text(x + w / 2.0, y + h / 2.0, fill=text_color, text=convert(self.bsobj.array[i]),
                                  tags=(text_tag))
            canvasobj.create_text(x + w / 2.0, y + h + h / 2.0, fill=text_color, text=i, tags=(key_tag))
            self.focus_box(box_tag)
            x += w + 2

    def set_info(self, text_tag, val, mode='append'):
        if (mode == 'append'):
            val = self.area.itemcget(text_tag, 'text') + '\n' + val
        self.area.itemconfigure(text_tag, text=val)

    def change_fillcolor(self, start_index, last_index, fillcolor='white'):
        self.area.update()
        for i in range(start_index, last_index + 1):
            self.area.itemconfigure(str(i) + '-b', fill=fillcolor)


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


class Entryset:
    def __init__(self, parent):
        self.valcomm = (parent.register(self.check_input), '%P')
        self.n = 10
        self.table = {}
        self.input_entrys = []
        self.input_vars = [StringVar() for i in range(self.n) if i or not i]

        for i in range(self.n):
            a = ttk.Entry(parent, textvariable=self.input_vars[i], width=8, validate='key',
                          validatecommand=self.valcomm)
            a.grid(column=0, row=i, sticky=E)
            self.table[a] = i
            self.input_entrys.append(a)

        for i, input_entry in enumerate(self.input_entrys):
            input_entry.bind('<KeyRelease>', lambda e: self.action(e.widget, e.keycode))

    def check_input(self, val):
        return re.match('^([+-]?[0-9]{1,4})?$', val) is not None or re.match('^([+-]?)?$',
                                                                             val) is not None

    def action(self, input_entry, keycode):
        if (keycode == 13 or keycode == 40):
            ind = self.table[input_entry]
            if (ind != self.n - 1):
                self.input_entrys[ind + 1].focus_set()
        elif (keycode == 38):
            ind = self.table[input_entry]
            if (ind != 0):
                self.input_entrys[ind - 1].focus_set()

    def disable(self):
        for i in self.input_entrys:
            i.state(['disabled'])

    def clear(self):
        for i in self.input_vars:
            i.set('')
