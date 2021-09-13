from mainwindow.ds.dsgui.bst_gui import BSTgui, convert


class BST:
    def __init__(self, root):
        tree = BinarySearchTree()
        gui = BSTgui(root, tree)
        tree.setgui(gui)


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.id = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.gui = None

    def setgui(self, gui):
        self.gui = gui

    def insert(self, data, node='root'):
        # default node value
        if (node == 'root'):
            node = self.root
        # Empty tree
        if (not self.root):
            self.root = Node(data)
            return self.root
        # non-empty tree
        if (not node):
            return Node(data)
        if (data < node.data):
            self.gui.blink_highlight(self.gui.operations[-1][0].area, node.id)
            node.left = self.insert(data, node.left)
        elif (data > node.data):
            self.gui.blink_highlight(self.gui.operations[-1][0].area, node.id)
            node.right = self.insert(data, node.right)
        return node

    def delete(self, data, node='root'):
        if (node == 'root'):
            node = self.root
        if (not node):
            return node
        if (data < node.data):
            self.gui.blink_highlight(self.gui.operations[-1][0].area, node.id)
            node.left = self.delete(data, node.left)
        elif (data > node.data):
            self.gui.blink_highlight(self.gui.operations[-1][0].area, node.id)
            node.right = self.delete(data, node.right)
        else:
            self.gui.blink_highlight(self.gui.operations[-1][0].area, node.id)
            if not node.right:
                if (node == self.root):
                    self.root = node.left
                return node.left
            if not node.left:
                if (node == self.root):
                    self.root = node.right
                return node.right
            temp = self.get_substitute(node.left)
            node.data = temp.data
            node.left = self.delete(temp.data, node.left)
        return node

    def search(self, data, node='root'):
        if (node == 'root'):
            node = self.root
        if (not node):
            return False
        self.gui.blink_highlight(self.gui.operations[-1][0].area, node.id)
        if (node.data == data):
            return node
        if (data < node.data):
            return self.search(data, node.left)
        return self.search(data, node.right)

    def inorder(self, node='root'):
        elements = []
        if (node == 'root'):
            node = self.root
        if (node):
            elements += self.inorder(node.left)
            elements += [str(node.data)]
            self.gui.blink_highlight(self.gui.operations[-1][0].area, node.id)
            k = '\n' + convert(node.data)
            self.gui.operations[-1][1] += k
            self.gui.details_box.insert('end -1 chars', k)
            elements += self.inorder(node.right)
        return elements

    def preorder(self, node='root'):
        elements = []
        if (node == 'root'):
            node = self.root
        if (node):
            elements += [str(node.data)]
            self.gui.blink_highlight(self.gui.operations[-1][0].area, node.id)
            k = '\n' + convert(node.data)
            self.gui.operations[-1][1] += k
            self.gui.details_box.insert('end -1 chars', k)
            elements += self.preorder(node.left)
            elements += self.preorder(node.right)
        return elements

    def postorder(self, node='root'):
        elements = []
        if (node == 'root'):
            node = self.root
        if (node):
            elements += self.postorder(node.left)
            elements += self.postorder(node.right)
            elements += [str(node.data)]
            self.gui.blink_highlight(self.gui.operations[-1][0].area, node.id)
            k = '\n' + convert(node.data)
            self.gui.operations[-1][1] += k
            self.gui.details_box.insert('end -1 chars', k)
        return elements

    def check(self, data, node='root'):
        if (node == 'root'):
            node = self.root
        if (not node):
            return False
        if (node.data == data):
            return True
        if (data < node.data):
            return self.check(data, node.left)
        return self.check(data, node.right)

    def height(self, node='root'):
        if (node == 'root'):
            node = self.root
        height = 0
        if (not node):
            return height
        return max(self.height(node.left), self.height(node.right)) + 1

    def nodes_at_level(self, level, node='root'):
        elements = []
        if (node == 'root'):
            node = self.root
        if (node):
            if (level == 0):
                elements = [node]
            else:
                elements = self.nodes_at_level(level - 1, node.left)
                elements += self.nodes_at_level(level - 1, node.right)
        if (not node):
            elements = ['empty'] * (2 ** level)
        return elements

    def levelorder(self):
        h = self.height()
        levels = []
        for i in range(h):
            levels += [self.nodes_at_level(i)]
        return levels

    def get_substitute(self, node):
        if (node.right):
            return self.get_substitute(node.right)
        return node
