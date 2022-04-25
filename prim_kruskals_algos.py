class Graph_Algorithms(DFS_Cyclicity): # DFS_Cyclicity Will be used in Naive-Kruskal

  def __init__(self, numberOfVertices):

    '''
      numberOfVertices : |Vertices|
      self.parent_prim -> PRIM : (child, parent) pairs, initially defined as (child, None) pairs
      self.keys -> PRIM : (node, weight) pairs whose weights are initially set to +inf
      self.parent -> KruskalUF : (child, parent) pairs, initially defined as (child, child) pairs
      self.size -> KruskalUF : (subtree, size) pairs whose sizes are initially set to 1
    '''

    self.V = numberOfVertices
    self.graph = []
    self.parent_prim = {i : None for i in range(1, self.V + 1)} # Will be used in PRIM
    self.keys = {i : float("inf") for i in range(1, self.V + 1)} # Will be used in PRIM
    self.parent = {i : i for i in range(1, self.V + 1)} # Will be used in KruskalUF
    self.size = {i : 1 for i in range(1, self.V + 1)} # Will be used in KruskalUF

  def graphConstruction(self, edgeList):

    '''
      self.graph : Set of edges, each edge representing as [u, v, w]
      u, v : Adjacent nodes -> (u, v) is incident on u, v
      w : Edge weight
    '''

    self.graph = edgeList

  def __extractMin(self, query): # Will be used in PRIM

        min_u = min(query, key=self.keys.get)
        query.remove(min_u)

        return min_u

  def __find_adjacent(self, u): # Will be used in PRIM

        adjacents = set()
        edges_of_graph = list(map(lambda x : x[:2] , self.graph))

        for edge in edges_of_graph:

              if edge[0] == u:
                    adjacents.add(edge[1])

              elif edge[1] == u:
                    adjacents.add(edge[0])

        return adjacents

  def __findParent(self, child): # Will be used in KruskalUF

    '''
      child: A node whose parent is supposed to get discoverd

      __findParent(child): Is a recurssive function that returns
      the rootNode of a subtree containing child
    '''

    if self.parent[child] == child:

      return child

    return self.__findParent(self.parent[child])

  def __Union(self, x, y): # Will be used in KruskalUF

    '''
      x, y : Nodes whose associated subtrees will be merged together

      __Union(x, y): Each time this function is called, it checks whether Find(x) and
      Find(y) is equal. If so, it does nothing. Otherwise, it checks if the size of
      subtree containing x is greater or equal than the size of subtree containing y.
      If so, it merges the second subtree with the first one. Otherwise, it merges the
      first subtree with the second one. 
    '''

    rootX = self.__findParent(x)
    rootY = self.__findParent(y)

    if rootX == rootY:

      pass

    elif self.size[rootX] >= self.size[rootY]:

      self.parent[rootY] = rootX
      self.size[rootX] += self.size[rootY]

    else:

      self.parent[rootX] = rootY
      self.size[rootY] += self.size[rootX]


  def PRIM(self, start, verbose=False):
    
    query = [i for i in range(1, self.V + 1)] # Q <- V
    self.keys[start] = 0

    while len(query) != 0: 

      u = self.__extractMin(query)
      adjacents = self.__find_adjacent(u)

      for v in adjacents:

        key = 0
        key_list1 = list(filter((lambda x : x[:2] == [u, v]), self.graph))
        key_list2 = list(filter((lambda x : x[:2] == [v, u]), self.graph))

        if key_list1 != []:

          key = key_list1[0][-1]
        else:

          key = key_list2[0][-1]
                    
        if v in query and key < self.keys[v]:
          self.keys[v] = key
          self.parent_prim[v] = u
        
    values = self.keys.values()
    totalWeight = sum(values)

    if verbose:

      print(f"MST found by PRIM algorithm: {totalWeight}")

    return totalWeight
        
  def NaiveKruskal(self, verbose=False):

    '''
      This method is using DFS_Cyclicity to check if a graph is ascyclic.
    ''' 

    A = []
    A_withWeights = []

    totalWeight = 0
    # sort edges of G by weight
    self.graph = sorted(self.graph, key=lambda item: item[2]) 

    s = self.graph[0][0]
    
    for (u, v, w) in self.graph: # foreach edge e, in nondecreasing order of weight do

      copy = A.copy()
      copy.append([u, v])

      super().__init__()
      self.graphInit(copy)

      if self.cycleChecking() == "acyclic":# if A U {e} is acyclic then

        A.append([u, v]) # A = A U {e}
        A_withWeights.append([u, v, w])

    for (u, v, w) in A_withWeights:

      totalWeight += w

    if verbose:

      print(f"MST found by Naive-Kruskal algorithm: {totalWeight}")

    return totalWeight

  def KruskalUF(self, verbose=False):

    A = []

    totalWeight = 0

    self.graph = sorted(self.graph, key=lambda item: item[2])

    for (u, v, w) in self.graph:

      if self.__findParent(u) != self.__findParent(v):

        A.append([u, v, w])

        self.__Union(u, v)

    for (u, v, w) in A:

      totalWeight += w

    if verbose:
      
      print(f"MST found by Kruskal-UF algorithm: {totalWeight}")

    return totalWeight
