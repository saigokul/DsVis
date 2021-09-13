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


class SORTBUBBLEgui:
    def __init__(self, root, sortbubbleobj):
        self.root = root
        self.sortbubbleobj = sortbubbleobj
        self.main_frame = None
        self.content_frame = None
        self.area = None
        self.inputs = None
        self.input_vars = None
        self.sort_btn = None
        self.back_btn = None
        self.info_tag = 'info'
        self.help = None
        self.anim_time = 0.5
        self.setup(root)
        self.setupcanvas()

    def sort(self):
        arr = [i.get() for i in self.input_vars]
        arr2 = []
        for i in arr:
            if (self.isinputvalid(i)):
                arr2.append(int(i))
        if (len(arr2) != 0):
            self.back_btn.state(['disabled'])
            self.sort_btn.state(['disabled'])
            self.sortbubbleobj.array = arr2
            print(self.sortbubbleobj.array)
            self.inputs.clear()
            self.inputs.disable()
            self.area.delete('all')
            self.area.create_text(10, 10, anchor='nw', tags=(self.info_tag))
            self.set_info(self.info_tag, self.help, 'overwrite')
            self.sortbubbleobj.bubble_sort()
            self.back_btn.state(['!disabled'])
            self.sort_btn.state(['!disabled'])
            self.inputs.enable()

    def setup(self, root):
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

        # sort button
        sort_btn = ttk.Button(toolbar, text="Sort", command=self.sort, cursor='hand2')
        sort_btn.grid(column=0, row=2, sticky=(N, S, E, W), columnspan=2)

        for widget in toolbar.winfo_children():
            widget.grid_configure(pady=5, padx=3)

        # content Frame
        content_frame = ttk.Frame(main_frame, borderwidth=5, relief='ridge')
        content_frame.grid(column=0, row=0, sticky=(N, S, E, W), padx=5, pady=5)
        self.content_frame = content_frame
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self.back_btn = back_btn
        self.sort_btn = sort_btn

    def setupcanvas(self):
        content_frame = self.content_frame
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        pageobj = Page(content_frame)
        pageobj.page.grid(column=0, row=0, sticky=(N, S, E, W))
        self.area = pageobj.area
        self.area.create_text(10, 10, anchor='nw', tags=(self.info_tag))
        self.help = \
            'Bubble Sort \n\n Note :\n\n   White colored containers represent that the data is processed and it is ' \
            'in the correct position.\n   Green colored containers represent the data which is to be processed.\n' \
            '\n   When comparing adjacent elements edges gets highlighted.\n' \
            '        Red indicates that the adjacent elements are being swapped\n' \
            '        Blue indicates no swapping'
        self.set_info(self.info_tag, self.help, 'overwrite')

    def isinputvalid(self, val):
        return re.match('^[+-]?[0-9]{1,4}$', val) is not None

    def gohome(self):
        self.main_frame.destroy()
        Home(self.root, 'DsVis')

    def focus_box(self, box_tag):
        canvas = self.area
        canvas.update()
        k = 100000.0
        extra = 56.0
        coor = canvas.bbox(box_tag)
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

    def change_fillcolor(self, start_index, last_index, pass_num, fillcolor='white'):
        self.area.update()
        for i in range(start_index, last_index + 1):
            self.area.itemconfigure(Tag(i, pass_num).box(), fill=fillcolor)

    def dual_blink(self, index1, index2, pass_num, swap=False):
        canvas = self.area
        tag1 = Tag(index1, pass_num)
        tag2 = Tag(index2, pass_num)
        self.focus_box(tag1.box())
        self.focus_box(tag2.box())
        outline_color = '#046604'
        blink_color = '#0000fc'
        if (swap):
            blink_color = '#ff0000'
        canvas.itemconfigure(tag1.box(), outline=blink_color, width=5)
        canvas.itemconfigure(tag2.box(), outline=blink_color, width=5)
        canvas.update()
        time.sleep(self.anim_time)
        canvas.itemconfigure(tag1.box(), outline=blink_color, width=4)
        canvas.itemconfigure(tag2.box(), outline=blink_color, width=4)
        if (swap):
            val1 = canvas.itemcget(tag1.text(), 'text')
            val2 = canvas.itemcget(tag2.text(), 'text')
            canvas.itemconfigure(tag1.text(), text=val2)
            canvas.itemconfigure(tag2.text(), text=val1)
        canvas.update()
        time.sleep(self.anim_time)
        canvas.itemconfigure(tag1.box(), outline=blink_color, width=5)
        canvas.itemconfigure(tag2.box(), outline=blink_color, width=5)
        canvas.update()
        time.sleep(self.anim_time)
        canvas.itemconfigure(tag1.box(), outline=outline_color, width=1)
        canvas.itemconfigure(tag2.box(), outline=outline_color, width=1)

    def set_info(self, text_tag, val, mode='append'):
        if (mode == 'append'):
            val = self.area.itemcget(text_tag, 'text') + '\n' + val
        self.area.itemconfigure(text_tag, text=val)


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
            a.grid(column=0, row=i, sticky=(W, E))
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

    def enable(self):
        for i in self.input_entrys:
            i.state(['!disabled'])


