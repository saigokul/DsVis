from tkinter import *
from tkinter import ttk, font
"""from mainwindow.ds.arr import ARR
from mainwindow.ds.bs import BS
from mainwindow.ds.bst import BST
from mainwindow.ds.cqueue import CQUEUE
from mainwindow.ds.queue import QUEUE
from mainwindow.ds.sll import SLL
from mainwindow.ds.sortbubble import SORTBUBBLE
from mainwindow.ds.sortinsertion import SORTINSERTION
from mainwindow.ds.sortselection import SORTSELECTION
from mainwindow.ds.stack import STACK"""


class Home:
    def __init__(self, root, default_title):
        self.root = root
        self.default_title = default_title
        self.main_frame = None
        self.dstable = None
        self.index_items_labels = None
        self.setup(root)

    def setup(self, root):
        main_frame = ttk.Frame(root, padding=5)
        main_frame.grid(column=0, row=0, sticky=(N, S, E, W))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame = main_frame

        label_title_font = font.Font(family='Helvetica', name='appHighlightFont', size=40, weight='bold')
        label_title = ttk.Label(main_frame, text=self.default_title, font=label_title_font, borderwidth=5, relief="ridge",
                                anchor='center', padding=10)
        label_title.grid(column=0, row=0, sticky=(N, S, E, W), columnspan=2, padx=5, pady=5)
        index_items = [
            'Array',
            'Single Linked List',
            'Bubble Sort',
            'Insertion Sort',
            'Selection Sort',
            'Stack',
            'Queue',
            'Circular Queue',
            'Binary Search',
            'Binary Search Tree'
        ]
        ds = ['arr', 'sll', 'sortbubble', 'sortinsertion', 'sortselection', 'stack', 'queue', 'cqueue', 'bs', 'bst']
        self.dstable = dict(zip(index_items, ds))
        index_frame = ttk.Frame(main_frame, borderwidth=5, relief="ridge",
                                padding=10)
        index_frame.grid(column=0, row=1, sticky=(N, S, E, W), padx=5, pady=5)
        item_label_font = font.Font(name='font3', size=15)
        item_label_font_on_hover = font.Font(name='font4', size=15, underline=True)
        self.index_items_labels = {}
        for item in range(len(index_items)):
            item_label_bullet = ttk.Label(index_frame, text='\u2022 ', font=item_label_font)
            item_label_bullet.grid(column=0, row=item, sticky=W, pady=8)
            self.index_items_labels[item] = (
                ttk.Label(index_frame, text=index_items[item], font=item_label_font, cursor='hand2'))
            self.index_items_labels[item].grid(column=1, row=item, sticky=W, pady=8)
            self.index_items_labels[item].bind('<Enter>', lambda e: self.mousein(e.widget, item_label_font_on_hover))
            self.index_items_labels[item].bind('<Leave>', lambda e: self.mouseout(e.widget, item_label_font))
            self.index_items_labels[item].bind('<ButtonPress-1>', lambda e: self.launch(e.widget))

        """help_frame = ttk.Frame(main_frame, borderwidth=5, relief="ridge")
        help_frame.grid(column=1, row=1, sticky=(N, S, E, W), padx=5, pady=5)
        label_help_font = font.Font(family='Helvetica', name='font2', size=20, weight='bold')
        label_help = ttk.Label(help_frame, text='Help', font=label_help_font, anchor='center', padding=5)
        label_help.grid(column=0, row=0, sticky=(N, S, E, W), padx=5, pady=5)

        help_content_frame = ttk.Frame(help_frame)
        help_content_frame.grid(column=0, row=1, sticky=(N, S, E, W), padx=5, pady=5)"""

        main_frame.columnconfigure(0, weight=1)
        # main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        """help_frame.columnconfigure(0, weight=1)
        help_frame.rowconfigure(1, weight=2)"""

    def launch(self, label):
        label.configure(foreground='gray')
        ds_name = label['text']
        self.root.title(self.default_title + ' (' + ds_name + ')')
        self.main_frame.destroy()
        code = f'''from mainwindow.ds.{self.dstable[ds_name]} import {self.dstable[ds_name].upper()}
{self.dstable[ds_name].upper()}(self.root)'''
        exec(code)

    def mousein(self, label, fnt):
        label.configure(font=fnt)

    def mouseout(self, label, fnt):
        label.configure(font=fnt, foreground='black')
