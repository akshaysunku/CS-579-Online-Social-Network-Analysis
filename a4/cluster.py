"""
Cluster data.
"""
import pickle
import networkx as nx
import matplotlib.pyplot as plt


def read_data():
    """ read the friend IDs of the users from the pickle file
    Args:
      Nothing
    Returns:
      the dictionary of users and their friends IDs
    """
    friends = pickle.load(open('./Collect Data/friends.pkl', 'rb'))
    return friends



def create_graph(friends):
    """ creates an undirected graph of the of the users and friends and 
    writes the summary to a text file
    Args:
      friends.... a dict of users and their friends IDs.
    Returns:
      An undirected networkx graph object
    """
    graph = nx.Graph()
    graph = nx.from_dict_of_lists(friends)

    file = open('./Cluster/cluster_summary.txt', 'w')
    file.write("Graph has " + str(len(graph.nodes())) + " nodes and " + str(len(graph.edges())) + "edges\n")

    return graph



def plot_initial_graph(graph):
    """ creates an image of an original graph before clustering.
    Args:
      graph.... networkx graph object
    Returns:
      Nothing
    """
    pos = nx.spring_layout(graph, scale = 5)
    plt.figure()
    plt.axis("off")

    nx.draw_networkx_nodes(graph, pos, alpha = 0.5, node_size = 22)
    nx.draw_networkx_edges(graph, pos, alpha = 0.3, width = 0.15)
    #nx.draw_networkx_labels(graph, labels=candidates, pos=pos,font_size=7)

    plt.savefig('./Cluster/Original Graph.png', dpi = 500)



def get_subgraph(graph, min_degree, make_subgraph):
    """ return a subgraph containing nodes whose degree is greater than
    or equal to min_degree.
    Args:
      graph........... networkx graph object.
      min_degree...... degree threshold.
      make_subgraph... decide to make a subgraph or not. When true makes
      a subgraph and when False returns the original graph.
    Returns:
      A graph
    """
    if make_subgraph == True:
        nodes = [node for node,deg in graph.degree() if deg < min_degree]
        graph.remove_nodes_from(nodes)
        print('subgraph has %s nodes and %s edges' % (len(graph.nodes()), len(graph.edges())))
        return graph

    return graph



def detect_communities(graph, max_depth):
    """ compute approximate betweenness of all the edges in the graph and keep
    removing all the edge edges until multiple components are formed.
    Args:
      graph....... a networkx graph object.
      max_depth... An integer representing the maximum depth to search.
    Returns:
      List of communities detected.
    """
    graph_copy = graph.copy()
    clusters = [comp for comp in nx.connected_component_subgraphs(graph_copy)]

    while len(clusters) < max_depth:
        edge_to_remove = find_best_edge(graph_copy)
        graph_copy.remove_edge(*edge_to_remove)
        clusters = [i for i in nx.connected_component_subgraphs(graph_copy)]

    return clusters



def find_best_edge(edge):
    """ this method uses the edge_betweenness_centrality to 
    find the edge with maximum betweenness.
    Args:
      edge.... a copied graph
    Returns:
      edge with the maximum betweenness value.
    """
    betweenness = nx.edge_betweenness_centrality(edge)
    return sorted(betweenness.items(), key = lambda x: -x[1])[0][0]



def clusters_info(clusters):
    """ get all the cluster information and write to a text file.
    Args:
      clusters... list of communities detected.
    Returns:
      Nothing
    """
    num_nodes = 0
    for cluster in range(len(clusters)):
        num_nodes += len(clusters[cluster])

    average = num_nodes / len(clusters)

    file = open('./Cluster/cluster_summary.txt', 'w')
    print("Number of communities: %d\n" % len(clusters))
    file.write("Number of communities discovered:" + str(len(clusters)) + "\n\n")
    for i in range(len(clusters)):
        print("Cluster: %d \t Nodes: %d" % (i+1, len(clusters[i])) )
        file.write("Cluster:" + str(i+1) + '\t' + "Number of nodes:" + str(len(clusters[i])))
        file.write("\n")
    print("Average number of users per community: %d\n" % average)
    file.write("Average number of users per community:" + str(int(average)) + "\n\n")
    file.close()



def save_clusters(graph, clusters):
    """ creates an image of a graph after clustering.
    Args:
      graph..... a networkx graph.
      clusters.. list of communities detected.
    """
    pos = nx.spring_layout(graph, scale = 5)
    plt.figure()
    plt.axis("off")

    color = ['red', 'green', 'blue','yellow','purple', 'orange']
    for i in range(len(clusters)):
        nx.draw_networkx_nodes(graph, pos, nodelist = clusters[i], alpha = 0.5, node_size = 22, node_color = color[i])
    nx.draw_networkx_edges(graph, pos, alpha = 0.3, width = 0.15)
    #nx.draw_networkx_labels(graph, labels=candidates, pos=pos,font_size=7)

    plt.savefig('./Cluster/Clustered Graph.png', dpi = 500)



def main():
    followers_data = read_data()
    initial_graph = create_graph(followers_data)
    print('graph has %s nodes and %s edges' % (len(initial_graph.nodes()), len(initial_graph.edges())))
    plot_initial_graph(initial_graph)
    initial_graph = get_subgraph(initial_graph, 2, False)
    clusters = detect_communities(initial_graph, 6)
    clusters_info(clusters)
    save_clusters(initial_graph, clusters)
    pass

if __name__ == "__main__":
    main()
