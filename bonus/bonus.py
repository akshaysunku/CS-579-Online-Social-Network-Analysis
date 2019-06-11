import networkx as nx
import numpy as np

'''
def example_graph():
    """
    Create the example graph from class. Used for testing.
    """
    g = nx.Graph()
    g.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'C'), ('B', 'D'), ('D', 'E'), ('D', 'F'), ('D', 'G'), ('E', 'F'), ('G', 'F')])
    nx.draw(g, with_labels=True)
    return g
'''

def jaccard_wt(graph, node):
    """
    The weighted jaccard score, defined above.
    Args:
      graph....a networkx graph
      node.....a node to score potential new edges for.
    Returns:
      A list of ((node, ni), score) tuples, representing the 
                score assigned to edge (node, ni)
                (note the edge order)
    """
    pass

    res = []
    neighbors = set(g.neighbors(node))
    non_neighbors = set(g.nodes()) - set(g.neighbors(node)) - {node}
    #print(neighbors)
    #print(non_neighbors)
    
    for i in non_neighbors:
        common = neighbors.intersection(set(g.neighbors(i)))
        num = [1/g.degree(n) for n in common]
        deno1 = [g.degree(n) for n in neighbors]
        deno2 = [g.degree(n) for n in set(g.neighbors(i))]
        score = np.sum(num) / ((1/np.sum(deno1)) + (1/np.sum(deno2)))
        res.append(((node, i), score))
    
    result = sorted(res, key=lambda x: (-x[1], x[0][1]))
    print(result)


if __name__ == '__main__':
    #g = example_graph()    #use this function for testing
    jaccard_wt(g, 'G')