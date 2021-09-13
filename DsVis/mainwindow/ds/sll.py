from mainwindow.ds.dsgui.sll_gui import SLLgui
import time


class SLL:
    def __init__(self, root):
        sll = LinkedList()
        gui = SLLgui(root, sll)
        sll.setgui(gui)


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.gui = None

    def setgui(self, gui):
        self.gui = gui

    def shiftdown(self, nid):
        found = False
        if self.head:
            temp = self.head
            while (temp):
                if (id(temp) == nid):
                    found = True
                if (found):
                    self.gui.node_move(str(id(temp)), 0, 110)
                temp = temp.next

    def shiftup(self, nid):
        found = False
        if self.head:
            temp = self.head
            while (temp):
                if (id(temp) == nid):
                    found = True
                if (found):
                    self.gui.node_move(str(id(temp)), 0, -110)
                temp = temp.next

    def search(self, data):
        self.gui.focus_item('headidbox')
        if not self.head:
            self.gui.details_box.insert('end -1 chars', '\nNot Found')
            return False
        temp = self.head
        while (temp):
            self.gui.blink_node(str(id(temp)))
            if (temp.data == data):
                self.gui.blink_node(str(id(temp)), color=self.gui.blue_color)
                self.gui.details_box.insert('end -1 chars', '\nFound')
                return True
            temp = temp.next
        self.gui.details_box.insert('end -1 chars', '\nNot Found')
        return False

    def insert_at_end(self, data):
        if not self.head:
            self.head = Node(data)
            self.gui.blink_next_field('headidbox')
            self.gui.area.itemconfigure('headid', text=str(id(self.head)))
            self.gui.draw(self.gui.area.bbox('headidbox')[3], id(self.head), self.head.data, self.head.next)
            self.gui.details_box.insert('end -1 chars', '\nDone!')
            return
        temp = self.head
        self.gui.blink_node(str(id(temp)))
        while (temp.next):
            temp = temp.next
            self.gui.blink_node(str(id(temp)))
        temp.next = Node(data)
        self.gui.blink_next_field(str(id(temp)))
        self.gui.area.itemconfigure(str(id(temp)) + 'nextid', text=id(temp.next))
        self.gui.draw(self.gui.area.bbox(str(id(temp)) + 'nextidbox')[3], id(temp.next), temp.next.data, temp.next.next)
        self.gui.details_box.insert('end -1 chars', '\nDone!')

    def insert_at_beg(self, data):
        self.gui.focus_item('headidbox')
        if not self.head:
            self.head = Node(data)
            self.gui.blink_next_field('headidbox')
            self.gui.area.itemconfigure('headid', text=str(id(self.head)))
            self.gui.draw(self.gui.area.bbox('headidbox')[3], id(self.head), self.head.data, self.head.next)
            self.gui.details_box.insert('end -1 chars', '\nDone!')
            return
        temp = self.head
        self.shiftdown(id(temp))
        time.sleep(0.5)
        self.gui.area.update()
        self.head = Node(data)
        self.head.next = temp
        self.gui.blink_next_field('headidbox')
        self.gui.area.itemconfigure('headid', text=str(id(self.head)))
        self.gui.draw(self.gui.area.bbox('headidbox')[3], id(self.head), self.head.data, self.head.next)
        self.gui.details_box.insert('end -1 chars', '\nDone!')

    def del_at_end(self):
        self.gui.focus_item('headidbox')
        if not self.head:
            self.gui.details_box.insert('end -1 chars', '\nNo items left \nto delete!')
            return False  # empty sll
        if not self.head.next:
            self.gui.node_delete(str(id(self.head)))
            self.gui.blink_next_field('headidbox')
            self.gui.area.itemconfigure('headid', text='NULL')
            self.head = None
            self.gui.details_box.insert('end -1 chars', '\nDone!')
            return True
        temp = self.head
        while (True):
            self.gui.blink_node(str(id(temp)))
            if not temp.next.next:
                self.gui.blink_node(str(id(temp.next)), self.gui.blue_color)
                self.gui.node_delete(str(id(temp.next)))
                temp.next = None
                self.gui.blink_next_field(str(id(temp)))
                self.gui.area.itemconfigure(str(id(temp)) + 'nextid', text='NULL')
                break
            temp = temp.next
        self.gui.details_box.insert('end -1 chars', '\nDone!')
        return True

    def del_at_beg(self):
        self.gui.focus_item('headidbox')
        if not self.head:
            self.gui.details_box.insert('end -1 chars', '\nNo items left \nto delete!')
            return False  # empty sll
        self.gui.node_delete(str(id(self.head)))
        self.gui.area.update()
        time.sleep(1.0)
        self.gui.area.update()
        self.head = self.head.next
        self.shiftup(id(self.head))
        text = str(id(self.head)) if (id(self.head) != id(None)) else 'NULL'
        self.gui.blink_next_field('headidbox')
        self.gui.area.itemconfigure('headid', text=text)
        self.gui.details_box.insert('end -1 chars', '\nDone!')
        return True

    def del_data(self, data):
        self.gui.focus_item('headidbox')
        if not self.head:
            self.gui.details_box.insert('end -1 chars', '\nElement not found!')
            return False  # empty sll
        if self.head.data == data:
            self.gui.blink_node(str(id(self.head)), color=self.gui.blue_color)
            self.gui.node_delete(str(id(self.head)))
            self.gui.area.update()
            time.sleep(1.0)
            self.gui.area.update()
            self.head = self.head.next
            self.shiftup(id(self.head))
            text = str(id(self.head)) if (id(self.head) != id(None)) else 'NULL'
            self.gui.blink_next_field('headidbox')
            self.gui.area.itemconfigure('headid', text=text)
            self.gui.details_box.insert('end -1 chars', '\nDone!')
            return True
        if not self.head.next:
            self.gui.blink_node(str(id(self.head)))
            self.gui.details_box.insert('end -1 chars', '\nElement not found!')
            return False
        temp = self.head
        self.gui.blink_node(str(id(temp)))
        while (temp and temp.next):
            if temp.next.data == data:
                self.gui.blink_node(str(id(temp.next)), color=self.gui.blue_color)
                self.gui.node_delete(str(id(temp.next)))
                self.gui.area.update()
                time.sleep(1.0)
                self.gui.area.update()
                text = str(id(temp.next.next)) if (id(temp.next.next) != id(None)) else 'NULL'
                self.gui.blink_next_field(str(id(temp)))
                self.gui.area.itemconfigure(str(id(temp)) + 'nextid', text=text)
                temp.next = temp.next.next
                self.shiftup(id(temp.next))
                self.gui.details_box.insert('end -1 chars', '\nDone!')
                return True
            temp = temp.next
            self.gui.blink_node(str(id(temp)))
        self.gui.details_box.insert('end -1 chars', '\nElement not found!')
        return False

    def insert_after(self, data, adata):
        self.gui.focus_item('headidbox')
        if not self.head:
            self.gui.details_box.insert('end -1 chars', '\nElement not found!')
            return False  # adata not found
        temp = self.head
        while (temp):
            if (temp.data == adata):
                self.gui.blink_node(str(id(temp)), color=self.gui.blue_color)
                tnode = Node(data)
                self.gui.blink_next_field(str(id(temp)))
                self.gui.area.itemconfigure(str(id(temp)) + 'nextid', text=str(id(tnode)))
                tnode.next = temp.next
                self.shiftdown(id(temp.next))
                self.gui.area.update()
                time.sleep(0.5)
                self.gui.area.update()
                temp.next = tnode
                self.gui.draw(self.gui.area.bbox(str(id(temp)) + 'nextidbox')[3], id(temp.next), temp.next.data,
                              temp.next.next)
                self.gui.details_box.insert('end -1 chars', '\nDone!')
                return True
            self.gui.blink_node(str(id(temp)))
            temp = temp.next
        self.gui.details_box.insert('end -1 chars', '\nElement not found!')
        return False

    def insert_before(self, data, bdata):
        self.gui.focus_item('headidbox')
        if not self.head:
            self.gui.details_box.insert('end -1 chars', '\nElement not found!')
            return False  # bdata not found
        if self.head.data == bdata:
            temp = self.head
            self.gui.blink_node(str(id(temp)), color=self.gui.blue_color)
            self.head = Node(data)
            self.head.next = temp
            self.shiftdown(id(temp))
            self.gui.area.update()
            time.sleep(0.5)
            self.gui.area.update()
            self.gui.blink_next_field('headidbox')
            self.gui.area.itemconfigure('headid', text=str(id(self.head)))
            self.gui.draw(self.gui.area.bbox('headidbox')[3], id(self.head), self.head.data, self.head.next)
            self.gui.details_box.insert('end -1 chars', '\nDone!')
            return True
        if not self.head.next:
            self.gui.blink_node(str(id(self.head)))
            self.gui.details_box.insert('end -1 chars', '\nElement not found!')
            return False
        prev = self.head
        self.gui.blink_node(str(id(prev)))
        temp = self.head.next
        while (temp.data != bdata):
            self.gui.blink_node(str(id(temp)))
            prev = prev.next
            temp = temp.next
            if not temp:
                self.gui.details_box.insert('end -1 chars', '\nElement not found!')
                return False
        self.gui.blink_node(str(id(temp)), color=self.gui.blue_color)
        temp = prev.next
        self.shiftdown(id(temp))
        self.gui.area.update()
        time.sleep(0.5)
        self.gui.area.update()
        prev.next = Node(data)
        self.gui.blink_next_field(str(id(prev)))
        self.gui.area.itemconfigure(str(id(prev)) + 'nextid', text=str(id(prev.next)))
        prev.next.next = temp
        self.gui.draw(self.gui.area.bbox(str(id(prev)) + 'nextidbox')[3], id(prev.next), prev.next.data, prev.next.next)
        self.gui.details_box.insert('end -1 chars', '\nDone!')
        return True

    def del_after(self, adata):
        self.gui.focus_item('headidbox')
        if not self.head:
            self.gui.details_box.insert('end -1 chars', '\nElement not found!')
            return False  # adata not found
        temp = self.head
        while (temp.data != adata):
            self.gui.blink_node(str(id(temp)))
            temp = temp.next
            if not temp:
                self.gui.details_box.insert('end -1 chars', '\nElement not found!')
                return False
        if not temp.next:
            self.gui.blink_node(str(id(temp)))
            self.gui.details_box.insert('end -1 chars', '\nGiven element is \nfound at the end \nof the list!')
            return False  # last item in the sll
        self.gui.blink_node(str(id(temp)), color=self.gui.blue_color)
        self.gui.node_delete(str(id(temp.next)))
        self.gui.area.update()
        time.sleep(0.5)
        self.gui.area.update()
        text = str(id(temp.next.next)) if (id(temp.next.next) != id(None)) else 'NULL'
        self.gui.blink_next_field(str(id(temp)))
        self.gui.area.itemconfigure(str(id(temp)) + 'nextid', text=text)
        temp.next = temp.next.next
        self.shiftup(id(temp.next))
        self.gui.details_box.insert('end -1 chars', '\nDone!')
        return True

    def del_before(self, bdata):
        self.gui.focus_item('headidbox')
        if not self.head:
            self.gui.details_box.insert('end -1 chars', '\nNot possible!')
            return False  # bdata not found
        if not self.head.next:
            self.gui.blink_node(str(id(self.head)))
            self.gui.details_box.insert('end -1 chars', '\nNot possible!')
            return False  # bdata not found or it may be the first element
        self.gui.blink_node(str(id(self.head)))
        if self.head.next.data == bdata:
            self.gui.blink_node(str(id(self.head.next)), color=self.gui.blue_color)
            self.gui.node_delete(str(id(self.head)))
            self.gui.area.update()
            time.sleep(0.5)
            self.gui.area.update()
            self.head = self.head.next
            self.gui.blink_next_field('headidbox')
            self.gui.area.itemconfigure('headid', text=str(id(self.head)))
            self.shiftup(id(self.head))
            self.gui.details_box.insert('end -1 chars', '\nDone!')
            return True
        if not self.head.next.next:
            self.gui.blink_node(str(id(self.head.next)))
            self.gui.details_box.insert('end -1 chars', '\nNot possible!')
            return False
        prev = self.head
        self.gui.blink_node(str(id(self.head.next)))
        temp = self.head.next.next
        while (temp.data != bdata):
            self.gui.blink_node(str(id(temp)))
            prev = prev.next
            temp = temp.next
            if not temp:
                self.gui.details_box.insert('end -1 chars', '\nNot possible!')
                return False  # bdata not found or it may be the first element
        self.gui.blink_node(str(id(temp)), color=self.gui.blue_color)
        self.gui.node_delete(str(id(prev.next)))
        self.gui.area.update()
        time.sleep(0.5)
        self.gui.area.update()
        prev.next = prev.next.next
        self.gui.blink_next_field(str(id(prev)))
        self.gui.area.itemconfigure(str(id(prev)) + 'nextid', text=str(id(prev.next)))
        self.shiftup(id(prev.next))
        self.gui.details_box.insert('end -1 chars', '\nDone!')
        return True