class Tag:
    def __init__(self, index_num, pass_num):
        self.index_num = index_num
        self.pass_num = pass_num

    def box(self):
        return str(self.index_num) + '-b-' + str(self.pass_num)

    def text(self):
        return str(self.index_num) + '-t-' + str(self.pass_num)

    def key(self):
        return str(self.index_num) + '-k-' + str(self.pass_num)


class SectionTag:
    def __init__(self, pass_num):
        self.pass_num = pass_num

    def separator(self):
        return str(self.pass_num) + '-separator'

    def upper(self):
        return str(self.pass_num) + '-upper'

    def lower(self):
        return str(self.pass_num) + '-lower'


class Section:
    def __init__(self, canvasobj, pass_num, array, utext='', ltext=''):
        canvasobj.update()
        if (pass_num == 0):
            self.y = canvasobj.bbox(SectionTag(len(array)).lower())[3]
        elif (pass_num == len(array)):
            self.y = canvasobj.bbox('info')[3]
        else:
            self.y = canvasobj.bbox(SectionTag(pass_num - 1).lower())[3]
        self.canvasobj = canvasobj
        self.array = array
        self.pass_num = pass_num
        self.x = 50
        self.y = self.y + 30
        self.section_tag = SectionTag(pass_num)
        self.separator = canvasobj.create_line(0, self.y, 1000000, self.y, width=1, tags=(self.section_tag.separator()))
        self.focus_box(self.separator)
        self.upper = canvasobj.create_text(self.x, self.y + 30, text=utext, tags=(self.section_tag.upper()))
        canvasobj.update()
        self.focus_box(self.upper)
        self.draw()
        self.lower = canvasobj.create_text(self.x + 50, self.y + 160, text=ltext, tags=(self.section_tag.lower()))
        canvasobj.update()
        self.focus_box(self.lower)

    def draw(self):
        canvasobj = self.canvasobj
        x = 100
        y = self.y + 50
        w = h = 56.0
        fill_color = '#ccebcc'
        outline_color = text_color = '#046604'
        for i in range(len(self.array)):
            canvasobj.update()
            k = Tag(i, self.pass_num)
            box_tag = k.box()
            text_tag = k.text()
            key_tag = k.key()
            canvasobj.create_rectangle(x, y, x + w, y + w, outline=outline_color, fill=fill_color, tags=(box_tag),
                                       width=1)
            canvasobj.create_text(x + w / 2.0, y + h / 2.0, fill=text_color, text=convert(self.array[i]),
                                  tags=(text_tag))
            canvasobj.create_text(x + w / 2.0, y + h + h / 2.0, fill=text_color, text=i, tags=(key_tag))
            self.focus_box(box_tag)
            x += w + 2

    def focus_box(self, box_tag):
        canvas = self.canvasobj
        canvas.update()
        k = 100000.0
        extra = 56.0
        coor = canvas.bbox(box_tag)
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
