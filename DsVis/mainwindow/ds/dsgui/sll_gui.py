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


class SLLgui:
    def __init__(self, root, sll):
        self.sll = sll
        self.root = root
        self.main_frame = None
        self.content_frame = None
        self.area = None

        self.search_var = StringVar()

        self.insert_var = StringVar()
        self.before_ivar = StringVar()
        self.after_ivar = StringVar()

        self.at_dvar = StringVar()
        self.before_dvar = StringVar()
        self.after_dvar = StringVar()

        self.details_box = None
        self.buttons = None

        self.anim_time = 0.25
        self.blue_color = '#0324ff'
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

        # search entry
        search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=8, validate='key',
                                 validatecommand=valcomm)
        search_entry.grid(column=0, row=2, sticky=E)

        # search button
        search_btn = ttk.Button(toolbar, text='Search', cursor='hand2', width=8, command=self.search)
        search_btn.grid(column=1, row=2, sticky=W)

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

        # beg_ibtn
        beg_ibtn = ttk.Button(insertion_frame, text='At Beginning', cursor='hand2', command=self.insert_beg)
        beg_ibtn.grid(column=0, row=4, sticky=(E, W), pady=5, padx=3, columnspan=2)

        # end_ibtn
        end_ibtn = ttk.Button(insertion_frame, text='At End', cursor='hand2', command=self.insert_end)
        end_ibtn.grid(column=0, row=5, sticky=(E, W), pady=5, padx=3, columnspan=2)

        # deletion Frame
        deletion_frame = ttk.Frame(i_and_d_box, padding=5)
        i_and_d_box.add(deletion_frame, text='Deletion')

        # at_dentry
        at_dentry = ttk.Entry(deletion_frame, textvariable=self.at_dvar, width=8, validate='key',
                              validatecommand=valcomm)
        at_dentry.grid(column=0, row=1, sticky=W, pady=5, padx=3)

        # at_dbtn
        at_dbtn = ttk.Button(deletion_frame, text='Delete this', cursor='hand2', width=12, command=self.del_ele)
        at_dbtn.grid(column=1, row=1, sticky=E, pady=5, padx=3)

        # before_dentry
        before_dentry = ttk.Entry(deletion_frame, textvariable=self.before_dvar, width=8, validate='key',
                                  validatecommand=valcomm)
        before_dentry.grid(column=0, row=2, sticky=W, pady=5, padx=3)

        # before_dbtn
        before_dbtn = ttk.Button(deletion_frame, text='Before', cursor='hand2', width=12, command=self.del_before)
        before_dbtn.grid(column=1, row=2, sticky=E, pady=5, padx=3)

        # after_dentry
        after_dentry = ttk.Entry(deletion_frame, textvariable=self.after_dvar, width=8, validate='key',
                                 validatecommand=valcomm)
        after_dentry.grid(column=0, row=3, sticky=W, pady=5, padx=3)

        # after_dbtn
        after_dbtn = ttk.Button(deletion_frame, text='After', cursor='hand2', width=12, command=self.del_after)
        after_dbtn.grid(column=1, row=3, sticky=E, pady=5, padx=3)

        # beg_dbtn
        beg_dbtn = ttk.Button(deletion_frame, text='At Beginning', cursor='hand2', command=self.del_beg)
        beg_dbtn.grid(column=0, row=4, sticky=(E, W), pady=5, padx=3, columnspan=2)

        # end_dbtn
        end_dbtn = ttk.Button(deletion_frame, text='At End', cursor='hand2', command=self.del_end)
        end_dbtn.grid(column=0, row=5, sticky=(E, W), pady=5, padx=3, columnspan=2)

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

        self.buttons = [search_btn,
                        at_dbtn, before_ibtn, before_dbtn,
                        beg_ibtn, beg_dbtn, end_ibtn, end_dbtn,
                        after_ibtn, after_dbtn, back_btn]

        self.details_box.delete('1.0', 'end')
        self.details_box.insert('end -1 chars', 'Single Linked List')

    def setupcanvas(self):
        content_frame = self.content_frame
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        pageobj = Page(content_frame)
        pageobj.page.grid(column=0, row=0, sticky=(N, S, E, W))
        self.area = pageobj.area
        x1 = 200
        x2 = x1 + 200
        y1 = 100
        y2 = y1 + 30
        y3 = y2 + 30
        fill_color = '#ccebcc'
        outline_color = text_color = '#046604'
        self.area.create_rectangle(x1, y1, x2, y2, outline=outline_color, fill=fill_color)
        self.area.create_text((x1 + x2) / 2, (y1 + y2) / 2, text='HEAD', fill=text_color)
        self.area.create_rectangle(x1, y2, x2, y3, outline=outline_color, tags=('headidbox', 'headidboxnextidbox'))
        self.area.create_text((x1 + x2) / 2, (y3 + y2) / 2, text='NULL', fill=text_color, tags=('headid'))

    def draw(self, y0, nid, data, nextid):
        if not nextid:
            nextid = 'NULL'
        else:
            nextid = id(nextid)
        canvas = self.area
        x1 = 200
        x3 = x1 + 200
        x2 = x1 + 55
        y1 = y0 + 50
        y2 = y1 + 30
        y3 = y2 + 30
        fill_color = '#ccebcc'
        outline_color = text_color = '#046604'
        canvas.create_line(x2 + 45, y0, x2 + 45, y1, fill=outline_color, arrow='last',
                           tags=(str(nid), str(nid) + 'arrow'))
        canvas.create_rectangle(x1, y1, x3, y2, outline=outline_color, fill=fill_color,
                                tags=(str(nid), str(nid) + 'nidbox'))
        canvas.create_text((x1 + x3) / 2, (y1 + y2) / 2, text=str(nid), fill=text_color,
                           tags=(str(nid), str(nid) + 'nid'))
        canvas.create_rectangle(x1, y2, x2, y3, outline=outline_color, tags=(str(nid), str(nid) + 'databox'))
        canvas.create_text((x1 + x2) / 2, (y3 + y2) / 2, text=convert(data), fill=text_color,
                           tags=(str(nid), str(nid) + 'data'))
        canvas.create_rectangle(x2, y2, x3, y3, outline=outline_color, tags=(str(nid), str(nid) + 'nextidbox'))
        canvas.create_text((x2 + x3) / 2, (y3 + y2) / 2, text=str(nextid), fill=text_color,
                           tags=(str(nid), str(nid) + 'nextid'))
        self.focus_item(str(nid) + 'arrow')
        self.focus_item(str(nid) + 'nextidbox')

    def node_move(self, idstr, xamount, yamount):
        canvas = self.area
        canvas.move(idstr + 'arrow', xamount, yamount)
        canvas.move(idstr + 'nidbox', xamount, yamount)
        canvas.move(idstr + 'nid', xamount, yamount)
        canvas.move(idstr + 'databox', xamount, yamount)
        canvas.move(idstr + 'data', xamount, yamount)
        canvas.move(idstr + 'nextidbox', xamount, yamount)
        canvas.move(idstr + 'nextid', xamount, yamount)

    def node_delete(self, idstr):
        canvas = self.area
        canvas.delete(idstr + 'arrow')
        canvas.delete(idstr + 'nidbox')
        canvas.delete(idstr + 'nid')
        canvas.delete(idstr + 'databox')
        canvas.delete(idstr + 'data')
        canvas.delete(idstr + 'nextidbox')
        canvas.delete(idstr + 'nextid')

    def blink_node(self, stringid, color='#046604'):
        canvas = self.area
        canvas.update()
        self.focus_item(stringid + 'nidbox')
        self.focus_item(stringid + 'nextidbox')
        x1, y1 = canvas.bbox(stringid + 'nidbox')[0:2]
        x2, y2 = canvas.bbox(stringid + 'nextidbox')[2:]
        k = canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=3)
        canvas.tag_raise(k)
        time.sleep(self.anim_time)
        canvas.update()
        canvas.itemconfigure(k, width=2)
        time.sleep(self.anim_time)
        canvas.update()
        canvas.itemconfigure(k, width=3)
        time.sleep(self.anim_time)
        canvas.update()
        canvas.delete(k)

    def blink_next_field(self, stringid):
        tag = stringid + 'nextidbox'
        temp_color = '#f05d5d'
        fill_color = 'white'
        canvas = self.area
        canvas.update()
        self.focus_item(tag)
        canvas.itemconfigure(tag, fill=temp_color)
        time.sleep(self.anim_time)
        canvas.update()
        canvas.itemconfigure(tag, fill=fill_color)
        time.sleep(self.anim_time)
        canvas.update()
        canvas.itemconfigure(tag, fill=temp_color)
        time.sleep(self.anim_time)
        canvas.update()
        canvas.itemconfigure(tag, fill=fill_color)
        canvas.update()

    def focus_item(self, tag):
        canvas = self.area
        canvas.update()
        k = 100000.0
        extra = 56.0
        coor = canvas.bbox(tag)
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

    def gohome(self):
        self.main_frame.destroy()
        Home(self.root, 'DsVis')

    def check_input(self, val):
        return re.match('^([+-]?[0-9]{1,4})?$', val) is not None or re.match('^([+-]?)?$',
                                                                             val) is not None

    def isinputvalid(self, val):
        return re.match('^[+-]?[0-9]{1,4}$', val) is not None

    def switch(self):
        k = '!disabled' if (self.buttons[0].instate(['disabled'])) else 'disabled'
        for btn in self.buttons:
            btn.state([k])

    def search(self):
        val = self.search_var.get()
        if (self.isinputvalid(val)):
            self.switch()
            self.area.update()
            print('Search Entry : ', val)
            self.search_var.set('')
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Searching ' + convert(int(val)) + ' ...')
            # call
            self.sll.search(int(val))
            self.switch()

    def insert_before(self):
        val = self.insert_var.get()
        bval = self.before_ivar.get()
        if (self.isinputvalid(val) and self.isinputvalid(bval)):
            self.switch()
            print('Insert Entry : ', val, ' Before : ', bval)
            self.insert_var.set('')
            self.before_ivar.set('')
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Inserting ' + convert(int(val)) +
                                    '\nbefore ' + convert(int(bval)) + ' ...')
            # call
            self.sll.insert_before(int(val), int(bval))
            self.switch()

    def insert_after(self):
        val = self.insert_var.get()
        aval = self.after_ivar.get()
        if (self.isinputvalid(val) and self.isinputvalid(aval)):
            self.switch()
            print('Insert Entry : ', val, ' After : ', aval)
            self.insert_var.set('')
            self.after_ivar.set('')
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Inserting ' + convert(int(val)) +
                                    '\nafter ' + convert(int(aval)) + ' ...')
            # call
            self.sll.insert_after(int(val), int(aval))
            self.switch()

    def insert_beg(self):
        val = self.insert_var.get()
        if (self.isinputvalid(val)):
            self.switch()
            print('Insert Entry at begin : ', val)
            self.insert_var.set('')
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Inserting ' + convert(int(val)) + '\nat beginning  ...')
            # call
            self.sll.insert_at_beg(int(val))
            self.switch()

    def insert_end(self):
        val = self.insert_var.get()
        if (self.isinputvalid(val)):
            self.switch()
            print('Insert Entry at end : ', val)
            self.insert_var.set('')
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Inserting ' + convert(int(val)) + '\nat end  ...')
            # call
            self.sll.insert_at_end(int(val))
            self.switch()

    def del_ele(self):
        val = self.at_dvar.get()
        if (self.isinputvalid(val)):
            self.switch()
            print('Delete an element entry : ', val)
            self.at_dvar.set('')
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Deleting ' + convert(int(val)) + ' ...')
            # call
            self.sll.del_data(int(val))
            self.switch()

    def del_before(self):
        val = self.before_dvar.get()
        if (self.isinputvalid(val)):
            self.switch()
            print('Delete an element before entry : ', val)
            self.before_dvar.set('')
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Deleting element \nbefore ' + convert(int(val)) + ' ...')
            # call
            self.sll.del_before(int(val))
            self.switch()

    def del_after(self):
        val = self.after_dvar.get()
        if (self.isinputvalid(val)):
            self.switch()
            print('Delete an element after entry : ', val)
            self.after_dvar.set('')
            self.details_box.delete('1.0', 'end')
            self.details_box.insert('end -1 chars', 'Deleting element \nafter ' + convert(int(val)) + ' ...')
            # call
            self.sll.del_after(int(val))
            self.switch()

    def del_beg(self):
        self.switch()
        print('clicked del begin btn')
        self.details_box.delete('1.0', 'end')
        self.details_box.insert('end -1 chars', 'Deleting element \nat the beginning ...')
        # call
        self.sll.del_at_beg()
        self.switch()

    def del_end(self):
        self.switch()
        print('clicked del end btn')
        self.details_box.delete('1.0', 'end')
        self.details_box.insert('end -1 chars', 'Deleting element \nat the End ...')
        # call
        self.sll.del_at_end()
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
