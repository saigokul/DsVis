from tkinter import *
from mainwindow.homescreen import Home
# import os


class MW:
    def __init__(self):
        self.root = Tk()
        self.default_title = 'DsVis'
        self.initialize(self.root)
        Home(self.root, self.default_title)

    def initialize(self, root):
        root.resizable(FALSE, FALSE)
        root.title(self.default_title)
        '''try:
            base_folder = os.path.dirname(__file__)
            image_path = os.path.join(base_folder, 'icon.png')
            photo = PhotoImage(file=image_path)
            self.root.iconphoto(False, photo)
        except Exception:
            pass'''
        window_size = str(root.winfo_screenwidth() - 100) + 'x' + str(root.winfo_screenheight() - 100) + '+25+25'
        root.geometry(window_size)
