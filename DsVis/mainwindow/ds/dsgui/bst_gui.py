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


def spaces(h):
    k = [2 ** i - 1 for i in range(h + 1)][::-1]
    return {'at_begin': k[1:], 'after_each': k[:len(k) - 1]}


class BSTgui:
    def __init__(self, root, tree):
        self.root = root
        self.tree = tree
        self.operations = []  # [ [ Pageobj, details_string, id of Nodeobj to be focused ], .... ]
        self.selected_operation = -1
        # self.require_canvas = None
        self.main_frame = None
        self.delete_var = None
        self.search_var = None
        self.counter_var = None
        self.insert_var = None
        self.details_box = None
        self.content_frame = None
        self.buttons = None
        self.anim_time = 0.25
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

        # Insert Entry
        self.insert_var = StringVar()
        insert_entry = ttk.Entry(toolbar, textvariable=self.insert_var, width=8, validate='key',
                                 validatecommand=valcomm)
        insert_entry.grid(column=0, row=1, sticky=E)
        # Insert Button
        insert_btn = ttk.Button(toolbar, text='Insert', cursor='hand2', width=6, command=self.insert)
        insert_btn.grid(column=1, row=1, sticky=W)
        # Delete Entry
        self.delete_var = StringVar()
        delete_entry = ttk.Entry(toolbar, textvariable=self.delete_var, width=8, validate='key',
                                 validatecommand=valcomm)
        delete_entry.grid(column=0, row=2, sticky=E)

        # Delete Button
        delete_btn = ttk.Button(toolbar, text='Delete', cursor='hand2', width=6, command=self.delete)
        delete_btn.grid(column=1, row=2, sticky=W)

        # search entry
        self.search_var = StringVar()
        search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=8, validate='key',
                                 validatecommand=valcomm)
        search_entry.grid(column=0, row=3, sticky=E)

        # search button
        search_btn = ttk.Button(toolbar, text='Search', cursor='hand2', width=6, command=self.search)
        search_btn.grid(column=1, row=3, sticky=W)

        # Traversal buttons
        traversal_frame = ttk.Labelframe(toolbar, text='Traversal', padding=5)
        traversal_frame.grid(column=0, row=4, columnspan=2, sticky=(W, E))

        # PreOrder Button
        preorder_btn = ttk.Button(traversal_frame, text='Preorder', cursor='hand2', command=self.preorder)
        preorder_btn.grid(column=0, row=0, pady=5)

        # Inorder Button
        inorder_btn = ttk.Button(traversal_frame, text='Inorder', cursor='hand2', command=self.inorder)
        inorder_btn.grid(column=0, row=1, pady=5)

        # Postorder Button
        postorder_btn = ttk.Button(traversal_frame, text='Postorder', cursor='hand2', command=self.postorder)
        postorder_btn.grid(column=0, row=2, pady=5)

        # status frame
        status_frame = ttk.Labelframe(toolbar, text='Status')
        status_frame.grid(column=0, row=5, columnspan=2, sticky=(W, E, N, S))

        # operation counter
        self.counter_var = StringVar()
        label_counter = ttk.Label(status_frame, textvariable=self.counter_var, anchor=(E))
        label_counter.grid(column=0, row=0, columnspan=2, padx=3, pady=5)
        # self.counter_var.set('Operation : 0/0')

        # previous operation button
        prev_btn = ttk.Button(status_frame, text='<<', cursor='hand2', command=self.backward)
        prev_btn.grid(column=0, row=1, sticky=E, padx=3, pady=5)

        # Next operation button
        next_btn = ttk.Button(status_frame, text='>>', cursor='hand2', command=self.forward)
        next_btn.grid(column=1, row=1, sticky=W, padx=3, pady=5)

        # details frame
        details_frame = ttk.Labelframe(status_frame, text='Details', padding=5)
        details_frame.grid(column=0, row=2, columnspan=2, padx=3, pady=5, sticky=(N, S, E, W))

        # details label
        details_label = Text(details_frame, width=20, bg='black', fg='#8ceb6c')
        details_label.grid(column=0, row=0)
        sb = ttk.Scrollbar(details_frame, orient=VERTICAL, command=details_label.yview)
        sb.grid(column=1, row=0, sticky=(N, S))
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(0, weight=1)
        details_label['yscrollcommand'] = sb.set
        self.details_box = details_label

        for widget in toolbar.winfo_children():
            widget.grid_configure(pady=5, padx=3)

        # content Frame
        content_frame = ttk.Frame(main_frame, borderwidth=5, relief='ridge')
        content_frame.grid(column=0, row=0, sticky=(N, S, E, W), padx=5, pady=5)
        self.content_frame = content_frame
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        toolbar.rowconfigure(5, weight=1)
        status_frame.rowconfigure(2, weight=1)
        self.buttons = [back_btn, insert_btn, delete_btn, search_btn, prev_btn, next_btn, preorder_btn, inorder_btn,
                        postorder_btn]

    def switch(self):
        k = '!disabled' if(self.buttons[0].instate(['disabled']) ) else 'disabled'
        for btn in self.buttons:
            btn.state([k])
        return 1

    def setupcanvas(self):
        content_frame = self.content_frame
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)

        self.operations.append([Page(content_frame), 'Binary Search Tree', None])
        welcome = self.operations[0][0]
        welcome.page.grid(column=0, row=0, sticky=(N, S, E, W))
        welcome = welcome.area
        self.details_box.insert('end -1 chars', self.operations[0][1])
        welcome.create_oval(410, 40, 466, 96, fill='#ccebcc', outline='#046604', width=2)
        welcome.create_text(410 + 28, 40 + 28, text='BST', fill='#046604')
        self.counter_var.set('Operation : 1/' + str(len(self.operations)))
        self.selected_operation += 1

    def gohome(self):
        self.main_frame.destroy()
        Home(self.root, 'DsVis')

    def check_input(self, val):
        return re.match('^([+-]?[0-9]{1,4})?$', val) is not None or re.match('^([+-]?)?$',
                                                                             val) is not None

    def isinputvalid(self, val):
        return re.match('^[+-]?[0-9]{1,4}$', val) is not None

    def forward(self):
        if (not self.selected_operation == len(self.operations) - 1):
            self.operations[self.selected_operation][0].page.grid_remove()
            self.selected_operation += 1
            self.change_content()

    def backward(self):
        if (not self.selected_operation == 0):
            self.operations[self.selected_operation][0].page.grid_remove()
            self.selected_operation -= 1
            self.change_content()

    def change_content(self):
        k = str(self.selected_operation + 1)
        self.counter_var.set('Operation : ' + k + '/' + str(len(self.operations)))
        self.details_box.delete('1.0', 'end')
        self.details_box.insert('end -1 chars', self.operations[self.selected_operation][1])
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        self.operations[self.selected_operation][0].page.grid(column=0, row=0, sticky=(N, S, E, W))
        focus = self.operations[self.selected_operation][2]
        if (focus):
            self.focus_item(self.operations[self.selected_operation][0].area, focus)

    def insert(self):
        self.switch()
        self.selected_operation = len(self.operations) - 2
        self.forward()
        val = self.insert_var.get()
        if self.isinputvalid(val):
            self.insert_var.set('')
            print('bst insert entry : ', int(val))
            # self.require_canvas = self.operations[-1][0].area
            self.tree.insert(int(val))
            val = convert(int(val))
            k = 'Inserted ' + val
            self.operations.append([Page(self.content_frame), k, None])
            f = self.attach_to_area(self.tree.levelorder(), self.operations[-1][0], int(val))
            self.highlight(self.operations[-1][0].area, f.id)
            self.operations[-1][2] = f.id
            self.selected_operation = len(self.operations) - 2
            self.forward()
        self.switch()

    def delete(self):
        self.switch()
        self.selected_operation = len(self.operations) - 2
        self.forward()
        val = self.delete_var.get()
        if self.isinputvalid(val):
            self.delete_var.set('')
            print('bst delete entry : ', int(val))
            # self.require_canvas = self.operations[-1][0].area
            check = self.tree.check(int(val))
            self.tree.delete(int(val))
            if (check):
                k = 'Deleted ' + convert(int(val))
            else:
                k = convert(int(val)) + ' can\'t be \ndeleted because it \ndoesn\'t exists'
            self.operations.append([Page(self.content_frame), k, self.tree.root.id])
            self.attach_to_area(self.tree.levelorder(), self.operations[-1][0])
            self.selected_operation = len(self.operations) - 2
            time.sleep(1.0)
            self.forward()
        self.switch()

    def search(self):
        self.switch()
        val = self.search_var.get()
        if self.isinputvalid((val)):
            self.search_var.set('')
            print('bst search entry : ', int(val))
            k = 'searching ' + convert(int(val)) + ' ...'
            self.operations.append([Page(self.content_frame), k, None])
            self.attach_to_area(self.tree.levelorder(), self.operations[-1][0])
            self.selected_operation = len(self.operations) - 2
            self.forward()
            # self.require_canvas = self.operations[-1][0].area
            j = self.tree.search(int(val))
            if (j):
                k = '\nFound'
                self.operations[-1][2] = j.id
                self.highlight(self.operations[-1][0].area, j.id)
            else:
                k = '\nNot Found'
                self.operations[-1][2] = self.tree.root.id
            self.operations[-1][1] += k
            self.details_box.insert('end -1 chars', k)
        self.switch()

    def preorder(self):
        self.switch()
        self.operations.append([Page(self.content_frame), 'Preorder...', None])
        self.attach_to_area(self.tree.levelorder(), self.operations[-1][0])
        self.selected_operation = len(self.operations) - 2
        self.forward()
        # self.require_canvas = self.operations[-1][0].area
        self.tree.preorder()
        self.switch()

    def postorder(self):
        self.switch()
        self.operations.append([Page(self.content_frame), 'Postorder...', None])
        self.attach_to_area(self.tree.levelorder(), self.operations[-1][0])
        self.selected_operation = len(self.operations) - 2
        self.forward()
        # self.require_canvas = self.operations[-1][0].area
        self.tree.postorder()
        self.switch()

    def inorder(self):
        self.switch()
        self.operations.append([Page(self.content_frame), 'Inorder...', None])
        self.attach_to_area(self.tree.levelorder(), self.operations[-1][0])
        self.selected_operation = len(self.operations) - 2
        self.forward()
        # self.require_canvas = self.operations[-1][0].area
        self.tree.inorder()
        self.switch()

    def attach_to_area(self, skeleton, pageobj, focus=None):
        # focus type is Node
        retn = None
        area = pageobj.area
        y = 50.0
        w = h = 56.0
        s = 14.0
        m = h / 2.0
        fill_color = '#ccebcc'
        outline_color = text_color = '#046604'
        gaps = spaces(len(skeleton))
        pageobj.memory = [[] for i in range(len(skeleton)) if i or not i]
        for lev, level in enumerate(skeleton):
            x = 50.0 + (w + s) * gaps['at_begin'][lev]
            for ele, element in enumerate(level):
                if (not element == 'empty'):
                    oval_id = area.create_oval(x, y, x + w, y + h, fill=fill_color, outline=outline_color, width=2)
                    element.id = oval_id
                    pageobj.memory[lev].append(area.coords(oval_id))
                    text = convert(element.data)
                    area.create_text(x + w / 2.0, y + h / 2.0, fill=text_color, text=text)
                    if (focus is not None and focus == element.data):
                        retn = element
                    if (not lev == 0):
                        cx, cy = pageobj.memory[lev - 1][ele // 2][0:2]
                        cy += m
                        if (ele % 2 != 0):
                            cx += w
                        area.create_line(cx, cy, x + m, y, arrow='last', fill=outline_color, width=2)
                else:
                    pageobj.memory[lev].append([])
                x += w + s
                x += (w + s) * gaps['after_each'][lev]
            y += h
        return retn

    def blink_highlight(self, canvas, oval_id):
        self.focus_item(canvas, oval_id)
        # outline_color = '#046604'
        outline_color = canvas.itemcget(oval_id, 'outline')
        outline_width = canvas.itemcget(oval_id, 'width')
        blink_color = '#ff0000'
        canvas.itemconfigure(oval_id, outline=blink_color, width=5)
        canvas.update()
        time.sleep(self.anim_time)
        canvas.itemconfigure(oval_id, outline=blink_color, width=4)
        canvas.update()
        time.sleep(self.anim_time)
        canvas.itemconfigure(oval_id, outline=blink_color, width=5)
        canvas.update()
        time.sleep(self.anim_time)
        canvas.itemconfigure(oval_id, outline=outline_color, width=outline_width)

    def highlight(self, canvas, oval_id):
        outline_color = '#0000fc'
        canvas.itemconfigure(oval_id, outline=outline_color, width=5)
        canvas.update()

    def focus_item(self, canvas, oval_id):
        canvas.update()
        k = 100000.0
        extra = 14.0
        coor = canvas.coords(oval_id)
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
