class DFS_Cyclicity: 

  def __init__(self):

    '''
    This class will be used in Naive Kruskal algorithm where we need to check cyclicity.
    It uses DFS algorithm to label each edge, and then by computing ancestors, it checks
    whether a graph is cyclic or not.

    IMPORTANT NOTE: This class should also take this fact into account that the input graph
    might not be connected. Hence, it should go through all connected parts of the graph and
    check whether there is a cycle in that part. One would say that all input graphs are connected
    and MST is also connected, but we do not need to check cyclicity on the original graph or on 
    the final version of MST. Instead, we need to check it on the current non-completed version of
    MST, which might be not connected. For example, after some iterations, we might obtain a non-complete
    MST including following edges:
    Edges = [1, 2], [1, 3], [4, 5], [4, 6], [5, 6]
    This set of edges constructs a not connected graph and we still need to check cyclicity on this set.
    This class will check cyclicity over the all connected parts of a graph.
    '''

    self.G = []

  def graphInit(self, edgeList):

    '''
    self.visit:

    Since, selecting edges in Naive Kruskal algorithm is according to the weights (selects the minimum-weighted
    edge that does not create cycle) and not according to the order of vertices, the non-completed MST might
    consist of this set of edges:
    Edges = [19, 20], [11, 13], [20, 21], [31, 32]
    As it is obvious, the number associated with vertices does not necessarily start from 1 and does not go in order.
    So, python lists are not a good choice to track whether a NODE has already been VISITED. Instead, we are better to
    use python dictionaries whose keys are edges.
    In order to construct such a dictionary, we need to have the unique set of vertices which are the keys. That is why 
    in this function we define a attribute named self.uniqueVertices and use it when defining self.visit.
    '''

    self.G = edgeList
    self.uniqueVertices = []
    list(map(lambda x: list(map(lambda y: self.uniqueVertices.append(y), x)), self.G))

    # L_E.label
    self.label = {f"{edgeList[i][0]},{edgeList[i][1]}": None for i in range(len(self.G))}
    # L_E.ancestor
    self.ancestor = {f"{edgeList[i][0]},{edgeList[i][1]}": None for i in range(len(self.G))}
    # L_V.ID
    self.visit = {i : False for i in list(set(self.uniqueVertices))}

  def __cycleCheckingOnConnectedGraph(self, sourceNode):

    '''
    This function will label edges in a CONNECTED part of a graph as 
    DISCOVERY or BACK edge.
    '''

    self.visit[sourceNode] = True # L_V[v].ID <- 1

    for Ed in self.G: # forall e E G.incidentEdges(v) do

      if Ed[0] == sourceNode or Ed[1] == sourceNode: # graph is undirected

        if self.label[f"{Ed[0]},{Ed[1]}"] == None: # if(L_E[e].label) = null then

          w = Ed[1] if Ed[0] == sourceNode else Ed[0] # w <- G.opposite(v, e) -> It returns the pair of source node. 
          #If the source node is Ed[0], it returns Ed[1] and if the source node is Ed[1], it returns Ed[0].

          if not self.visit[w]: # if(L_V[w].ID = 0) then

            self.label[f"{Ed[0]},{Ed[1]}"] = "DISCOVERY" # L_E[e].label <- DISCOVERY
            self.__cycleCheckingOnConnectedGraph(w) # DFS(G, w)

          else:

            self.label[f"{Ed[0]},{Ed[1]}"] = "BACK" # L_E[e].label <- BACK
            self.ancestor[f"{Ed[0]},{Ed[1]}"] = w

    self.backEdges = [i for i in self.label.keys() if self.label[i] == "BACK"]

  def cycleChecking(self):

    '''
    As far as we have edges in the graph labeled as None, our graph is not
    fully visited and there is(are) (an)other connected part(s) to visit. That
    is why the below while loop will terminate if there is no None-labeled edge.
    This function visits and labels all of graph's edges, even if the graph is not
    connected.
    '''

    while None in self.label.values():

      # Find a node whose value is None and run the cycleCheckingOnConnectedGraph function
      # on this node. (source node)

      sN = int(list(self.label.keys())[list(self.label.values()).index(None)].split(",")[0])

      self.__cycleCheckingOnConnectedGraph(sN)
    
    # Once you labeled all edges, iterate on all edges. As soon as an edge e=(v,w) labelled
    #  as BACK and with L_E[e].ancestor = w is found, return "cyclic". Otherwise, "acyclic".

    for BcEd in self.backEdges:

      if self.ancestor[BcEd] == int(BcEd.split(',')[0]) or self.ancestor[BcEd] == int(BcEd.split(',')[-1]): # graph is undirected

        return "cyclic"

    return "acyclic"
