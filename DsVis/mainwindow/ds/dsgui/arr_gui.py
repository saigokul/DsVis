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


class ARRgui:
    def __init__(self, root, arr):
        self.arr = arr
        self.root = root
        self.main_frame = None
        self.content_frame = None
        self.area = None
        self.size_var = StringVar()
        self.search_var = StringVar()
        self.get_var = StringVar()
        self.append_var = StringVar()
        self.insert_var = StringVar()
        self.at_ivar = StringVar()
        self.before_ivar = StringVar()
        self.after_ivar = StringVar()
        self.at_dvar = StringVar()
        self.before_dvar = StringVar()
        self.after_dvar = StringVar()
        self.details_box = None
        self.buttons = None
        self.size = 0
        self.size_btn = None
        self.size_entry = None
        self.anim_time = 0.25
        self.setup(root)
        self.setupcanvas()

    def setup(self, root):
        valcomm = (root.register(self.check_input), '%P')
        valcomm2 = (root.register(self.check_input2), '%P')

        main_frame = ttk.Frame(root, padding=5)
        main_frame.grid(column=0, row=0, sticky=(N, S, E, W))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame = main_frame

        toolbar = ttk.Frame(main_frame, padding=5, borderwidth=5, relief='ridge')
        toolbar.grid(column=1, row=0, sticky=(N, S, E, W), padx=5, pady=5)
        back_btn = ttk.Button(toolbar, text="Home", command=self.gohome, cursor='hand2')
        back_btn.grid(column=0, row=0, columnspan=2, sticky=(N, S, E, W))

        # size entry
        size_entry = ttk.Entry(toolbar, textvariable=self.size_var, width=8, validate='key',
                               validatecommand=valcomm2)
        size_entry.grid(column=0, row=1, sticky=E)
        self.size_entry = size_entry

        # set size Button
        set_size_btn = ttk.Button(toolbar, text='Set Size', cursor='hand2', width=8, command=self.set_size)
        set_size_btn.grid(column=1, row=1, sticky=W)
        self.size_btn = set_size_btn

        # search entry
        search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=8, validate='key',
                                 validatecommand=valcomm)
        search_entry.grid(column=0, row=2, sticky=E)

        # search button
        search_btn = ttk.Button(toolbar, text='Search', cursor='hand2', width=8, command=self.search_data)
        search_btn.grid(column=1, row=2, sticky=W)

        # get entry
        get_entry = ttk.Entry(toolbar, textvariable=self.get_var, width=8, validate='key',
                              validatecommand=valcomm2)
        get_entry.grid(column=0, row=3, sticky=E)

        # get Button
        get_btn = ttk.Button(toolbar, text='Get', cursor='hand2', width=8, command=self.get_data)
        get_btn.grid(column=1, row=3, sticky=W)

        # append entry
        append_entry = ttk.Entry(toolbar, textvariable=self.append_var, width=8, validate='key',
                                 validatecommand=valcomm)
        append_entry.grid(column=0, row=4, sticky=E)

        # append Button
        append_btn = ttk.Button(toolbar, text='Append', cursor='hand2', width=8, command=self.append_data)
        append_btn.grid(column=1, row=4, sticky=W)

        # pop button
        pop_btn = ttk.Button(toolbar, text="Pop", command=self.pop_data, cursor='hand2')
        pop_btn.grid(column=0, row=5, columnspan=2, sticky=(N, S, E, W))

        # insertion and deletion Box
        i_and_d_box = ttk.Notebook(toolbar)
        i_and_d_box.grid(column=0, row=6, columnspan=2, sticky=(W, E))

        # insertion Frame
        insertion_frame = ttk.Frame(i_and_d_box, padding=5)
        i_and_d_box.add(insertion_frame, text='Insertion')

        # insert data label
        insert_data_label = ttk.Label(insertion_frame, text='Enter Data')
        insert_data_label.grid(column=0, row=0, pady=5, padx=3, sticky=W)

        # insert entry
        insert_entry = ttk.Entry(insertion_frame, textvariable=self.insert_var, width=8, validate='key',
                                 validatecommand=valcomm)
        insert_entry.grid(column=1, row=0, sticky=E, pady=5, padx=3)

        '''# at_ientry
        at_ientry = ttk.Entry(insertion_frame, textvariable=self.at_ivar, width=8, validate='key',
                              validatecommand=valcomm2)
        at_ientry.grid(column=0, row=1, sticky=W, pady=5, padx=3)

        # at_ibtn
        at_ibtn = ttk.Button(insertion_frame, text='At index', cursor='hand2', width=8, command=self.insert_at)
        at_ibtn.grid(column=1, row=1, sticky=E, pady=5, padx=3)
        '''

        # before_ientry
        before_ientry = ttk.Entry(insertion_frame, textvariable=self.before_ivar, width=8, validate='key',
                                  validatecommand=valcomm)
        before_ientry.grid(column=0, row=2, sticky=W, pady=5, padx=3)

        # before_ibtn
        before_ibtn = ttk.Button(insertion_frame, text='Before', cursor='hand2', width=8, command=self.insert_before)
        before_ibtn.grid(column=1, row=2, sticky=E, pady=5, padx=3)

        # after_ientry
        after_ientry = ttk.Entry(insertion_frame, textvariable=self.after_ivar, width=8, validate='key',
                                 validatecommand=valcomm)
        after_ientry.grid(column=0, row=3, sticky=W, pady=5, padx=3)

        # after_ibtn
        after_ibtn = ttk.Button(insertion_frame, text='After', cursor='hand2', width=8, command=self.insert_after)
        after_ibtn.grid(column=1, row=3, sticky=E, pady=5, padx=3)

        # deletion Frame
        deletion_frame = ttk.Frame(i_and_d_box, padding=5)
        i_and_d_box.add(deletion_frame, text='Deletion')

        # at_dentry
        at_dentry = ttk.Entry(deletion_frame, textvariable=self.at_dvar, width=8, validate='key',
                              validatecommand=valcomm2)
        at_dentry.grid(column=0, row=1, sticky=W, pady=5, padx=3)

        # at_dbtn
        at_dbtn = ttk.Button(deletion_frame, text='At index', cursor='hand2', width=8, command=self.del_at)
        at_dbtn.grid(column=1, row=1, sticky=E, pady=5, padx=3)

        # before_dentry
        before_dentry = ttk.Entry(deletion_frame, textvariable=self.before_dvar, width=8, validate='key',
                                  validatecommand=valcomm)
        before_dentry.grid(column=0, row=2, sticky=W, pady=5, padx=3)

        # before_dbtn
        before_dbtn = ttk.Button(deletion_frame, text='Before', cursor='hand2', width=8, command=self.del_before)
        before_dbtn.grid(column=1, row=2, sticky=E, pady=5, padx=3)

        # after_dentry
        after_dentry = ttk.Entry(deletion_frame, textvariable=self.after_dvar, width=8, validate='key',
                                 validatecommand=valcomm)
        after_dentry.grid(column=0, row=3, sticky=W, pady=5, padx=3)

        # after_dbtn
        after_dbtn = ttk.Button(deletion_frame, text='After', cursor='hand2', width=8, command=self.del_after)
        after_dbtn.grid(column=1, row=3, sticky=E, pady=5, padx=3)

        # details frame
        details_frame = ttk.Labelframe(toolbar, text='Details', padding=5)
        details_frame.grid(column=0, row=7, columnspan=2, padx=3, pady=5, sticky=(N, S, E, W))

        # details label
        details_label = Text(details_frame, width=20, bg='black', fg='#8ceb6c')
        details_label.grid(column=0, row=0)
        sb = ttk.Scrollbar(details_frame, orient=VERTICAL, command=details_label.yview)
        sb.grid(column=1, row=0, sticky=(N, S))
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(0, weight=1)
        details_label['yscrollcommand'] = sb.set
        self.details_box = details_label
        toolbar.rowconfigure(7, weight=1)

        for widget in toolbar.winfo_children():
            widget.grid_configure(pady=5, padx=3)

        # content Frame
        content_frame = ttk.Frame(main_frame, borderwidth=5, relief='ridge')
        content_frame.grid(column=0, row=0, sticky=(N, S, E, W), padx=5, pady=5)
        self.content_frame = content_frame
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self.buttons = [search_btn, get_btn, append_btn, pop_btn,
                        # at_ibtn,
                        at_dbtn, before_ibtn, before_dbtn,
                        after_ibtn, after_dbtn, back_btn]

        self.switch()
        back_btn.state(['!disabled'])
        self.details_box.delete('1.0', 'end')
        self.details_box.insert('end -1 chars', 'Array \n\nPlease configure\narray size')

    def set_size(self):
        val = self.size_var.get()
        if (val != ''):
            self.size = int(val)
            self.size_btn.state(['disabled'])
            print('Array Size : ', val)
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Array Size : ' + val)
            self.size_var.set('')
            self.size_entry.state(['disabled'])
            self.draw(self.area)
            self.arr.array = ['-'] * self.size
            self.arr.length = self.size
            print('length : ', self.arr.length, '\nArray:', self.arr.array)
            self.switch()

    def draw(self, canvasobj):
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

    def search_data(self):
        val = self.search_var.get()
        if (self.isinputvalid(val)):
            self.switch()
            print('Search data entry : ', val)
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Searching\nfor : ' + convert(int(val)) + ' ...')
            self.search_var.set('')
            k = self.arr.array_search(int(val))
            if (k != -1):
                k = '\nFound at ' + str(k)
            else:
                k = '\nNot Found'
            self.details_box.insert('end -1 chars', k)
            print('length : ', self.arr.length, '\nArray:', self.arr.array)
            self.switch()

    def get_data(self):
        val = self.get_var.get()
        if (val != ''):
            self.switch()
            print('Get data entry : ', val)
            self.get_var.set('')
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Finding value \nat index : ' + val + ' ..')
            k = self.arr.array_getat(int(val))
            self.details_box.insert('end -1 chars', k)
            print('length : ', self.arr.length, '\nArray:', self.arr.array)
            self.switch()

    def append_data(self):
        val = self.append_var.get()
        if (self.isinputvalid(val)):
            self.switch()
            blink_color = '#0000fc'
            print('Append data entry : ', val)
            self.append_var.set('')
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Appending : ' + convert(int(val)) + ' ..')
            k = self.arr.array_append(int(val))
            if (k != -1):
                self.blink_highlight(str(k) + '-b', blink_color)
                self.set_data(str(k) + '-t', int(val))
                self.details_box.insert('end -1 chars', '\nDone!')
            else:
                self.details_box.insert('end -1 chars', '\nNo space to Append!')
            print('length : ', self.arr.length, '\nArray:', self.arr.array)
            self.switch()

    def pop_data(self):
        self.switch()
        print('Clicked on pop')
        k = self.arr.array_pop()
        self.details_box.delete('1.0', 'end')
        self.details_box.insert('end -1 chars', k)
        print('length : ', self.arr.length, '\nArray:', self.arr.array)
        self.switch()

    # def insert_at(self):
    #    pass

    def insert_before(self):
        val = self.insert_var.get()
        bval = self.before_ivar.get()
        if (self.isinputvalid(val) and self.isinputvalid(bval)):
            self.switch()
            print('insert data entry : ' + val, ' before data entry : ' + bval)
            self.insert_var.set('')
            self.before_ivar.set('')
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Inserting ' + val + '\nbefore ' + bval + ' ...')
            k = self.arr.insert_before(int(val), int(bval))
            self.details_box.insert('end -1 chars', k)
            print('length : ', self.arr.length, '\nArray:', self.arr.array)
            self.switch()

    def insert_after(self):
        val = self.insert_var.get()
        aval = self.after_ivar.get()
        if (self.isinputvalid(val) and self.isinputvalid(aval)):
            self.switch()
            print('insert data entry : ' + val, ' After data entry : ' + aval)
            self.insert_var.set('')
            self.after_ivar.set('')
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Inserting ' + val + '\nafter ' + aval + ' ...')
            k = self.arr.insert_after(int(val), int(aval))
            self.details_box.insert('end -1 chars', k)
            print('length : ', self.arr.length, '\nArray:', self.arr.array)
            self.switch()

    def del_at(self):
        val = self.at_dvar.get()
        if (val != ''):
            self.switch()
            print('Delete At index entry : ' + val)
            self.at_dvar.set('')
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Deleting data \nat ' + val + ' ...')
            k = self.arr.del_at(int(val))
            self.details_box.insert('end -1 chars', k)
            print('length : ', self.arr.length, '\nArray:', self.arr.array)
            self.switch()

    def del_before(self):
        val = self.before_dvar.get()
        if (self.isinputvalid(val)):
            self.switch()
            print('Delete before entry : '+val)
            self.before_dvar.set('')
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Deleting data \nbefore ' + val + ' ...')
            k = self.arr.del_before(int(val))
            self.details_box.insert('end -1 chars', k)
            print('length : ', self.arr.length, '\nArray:', self.arr.array)
            self.switch()

    def del_after(self):
        val = self.after_dvar.get()
        if (self.isinputvalid(val)):
            self.switch()
            print('Delete after entry : ' + val)
            self.after_dvar.set('')
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Deleting data \nafter ' + val + ' ...')
            k = self.arr.del_after(int(val))
            self.details_box.insert('end -1 chars', k)
            print('length : ', self.arr.length, '\nArray:', self.arr.array)
            self.switch()

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

    def setupcanvas(self):
        content_frame = self.content_frame
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        pageobj = Page(content_frame)
        pageobj.page.grid(column=0, row=0, sticky=(N, S, E, W))
        self.area = pageobj.area

    def check_input(self, val):
        return re.match('^([+-]?[0-9]{1,4})?$', val) is not None or re.match('^([+-]?)?$',
                                                                             val) is not None

    def check_input2(self, val):
        return re.match('^([0-9]{1,2})?$', val) is not None

    def isinputvalid(self, val):
        return re.match('^[+-]?[0-9]{1,4}$', val) is not None

    def switch(self):
        k = '!disabled' if (self.buttons[0].instate(['disabled'])) else 'disabled'
        for btn in self.buttons:
            btn.state([k])
        return 1

    def shift(self, hyphen_index, val_index):
        canvas = self.area
        hyphen_box_tag = str(hyphen_index) + '-b'
        val_box_tag = str(val_index) + '-b'
        hyphen_text_tag = str(hyphen_index) + '-t'
        val_text_tag = str(val_index) + '-t'
        self.focus_box(hyphen_box_tag)
        self.focus_box(val_box_tag)
        outline_color = '#046604'
        blink_color = '#ff0000'
        canvas.itemconfigure(hyphen_box_tag, outline=blink_color, width=5)
        canvas.itemconfigure(val_box_tag, outline=blink_color, width=5)
        canvas.update()
        time.sleep(self.anim_time)
        canvas.itemconfigure(hyphen_box_tag, outline=blink_color, width=4)
        canvas.itemconfigure(val_box_tag, outline=blink_color, width=4)
        k = canvas.itemcget(val_text_tag, 'text')
        canvas.itemconfigure(hyphen_text_tag, text=k)
        canvas.itemconfigure(val_text_tag, text='-')
        canvas.update()
        time.sleep(self.anim_time)
        canvas.itemconfigure(hyphen_box_tag, outline=blink_color, width=5)
        canvas.itemconfigure(val_box_tag, outline=blink_color, width=5)
        canvas.update()
        time.sleep(self.anim_time)
        canvas.itemconfigure(hyphen_box_tag, outline=outline_color, width=1)
        canvas.itemconfigure(val_box_tag, outline=outline_color, width=1)


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
