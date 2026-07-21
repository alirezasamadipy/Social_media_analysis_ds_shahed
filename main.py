#algorithms  , input proccess , data will be here. 
from collections import deque , defaultdict
data =  open("data.txt")

class node:
    def __init__(self, name):
        self.name = name
        self.parent = None

    def __str__(self):
        return f"Node({self.name})"

    def __eq__(self, value):
        return isinstance(value, node) and self.name == value.name

    def __hash__(self):
        return hash(self.name)

Graph = defaultdict(set)
groups = []



def txtproccess(g:defaultdict , txt):
    for line in txt:
        k,v =line[:-2].split()
        g[node(k)].add(node(v))
        g[node(v)].add(node(k))
    


def shortest_path(g:defaultdict,a:node , b:node) -> list:
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
                neighbor.parent = node
                que.append(neighbor)
                visited.add(neighbor)
                if grouping:
                    gg.pop(neighbor)
                if neighbor == stop:
                    return neighbor
    
    if grouping and gg:
        start = next(iter(gg))
        groups.append(BFS(gg , start , grouping=True))
    return visited
    

    


txtproccess(Graph ,data)
groups.append(BFS(Graph , node("adlfj") , grouping=True))
print( len(groups))
#shortest_path(Graph , node("321") , node("adlfj"))


