# Social_media_using_graph_analysis
run.py for GUI test depends to main.py and json_manager.py.<br>
main.py have the algorithms and input procces and core of project functions.<br>
json_manager.py is the manager of json save and retrieve app data.<br>

# Open TXT botton: 
text file format for each line -->(name_of_node1+" "+name_of_node2+" "+weight_of_edge)<br>
time complexity:O((#_of_lines)* (sum of length of tow node names))<br>
space complexity:O(V+E)

# Load JSON botton:
time complexity:O(string length of *.json file) OR O(V * E)<br>
space complexity:O(V + E)<br>

# Save JSON botton:
time complexity:O(V * E)<br>
space complexity:O(size of json file)<br>

# List of Friends:
time complexity:O(1)<br>
(in GUI Show Friends botton O(n) because of the output)<br>
space complexity:O(1)<br>
(in GUI Show Friends botton O(n) because of the output)<br>

# Same Group or tow users are connected?
time complexity:O(#_of_groups)<br>
space complexity:O(1)<br>

# Find shortest path
time complexity:O(V + E)    (in worst case)<br>
space complexity:O(#_of_nodes_in_path)<br>

# Friend suggestion
time complexity:O(V^2)<br>
space complexity:O(V^2)<br>

# List of Groups
time complexity:O(1)<br>
space complexity:O(V * (#_of_groups))    (because group set save in a list by index {group1} , {group2} , ...)<br>

# Popular person(s)
time complexity:O(V)<br>
space complexity:O(#_of_popular_person(s))<br>

# Friend(s) intersection between tow nodes
time complexity:O(min(len(s1) , len(s2)))<br>
space complexity:O(#_of_instersected_elements)<br>

# Network data
time complexity:O(1)      (for GUI output O(length of biggest group) or O(#_of_popular_person))<br>
space complexity:O(#_of_biggest_group_elements) or O(#_of_popular_persons)<br>

# BFS
time complexity:O(V + E)<br>
space complexity:O(V)<br>

# Add user
time complexity:O(1)<br>
space complexity:O(1)<br>

# Remove user
time complexity:O(#_of_friends) or O(#_of_groups)<br>
space complexity:O(1)<br>

# Add edge
time complexity:O(#_of_groups)<br>
space complexity:O(1)<br>

# Remove edge
time complexity:O(V + E)<br>
space complexity:O(1)<br>





# main.py Procces class:

Proccess(data).BFS(node("name of node"))-->O(V + E)<br>
Proccess(data)._group() --> O(V + E)<br>
Proccess(data).find_friend(node("name of node")) --> O(V^2)<br>
Proccess(data).popular_person() --> O(V)<br>
Proccess(data).intersecion(node("name of node") , node("name of node")) -- > O(min(len(s1) , len(s2)))<br>
Proccess(data).path(node("name of node") , node("name of node")) -- > O(V + E) in worst case <br>
Proccess(data).network() -- > O((#_of_groups)^2)<br>
