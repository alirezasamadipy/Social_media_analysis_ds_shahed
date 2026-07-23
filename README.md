# Social_media_using_graph_analysis
Run the run.py for GUI test.<br>
main.py have the algorithms and input proccess and core of project functions.<br>

main.py input:text file format -->(name_of_node1+" "+name_of_node2+" "+weight_of_edge)<br>

main.py timecomplexities:<br>
creating a object of Proccess(data)--> O(# lines in text file)<br>
Proccess(data).BFS(node("name of node"))-->O(V + E)<br>
Proccess(data).group() --> O(V + E)<br>
Proccess(data).find_friend(node("name of node")) --> O((# neighbors)*(# neighbors of neighbors))<br>
Proccess(data).popular_person() --> O(V)<br>
Proccess(data).intersecion(node("name of node") , node("name of node")) -- > O(min(len(s1) , len(s2)))<br>
Proccess(data).path(node("name of node") , node("name of node")) -- > O(V + E)<br>
Proccess(data).network() -- > O(# groups * (V + E))<br>
