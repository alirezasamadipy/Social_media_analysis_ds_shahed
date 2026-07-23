# Social_media_using_graph_analysis
Run the run.py for GUI test.\n
main.py have the algorithms and input proccess and core of project functions.\n

main.py input:text file format -->(name_of_node1+" "+name_of_node2+" "+weight_of_edge)\n

main.py timecomplexities:\n
creating a object of Proccess(data)--> O(# lines in text file)\n
Proccess(data).BFS(node("name of node"))-->O(V + E)\n
Proccess(data).group() --> O(V + E)\n
Proccess(data).find_friend(node("name of node")) --> O((# neighbors)*(# neighbors of neighbors))\n
Proccess(data).popular_person() --> O(V)\n
Proccess(data).intersecion(node("name of node") , node("name of node")) -- > O(min(len(s1) , len(s2)))\n
Proccess(data).path(node("name of node") , node("name of node")) -- > O(V + E)\n
Proccess(data).network() -- > O(# groups * (V + E))\n