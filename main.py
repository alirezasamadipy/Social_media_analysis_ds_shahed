#algorithms  , input proccess , data will be here. 
from collections import deque , defaultdict
from math import inf
data =  open("/media/alireza/Local Disk/ALIREZA/VS CODE/Social media project with Graph(data structure course)/data1.txt")

class node: 
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.d = inf

    def __str__(self):
        return f"Node({self.name})"

    def __eq__(self, value):
        return isinstance(value, node) and self.name == value.name

    def __hash__(self):
        return hash(self.name)
    def __iter__(self):
        return 


groups = []  #groups list declaration



def txtproccess(txt):  #proccess the input text file
    e = 0  #number of edges
    g = defaultdict(set)  #graph network declaration
    for line in txt:
        k,v =line[:-2].split()
        k = node(k)
        v = node(v)
        if v in g[k] :
            continue
            
        g[k].add(v)
        g[v].add(k)
        e += 1
    return (g , e)
    


def shortest_path(g:defaultdict,a:node , b:node) -> list: # finding the shortest path
    b = BFS(g , start=a , stop=b)
    lst = [b]
    #s=f"{b}"
    while b.parent != a:
        b = b.parent
        #s += f" -- {b}"  
        lst.append(b)
    lst.append(a)
    #print(s+f" -- {a}")
    return lst             # path from b  to  a nodes



def BFS(g:defaultdict,start:node , stop = node("not set"),grouping = False):
    #print(start)
    #print(stop)
    for u in g.keys():
        u.d = inf
    start.d = 0
    dlist = defaultdict(set)
    dlist[start.d] = start
    visited = set()
    que = deque()
    que.append(start)
    visited.add(start)
    if grouping:
        gg = g.copy()
        gg.pop(start)
    while que:
        node = que.popleft()
        # Process
        for neighbor in g[node]:
            if neighbor not in visited:
                neighbor.d = node.d + 1
                dlist[neighbor.d].add(neighbor)
                neighbor.parent = node
                que.append(neighbor)
                visited.add(neighbor)
                if grouping:
                    gg.pop(neighbor)
                if neighbor == stop:
                    return neighbor
    if not grouping:
        return dlist
    if grouping and gg:
        start = next(iter(gg))
        groups.append(BFS(gg , start , grouping=True))
    return visited





class Proccess():  #interface of main.py
    def __init__(self , input_txt):
        self.gg = None
        self.g , self.e = txtproccess(input_txt)
    def group(self): #grouping the network
        global groups
        groups.clear()
        groups.append(BFS(self.g , next(iter(self.g)) , grouping=True))
        self.gg = groups
        return groups
    def find_friend(self , start:node): #suggest friend for start node
        friends = set()
        for neighbor in self.g[start]:
            for friend in self.g[neighbor]:
                if friend == start or friend in self.g[start]:
                    continue
                friends.add(friend)
        return friends
    def popular_person(self): # person with largest community and friends
        self.pperson = []
        mx = 0
        for p in self.g.keys():
            ln = len(self.g[p])
            if mx < ln:
                self.pperson.append(p)
                mx = len(self.g[p])
            elif mx == ln:
                self.pperson.append(p)
        return self.pperson
    def intersecion(self , u:node , v:node): # friends of tow person
        return self.g[u].intersection(self.g[v])
    def path(self , start:node , stop:node):
        return shortest_path(self.g , start , stop) #shortest path from b to a
    def network(self):  # network data
        lnn = len(self.g.keys())
        if self.gg == None:
            self.group()
        biggest_group = set()
        mx = 0
        for p in range(len(self.gg)):
            ln = len(self.gg[p])
            if mx < ln:
                biggest_group = self.gg[p]
                mx = ln
        return ( lnn , self.e , lnn/self.e , biggest_group , self.popular_person() ) #8.a , 8.b , 8.c , 8.d , 8.e
    def BFS(self , start:node): # distance and list nodes from start node
        self.bf = BFS(self.g , start)
        return self.bf

    



            

