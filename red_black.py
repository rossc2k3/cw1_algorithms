
# File:     red_black.py
# Author:   John Longley
# Date:     October 2022

# Template file for Inf2-IADS (2022-23) Coursework 1, Part B
# Implementation of dictionaries by red-black trees: space-saving version

# Provided code:

Red, Black = True, False

def colourStr(c):
    return 'R' if c==Red else 'B'

Left, Right = 0, 1

def opposite(branch):
    return 1 - branch

branchLabels = ['l','r']

class Node():
    
    def __init__(self,key,value):
        self.key = key
        self.value = value
        self.colour = Red
        self.left = None
        self.right = None
        
    def getChild(self,branch):
        if branch==Left:
            return self.left
        else:
            return self.right

    def setChild(self,branch,y):
        if branch==Left:
            self.left = y
        else:
            self.right = y

    def __repr__(self):
        return str(self.key) +':'+ str(self.value) +':'+ colourStr(self.colour)

# Use None for all trivial leaf nodes

def colourOf(x):
    if x is None:
        return Black
    else:
        return x.colour


class RedBlackTree():

    def __init__ (self):
        self.root = None
        self.stack = []


# TODO: Task 1.
#   lookup(self,key)


# TODO: Task 2.
#   plainInsert(self,key,value)


# TODO: Task 3.
#   tryRedUncle(self)
#   repeatRedUncle(self):


# Provided code to support Task 4:

    def toNextBlackLevel(self,node):
        # inspect subtree down to the next level of blacks
        # and return list of components (subtrees or nodes) in L-to-R order
        # (in cases of interest there will be 7 components A,a,B,b,C,c,D).
        if colourOf(node.left)==Black:  # node.left may be None
            leftHalf = [node.left]
        else:
            leftHalf = self.toNextBlackLevel(node.left)
        if colourOf(node.right)==Black:
            rightHalf = [node.right]
        else:
            rightHalf = self.toNextBlackLevel(node.right)
        return leftHalf + [node] + rightHalf

    def balancedTree(self,comps):
        # build a new (balanced) subtree from list of 7 components
        [A,a,B,b,C,c,D] = comps
        a.colour = Red
        a.left = A
        a.right = B
        c.colour = Red
        c.left = C
        c.right = D
        b.colour = Black
        b.left = a
        b.right = c
        return b


# TODO: Task 4.
#   endgame(self)
#   insert(self,key,value)
        

# Provided code:

    # Printing tree contents
    
    def __str__(self,x):
        if x==None:
            return 'None:B'
        else:
            leftStr = '[ ' + self.__str__(x.left) + ' ] '
            rightStr = ' [ ' + self.__str__(x.right) + ' ]'
            return leftStr + x.__str__() + rightStr

    def __repr__(self):
        return self.__str__(self.root)

    def showStack(self):
        return [x.__str__() if isinstance(x,Node) else branchLabels[x]
                for x in self.stack]

    # All keys by left-to-right traversal
    
    def keysLtoR_(self,x):
        if x==None:
            return []
        else:
            return self.keysLtoR_(x.left) + [x.key] + self.keysLtoR_(x.right)

    def keysLtoR(self):
        return self.keysLtoR_(self.root)

# End of class RedBlackTree


# Creating a tree by hand:

sampleTree = RedBlackTree()
sampleTree.root = Node(2,'two')
sampleTree.root.colour = Black
sampleTree.root.left = Node(1,'one')
sampleTree.root.left.colour = Black
sampleTree.root.right = Node(4,'four')
sampleTree.root.right.colour = Red
sampleTree.root.right.left = Node(3,'three')
sampleTree.root.right.left.colour = Black
sampleTree.root.right.right = Node(6,'six')
sampleTree.root.right.right.colour = Black


# For fun: sorting algorithm using trees
# Will remove duplicates

def TreeSort(L):
    T = RedBlackTree()
    for x in L:
        T.insert(x,None)
    return T.keysLtoR()

# End of file
