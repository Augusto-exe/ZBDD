class Node:
    def __init__(self, top, p0, p1):
        self.top = top
        self.p0 = p0
        self.p1 = p1
    def printNode(self, node_num):
        print("[",node_num,"]", "var: ", self.top, " p0: ",self.p0, " p1: ",   self.p1)


class ZBDD:
    def __init__(self):
        self.uniq_table = []
        self.base_node = Node(-1, 0, 0)
        self.base_node_1 = Node(-1, 1, 1)
        self.uniq_table.append(self.base_node)
        self.uniq_table.append(self.base_node_1)

    def nodeInTable(self,P):

        for node in self.uniq_table:
            if node.top == P.top and node.p0 == P.p0 and node.p1 == P.p1:
                return self.uniq_table.index(node)
        return -1

    def getNode(self, top, p0, p1):
        if p1 == 0:
            return p0
        P = Node(top,p0,p1)
        n = self.nodeInTable(P)
        if n > 0:
            return n
        self.uniq_table.append(P)
        return self.uniq_table.index(P)
    
    def subset1(self, P, var):
        node = self.uniq_table[P]
        if node.top < var:
            return 0
        if node.top == var:
            return node.p1
        if node.top > var:
            return self.getNode(node.top, self.subset1(node.p0,var),self.subset1(node.p1,var))    
        
    def subset0(self, P, var):
        node = self.uniq_table[P]
        if node.top < var:
            return P
        if node.top == var:
            return node.p0
        if node.top > var:
            return self.getNode(node.top, self.subset0(node.p0,var),self.subset0(node.p1,var))        
        
    def change(self,P,var):
        node = self.uniq_table[P]
        if node.top < var:
            return self.getNode(var,0,P)
        if node.top == var:
            return self.getNode(var,node.p1,node.p0)
        if node.top > var:
            return self.getNode(node.top,self.change(node.p0,var),self.change(node.p1,var))

    def union(self,P,Q):
        nodeP = self.uniq_table[P]
        nodeQ = self.uniq_table[Q]
        if P == 0:
            return Q
        if Q == 0:
            return P
        if P == Q:
            return P
        if nodeP.top > nodeQ.top:
            return self.getNode(nodeP.top,self.union(nodeP.p0,Q),nodeP.p1)
        if nodeQ.top > nodeP.top:
            return self.getNode(nodeQ.top,self.union(P,nodeQ.p0),nodeQ.p1)
        if nodeP.top == nodeQ.top:
            return self.getNode(nodeP.top,self.union(nodeP.p0,nodeQ.p0),self.union(nodeP.p1,nodeQ.p1))
        
    def intsec(self,P,Q):
        nodeP = self.uniq_table[P]
        nodeQ = self.uniq_table[Q]
        if P == 0:
            return 0
        if Q == 0:
            return 0
        if P == Q:
            return P
        if nodeP.top > nodeQ.top:
            return self.intsec(nodeP.p0,Q)
        if nodeQ.top > nodeP.top:
            return self.intsec(P,nodeQ.p0)
        if nodeP.top == nodeQ.top:
            return self.getNode(nodeP.top,self.intsec(nodeP.p0,nodeQ.p0),self.intsec(nodeP.p1,nodeQ.p1))
        
    def diff(self,P,Q):
        nodeP = self.uniq_table[P]
        nodeQ = self.uniq_table[Q]
        if P == 0:
            return 0
        if Q == 0:
            return P
        if P == Q:
            return 0
        if nodeP.top > nodeQ.top:
            return self.getNode(nodeP.top,self.diff(nodeP.p0,Q),nodeP.p1)
        if nodeQ.top > nodeP.top:
            return self.diff(P,nodeQ.p0)
        if nodeP.top == nodeQ.top:
            return self.getNode(nodeP.top,self.diff(nodeP.p0,nodeQ.p0),self.diff(nodeP.p1,nodeQ.p1))
    
    def count(self,P):
        if P == 0: 
            return 0
        node = self.uniq_table[P]
        if node.p0 == 0 and node.p1 ==0:
            return 1

