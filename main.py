from collections import deque, defaultdict
from math import inf

class node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.d = inf
    
    def __str__(self):
        return f"Node({self.name})"
    
    def __repr__(self):
        return f"Node({self.name})"
    
    def __eq__(self, value):
        return isinstance(value, node) and self.name == value.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __iter__(self):
        return iter([])

def txtproccess(txt):
    g = defaultdict(set)
    nodes_cache = {}
    
    def get_or_create_node(name):
        if name not in nodes_cache:
            nodes_cache[name] = node(name)
        return nodes_cache[name]
    
    edge_count = 0
    for line in txt:
        parts = line.strip().split()
        if len(parts) == 1: 
            k = get_or_create_node(parts[0])
            if k not in g:
                g[k] = set()
        elif len(parts) >= 2: 
            k = get_or_create_node(parts[0])
            v = get_or_create_node(parts[1])
            if v not in g[k]:
                g[k].add(v)
                g[v].add(k)
                edge_count += 1
    
    return (g, edge_count)

class Proccess():
    def __init__(self, input_txt):
        self.gg = None
        self.g, self.e = txtproccess(input_txt)
        self._components = None
    
    def _find_components(self):
        if self._components is not None:
            return self._components
        
        visited = set()
        components = []
        
        for node_item in list(self.g.keys()):
            if node_item not in visited:
                component = set()
                queue = deque([node_item])
                visited.add(node_item)
                
                while queue:
                    current = queue.popleft()
                    component.add(current)
                    for neighbor in self.g[current]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                
                components.append(component)
        
        self._components = components
        return components
    
    def group(self):
        components = self._find_components()
        self.gg = components
        return components
    
    def find_friend(self, start: node):
        if start not in self.g:
            return set()
        
        friends = set()
        for neighbor in self.g[start]:
            for friend in self.g[neighbor]:
                if friend == start or friend in self.g[start]:
                    continue
                friends.add(friend)
        
        return friends
    
    def popular_person(self):
        if not self.g:
            return []
        
        max_degree = max(len(neighbors) for neighbors in self.g.values())
        popular = [n for n, neighbors in self.g.items() if len(neighbors) == max_degree]
        
        return popular
    
    def intersecion(self, u: node, v: node):
        if u not in self.g or v not in self.g:
            return set()
        return self.g[u].intersection(self.g[v])
    
    def path(self, start: node, stop: node):
        if start not in self.g or stop not in self.g:
            return []
        
        visited = {start}
        queue = deque([(start, [start])])
        
        while queue:
            current, path_list = queue.popleft()
            if current == stop:
                return path_list
            
            for neighbor in self.g[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path_list + [neighbor]))
        
        return []
    
    def network(self):
        lnn = len(self.g.keys())
        
        if self._components is None:
            self._find_components()
        
        biggest_group = set()
        for comp in self._components:
            if len(comp) > len(biggest_group):
                biggest_group = comp
        
        max_possible_edges = (lnn * (lnn - 1)) // 2 if lnn > 1 else 1
        ratio = self.e / max_possible_edges if max_possible_edges > 0 else 0
        
        return (lnn, self.e, ratio, biggest_group, self.popular_person())
    
    def BFS(self, start: node):
        if start not in self.g:
            return {}
        
        distances = {start: 0}
        queue = deque([start])
        visited = {start}
        
        while queue:
            current = queue.popleft()
            for neighbor in self.g[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        
        result = defaultdict(set)
        for user, dist in distances.items():
            result[dist].add(user)
        
        return result
    
    def are_connected(self, user1: node, user2: node):
        if user1 not in self.g or user2 not in self.g:
            return False
        
        visited = {user1}
        queue = deque([user1])
        
        while queue:
            current = queue.popleft()
            if current == user2:
                return True
            for neighbor in self.g[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return False
