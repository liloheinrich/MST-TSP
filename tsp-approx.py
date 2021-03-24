"""
Advanced Algorithms HW3, Q3: Implement a 2-approximation algorithm for the metric TSP problem!

The code is directly drawn from a very outstanding existing implementation:
https://github.com/shiThomas/MST-TSP

Hence, the answers are available at the GitHub link above!
Please don't look at it unless you are absolutely stuck, even after hours!
"""

import math
import copy 
import itertools
################################################################################

"""
Prim's Algorithm
This Function builds a MST from the given map using the Prim's algorithm.
This is provided! No need to change anything.

Input:
adjList: the list of all neighbors of all cities in the map
adjMat: the 2D array representing the distance between two cities

Output:
This function has no output, it just changes the vertexes' attributes
"""
def prim(adjList, adjMat):

    # initialize all vertexes in the graph
    for vertex in adjList:
        vertex.cost = math.inf
        vertex.prev = None
        vertex.visited = False
        # set the vertex with rank 0 as start
        if vertex.rank == 0:
            start = vertex
            start.cost = 0

    # initialize the priority queue
    Q = MinQueue(adjList)
    while not Q.isEmpty():
        # get the next unvisited vertex and visit it
        v = Q.deleteMin()
        v.visited = True

        # For each edge out of v
        for neigh in v.neigh:

            # If the edge leads out, update
            if not neigh.visited:
                if neigh.cost > adjMat[v.rank][neigh.rank]:
                    neigh.cost = adjMat[v.rank][neigh.rank]
                    neigh.prev = v
    return

################################################################################

"""
TSP
Use a 2-approximation to get an approximate solution of the TSP problem.

Input:
adjList: the list of all neighbors of all cities in the map
start: the city where we start our tour
(see Map class for more information!)

Output:
A tour which is a cycle of cities.
Its cost is at most twice the optimal solution
It should be an array of cities visited in the tour, in the order visited.
The cities should be denoted by their rank (their numbering in adjList).
"""
def tsp(adjList, start):
    ##### Your implementation goes here. #####
    tour = []

    for v in adjList:
        v.visited = False

    stack = []
    stack.append(start)

    while stack:
        curr = stack.pop()
        curr.visited = True
        tour.append(curr.rank)

        for n in curr.mstN:
            if n.visited is False:
                stack.append(n)

    tour.append(start.rank)
    return tour

################################################################################

"""
Vertex Class
Provided for your convenience! Don't change anything.
"""
class Vertex:

    """
    Class attributes:

    rank    # The rank of this node.
    neigh   # The list of neighbors IN THE ORIGINAL GRAPH.
    mstN    # The list of neighbors IN THE MST.
    visited # A flag for whether the vertex has been visited.
    cost    # The cost of the edge out of the tree.
    prev    # The previous vertex in the path.
    city    # The name of the associated city.
    """

    """
    __init__ function to initialize the vertex.
    """
    def __init__(self, rank):

        self.rank = rank     # Set the rank of this vertex.
        self.neigh = []      # Set the input neighbors.
        self.mstN = []       # Set the mst neighbors.
        self.visited = False # Not yet visited.
        self.cost = math.inf # Infinite cost initially.
        self.prev = None     # No previous node on path yet.
        self.city = ''       # No city initially.
        return

    """
    __repr__ function to print a vertex.
    Note: only prints the city!
    """
    def __repr__(self):
        return '%s' % self.city

    """
    isEqual function compares this Vertex to an input Vertex object.
    Note: only needs to compare the rank!
    """
    def isEqual(self,vertex):
        return self.rank == vertex.rank

    """
    Overloaded comparison operators for priority queue.
    Sorted by cost.
    """
    def __lt__(self, other):
        return self.cost < other.cost

################################################################################

"""
Edge Class
Provided for your convenience! Don't change anything.
"""
class Edge:

    """
    Class attributes:

    vertices # The list of vertices for this edge.
    weight   # The weight of this edge.
    """

    """
    __init__ function to initialize the edge.

    INPUTS:
    vertex1 and vertex2: the vertices for the edge
    weight: the weight of the edge
    """
    def __init__(self, vertex1=None, vertex2=None, weight=math.inf):
        self.vertices = [vertex1]+[vertex2]
        self.weight = weight
        return

    """
    __repr__ function to print an edge.
    """
    def __repr__(self):
        return '(%s,%s): %f' % (self.vertices[0].city, \
                                self.vertices[1].city, \
                                self.weight)

    """
    Overloaded comparison operators for sorting by weight...
    """
    def __lt__(self, other):
        return self.weight < other.weight
    def __le__(self, other):
        return self.weight <= other.weight
    def __eq__(self, other):
        return self.weight == other.weight
    def __ne__(self, other):
        return self.weight != other.weight
    def __gt__(self, other):
        return self.weight > other.weight
    def __ge__(self, other):
        return self.weight >= other.weight

################################################################################

"""
minQueue Class
Provided for your convenience! Don't change anything.
"""
class MinQueue:

    """
    Class attributes:
    array # The array storing the values in the queue.
          # Note: the values must have comparison operations.
    """

    """
    __init__ function to initialize the edge.

    INPUTS:
    array: the input array to be inserted into the queue.
    """
    def __init__(self, array=[]):
        self.array = array.copy()
        return

    """
    __repr__ function to print an edge.
    """
    def __repr__(self):
        return repr(self.array)

    """
    isEmpty: check if the queue is empty.
    """
    def isEmpty(self):
        if len(self.array) == 0:
            return True
        else:
            return False

    """
    insert: insert an object into the queue.
    """
    def insert(self, val):
        self.array.append(val)

    """
    deleteMin: returns the min element and removes it from the queue.
    """
    def deleteMin(self):
        # Check if empty.
        if len(self.array) == 0:
            raise Exception('Cannot delete min from an empty queue.')

        # Start by considering the first element.
        minVal = self.array[0]
        minInd = 0

        # Loop to find the min element.
        for ind in range(1,len(self.array)):
            if self.array[ind] < minVal:
                minVal = self.array[ind]
                minInd = ind

        # Remove the min and return it.
        self.array.pop(minInd)
        return minVal

################################################################################

"""
Map Class

TODO!!
You need to complete the getTSPApprox() and getTSPOptimal() methods.
Everything else is complete and provided for your convenience.
"""
class Map:

    """
    Class attributes:
    adjMat   # The adjacency matrix storing edge weights.
    cities   # The list of city names.
    adjList  # The list of vertices.
    edgeList # The list of edges (edge objects).
    start    # The starting vertex of the tour.
    mst      # The edges in the MST.
    tour     # The approximate TSP tour (list of vertex ranks).
    tourOpt  # The optimal TSP tour (list of vertex ranks).
    optTour  # A string displaying the optimal tour.
    """

    """
    __init__ function to initialize the map.

    INPUTS:
    mapNum: The number of the map to use.
    """
    def __init__(self, mapNum=0):
        # Get the adjMat, cities, and optTour using mapNum.
        self.adjMat, self.cities, self.optTour = getMap(mapNum)[0:3]
        self.mapNum = mapNum

        # Create the adjList of vertices
        self.adjList = []
        for rank in range(0,len(self.cities)):
            v = Vertex(rank)
            self.adjList.append(v)

        # Create the list of edges and fill the vertex.neigh values.
        # Fill in the cities while we are at it.
        self.edgeList = []
        for r1 in range(0,len(self.adjMat)):
            v1 = self.adjList[r1]
            v1.city = self.cities[r1]
            for r2 in range(r1+1,len(self.adjMat[r1])):
                if self.adjMat[r1][r2] != 0:
                    v2 = self.adjList[r2]
                    v1.neigh.append(v2)
                    v2.neigh.append(v1)
                    e = Edge(v1,v2,self.adjMat[r1][r2])
                    self.edgeList.append(e)

        # Sort the edges.
        self.edgeList.sort()

        # Set start to the 0 ranked vertex (the first city).
        self.start = self.adjList[0]

        # Empty MST initially.
        self.mst = []

        # Empty tour initially.
        self.tour = []
        self.tourOpt = []
        return

    """
    __repr__ function to print a map.
    """
    def __repr__(self):
        # First the MST edges.
        s = ''
        s += '\nMST Edges:\n'
        w = 0
        for e in self.mst:
            s += repr(e) +'\n'
            w += e.weight
        s += '\nMST Weight:\n%f\n' % w


        # Now the tour.
        s += '\nTSP Approx. Tour:\n'
        w = 0
        if len(self.tour) > 0:
            for r in range(0,len(self.tour)-1):
                s += self.cities[self.tour[r]] + '\n'
                w += self.adjMat[self.tour[r]][self.tour[r+1]]
            s += self.cities[self.tour[0]] + '\n'
        else:
            w = math.inf
        s += '\nTSP Approx. Tour Weight:\n%f\n' % w

        # Now the optimal tour.
        s += self.optTour

        # Return the repr string.
        return s

    """
    printList function for cleanly printing the adjaceny list.
    Note: skips vertices with no neighbors.
    """
    def printList(self):
        for vertex in self.adjList:
            if len(vertex.neigh) > 0:
                print('Rank: %d' % vertex.rank)
                print('Neighbors:')
                print(vertex.neigh)
                print('')
        return

    """
    printMat function for cleanly printing the adjaceny matrix.
    Note: for the larger matrices, this will still likely be hard to read.
    """
    def printMat(self):
        for row in self.adjMat:
            print(row)
        return

    """
    printEdges function prints the edge list of the Map.
    """
    def printEdges(self):
        s = 'Edge List:\n'
        for e in self.edgeList:
            s += repr(e) +'\n'
        print(s)
        return

    """
    getMST: uses MSTalg to get the MST and fill in the edges
    """
    def getMST(self):
        # Call Prim's on the adjList and adjMat.
        # This should update all of the vertices' prev values.
        prim(self.adjList, self.adjMat)
        # Now that we've set all of the prev values, go through each vertex
        # and update its mstN list.
        for v in self.adjList:
            if not v.prev is None:
                v.mstN.append(v.prev)
                v.prev.mstN.append(v)

        # Loop through the vertices and add the MST edges.
        for rank in range(0,len(self.adjList)):
            v = self.adjList[rank]
            for neighbor in v.mstN:
                if neighbor.rank > rank:
                    e = Edge(v,neighbor,self.adjMat[rank][neighbor.rank])
                    self.mst.append(e)
        return

    """
    getTSPApprox: uses the MST to find the approximate solution to TSP.
    """
    def getTSPApprox(self):
        if len(self.mst) > 0:
            ### TODO ###
            # Complete the TSP Approximation method here
            # Update the Map object with the TSP Approximate tour
            self.tour = tsp(self.adjList, self.start)
        else:
            raise Exception('No MST set!')
        return

    """
    getTSPOptimal: brute-force approach to finding the optimal tour.
    """
    def getTSPOptimal(self):
        ### TODO ###
        # Complete a brute-force TSP solution!
        # Replace the following two lines with an actual implementation.

        final_cost = float("+inf")
        vertices_left = copy.deepcopy(self.adjList[1:])
        circuits = list(itertools.permutations(vertices_left))

        for circ in circuits:
            c = list(circ)
            c.insert(0, self.adjList[0])
            temp_cost = 0
            for i in range(len(c)):
                temp_cost += self.adjMat[c[i].rank][c[(i+1) % len(c)].rank]

            if temp_cost < final_cost:
                final_cost = temp_cost
                for i in c:
                    self.tourOpt.append(i.rank)

        return self.tourOpt

        """
        Class attributes:

        rank    # The rank of this node.
        neigh   # The list of neighbors IN THE ORIGINAL GRAPH.
        mstN    # The list of neighbors IN THE MST.
        visited # A flag for whether the vertex has been visited.
        cost    # The cost of the edge out of the tree.
        prev    # The previous vertex in the path.
        city    # The name of the associated city.
        """

    """
    clearMap: this function will reset the MST and tour for the map, along with
              all vertex info.
    """
    def clearMap(self):
        # Create the adjList of vertices
        self.adjList = []
        for rank in range(0,len(self.cities)):
            v = Vertex(rank)
            self.adjList.append(v)

        # Create the list of edges and fill the vertex.neigh values.
        # Fill in the cities while we are at it.
        self.edgeList = []
        for r1 in range(0,len(self.adjMat)):
            v1 = self.adjList[r1]
            v1.city = self.cities[r1]
            for r2 in range(r1+1,len(self.adjMat[r1])):
                if self.adjMat[r1][r2] != 0:
                    v2 = self.adjList[r2]
                    v1.neigh.append(v2)
                    v2.neigh.append(v1)
                    e = Edge(v1,v2,self.adjMat[r1][r2])
                    self.edgeList.append(e)

        # Sort the edges.
        self.edgeList.sort()

        # Set start to the 0 ranked vertex (the first city).
        self.start = self.adjList[0]

        # Empty MST initially.
        self.mst = []

        # Empty tour initially.
        self.tour = []

################################################################################
# The following functions generate test maps to run the algorithm on!

"""
getMap

This function will return the adjacency matrix and city names for the map.

INPUTS
mapNum: the number of which map to select.

OUTPUTS
adjMat:   the adjacency matrix.
cityList: the list of the cities.
optTour:  string of the optimal tour.
optList:  array of the optimal tour (each city is denoted by their rank: their numbering in cityList).
"""
def getMap(mapNum=0):
    if mapNum == 0:
        cityList = ['a','b','c','d']
        adjMat = [[0,2,8,5],\
                  [2,0,7,4],\
                  [8,7,0,6],\
                  [5,4,6,0]]
        optTour = '\nOptimal Tour:' + \
                  '\na\nb\nc\nd\na\n\nWeight of Optimal Tour:\n20'
        optList = [0,1,2,3,0]
        return adjMat, cityList, optTour, optList

    elif mapNum == 1:
        cityList = ['a','b','c','d']
        adjMat = [[0,2,2,3],\
                  [2,0,3,2],\
                  [2,3,0,2],\
                  [3,2,2,0]]
        optTour = '\nOptimal Tour:' + \
                  '\na\nb\nd\nc\na\n\nWeight of Optimal Tour:\n8'
        optList = [0,1,3,2,0]
        return adjMat, cityList, optTour, optList


    elif mapNum == 2:
        cityList = ['NYC','Urbandale','Chicago','Durham','LA','Seattle',\
                    'Washington DC']
        lats = [40.71,41.63,41.88,35.99,34.05,47.61,38.91]
        longs = [74.01,93.71,87.63,78.90,118.24,122.33,77.04]
        optTour = '\nOptimal Tour:\nNYC\nChicago\nUrbandale\nSeattle\nLA' + \
                  '\nDurham\nWashington DC\nNYC\n\nWeight of Optimal ' + \
                  'Tour:\n9796'
        optList = [0,2,1,5,4,3,6,0]

    elif mapNum == 3:
        cityList = ['London','Paris','Madrid','Rome','Berlin','Istanbul',\
                    'Moscow','Athens','Copenhagen']
        lats = [51.51,48.86,40.42,41.90,52.52,41.01,55.76,37.98,55.68]
        longs = [0.13,-2.35,3.70,-12.50,-13.41,-28.98,-37.62,-23.73,-12.57]
        optTour = '\nOptimal Tour:\nLondon\nBerlin\nCopenhagen\nMoscow\n' + \
                  'Istanbul\nAthens\nRome\nMadrid\nParis\nLondon\n\nWeight ' + \
                  'of Optimal Tour:\n8978'
        optList = [0,4,8,6,5,7,3,2,1,0]

    elif mapNum == 4:
        cityList = ['NYC','Urbandale','Chicago','Durham','LA','Seattle',\
                    'Washington DC','Houston','Phoenix','Denver',\
                    'San Francisco','Honolulu','Boston','Cleveland']
        lats = [40.71,41.63,41.88,35.99,34.05,47.61,38.91,\
                29.76,33.45,39.74,37.77,21.31,42.36,41.50]
        longs = [74.01,93.71,87.63,78.90,118.24,122.33,77.04,\
                 95.37,112.07,104.99,122.42,157.86,71.06,81.69]
        optTour = '\nOptimal Tour: ?'
        optList = []

    elif mapNum == 5:
        cityList = ['London','Paris','Madrid','Rome','Berlin','Istanbul',\
                    'Moscow','Athens','Copenhagen','Dublin','Warsaw',\
                    'Kiev']
        lats = [51.51,48.86,40.42,41.90,52.52,41.01,55.76,37.98,55.68,\
                53.35,52.23,50.45]

        longs = [0.13,-2.35,3.70,-12.50,-13.41,-28.98,-37.62,-23.73,-12.57,\
                 6.26,-21.01,-30.52]
        optTour = '\nOptimal Tour:\nLondon\nParis\nMadrid\nRome\nAthens\n' + \
                  'Istanbul\nKiev\nMoscow\nWarsaw\nBerlin\nCopenhagen\n' + \
                  'Dublin\nLondon\n\nWeight of Optimal Tour:\n9911'
        optList = []

    elif mapNum == 6:
        cityList = ['London','Paris','Madrid','Rome','Berlin','Istanbul',\
                    'Moscow','Athens','Copenhagen','Dublin','Warsaw',\
                    'Kiev','St. Petersburg','Stockholm']
        lats = [51.51,48.86,40.42,41.90,52.52,41.01,55.76,37.98,55.68,\
                53.35,52.23,50.45,59.93,59.33]
        longs = [0.13,-2.35,3.70,-12.50,-13.41,-28.98,-37.62,-23.73,-12.57,\
                 6.26,-21.01,-30.52,-30.34,-18.07]
        optTour = '\nOptimal Tour: ?'
        optList = []

    elif mapNum == 7:
        N = 75
        cityList = []
        lats = []
        longs = []
        lab = 0
        for ind in range(0,N+1):
            cityList.append(str(lab))
            lats.append(ind*180/N-90)
            longs.append(-10)
            lab += 1
        for ind in range(1,N-1):
            cityList.append(str(lab))
            lats.append(90-ind*180/N)
            longs.append(170)
            lab += 1
        antiPolar = -(lats[0]+lats[-1])/2
        lats.append(antiPolar)
        longs.append(-10)
        cityList.append(str(lab))
        optTour = '\nOptimal Tour: 40030.173592'
        optList = []

    elif mapNum == 8:
        N = 75
        cityList = []
        lats = []
        longs = []
        lab = 0
        for ind in range(0,N+1):
            cityList.append(str(lab))
            lats.append(ind*180/N-90)
            longs.append(-10)
            lab += 1
        for ind in range(1,N-1):
            cityList.append(str(lab))
            lats.append(90-ind*180/N)
            longs.append(170)
            lab += 1
        antiPolar = -(lats[0]+lats[-1])/2
        lats.insert(0,antiPolar)
        longs.insert(0,-10)
        cityList.insert(0,str(lab))
        optTour = '\nOptimal Tour: 40030.173592'
        optList = []

    else:
        raise Exception('Not a valid map number.')

    # Get the distances and insert into the adjacency matrix.
    adjMat = [[0 for x in range(0,len(cityList))] \
              for x in range(0,len(cityList))]
    for r in range(0,len(adjMat)):
        for c in range(r+1,len(adjMat[r])):
            adjMat[r][c] = getDist(lats[r],longs[r],lats[c],longs[c])
            adjMat[c][r] = adjMat[r][c]
        adjMat[r][r] = 0

    return adjMat, cityList, optTour, optList

################################################################################

"""
getDist

This function takes in two coordinates and returns the distance between them
(in kilometers).

INPUTS
lat1, long1: the latitude and longitude of the first city.
lat2, long2: the latitude and longitude of the second city.

OUTPUTS
dist: the distance between the two cities (km).
"""
def getDist(lat1,long1,lat2,long2):
    # Convert to radians.
    lat1 = lat1*math.pi/180
    long1 = long1*math.pi/180
    lat2 = lat2*math.pi/180
    long2 = long2*math.pi/180

    # Calculate the change in lat and long.
    dLat = lat2 - lat1
    dLong = long2 - long1

    # Set the radius of the Earth.
    R = 6371 # km

    # Calculate the distance using the formula for distance on a great circle.
    a = math.sin(dLat/2)**2 \
        + \
        ( \
          math.cos(lat1)*math.cos(lat2) \
          * \
          math.sin(dLong/2)**2 \
        )
    if abs(a) < 1e-15: a = 0
    if abs(1-a) < 1e-15: a = 1
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist = R*c
    return dist # km

################################################################################

"""
testMSTApprox

This function will test your code on the various maps using the input alg.

INPUTS
alg: 'Prim' or 'Kruskal'

OUTPUTS
s: a string indicating number of tests passed.
"""
def testMSTApprox():
    Mpass = 0
    Tpass = 0
    Mflag = False
    Tflag = False
    t = 9
    tol = 1e-6

    # Test MST approximation of Metric TSP.
    MSTws = [12,6,5999.977279,6909.105275,11810.893206,7724.194671,\
             8813.919553,39763.305768,39763.305768]
    for ind in range(0,t):
        MSTw = MSTws[ind]
        m = Map(ind)
        m.getMST()
        if len(m.mst) < len(m.cities)-1:
            print('Test %d: Not enough edges in MST.' % ind)
            Mflag = True
        if len(m.mst) > len(m.cities)-1:
            print('Test %d: Too many edges in MST.' % ind)
            Mflag = True
        w = 0
        for e in m.mst:
            w += e.weight
        if w < MSTw-tol:
            print('Test %d: MST weight too low.' % ind)
            Mflag = True
        if w > MSTw+tol:
            print('Test %d: MST weight too high.' % ind)
            Mflag = True
        if not Mflag:
            m.getTSPApprox()
            w = 0
            if len(m.tour) > 0:
                for r in range(0,len(m.tour)-1):
                    w += m.adjMat[m.tour[r]][m.tour[r+1]]
            else:
                w = math.inf
            if len(m.tour) != len(m.cities)+1:
                print('Test %d: TSP should be length %d.' % (ind,len(m.cities)+1))
                Tflag = True
            if w == math.inf:
                print('Test %d: No TSP reported.' % ind)
                Tflag = True
            else:
                if w > 2*MSTw+2*tol:
                    print('Test %d: TSP too large.' % ind)
                    Tflag = True
                if w <= MSTw-tol:
                    print('Test %d: TSP too small.' % ind)
                    Tflag = True
            if m.tour[0] != m.tour[-1]:
                print('Test %d: TSP start != end.' % ind)
                Tflag = True
            for c in range(1,len(m.tour)):
                city = m.tour[c]
                if city in m.tour[c+1:]:
                    print('Test %d: Repeated City in TSP.' % ind)
                    Tflag = True
            if ind == 7:
                ans = 40030.173592
                ans2 = 78992.875888
                flag_left = False
                flag_right = False
                if (w < ans - tol) or (w > ans + tol):
                    print('Test %d: Wrong TSP (when traversing the tree via DFS from left to right)!' % ind)
                    flag_left = True
                if (w < ans2 - tol) or (w > ans2 + tol):
                    print('Test %d: Wrong TSP (when traversing the tree via DFS from right to left)!' % ind)
                    flag_right = True
                if flag_left and flag_right:
                    print("[FAILED} Test %d: Wrong TSP considering both directions of DFS traversal" % ind)
                    Tflag = True
                if (flag_left or flag_right) and not Tflag:
                    print("Test %d still passed." % ind)
            if ind == 8:
                ans = 79526.611536
                ans2 = 78992.875888
                flag_left = False
                flag_right = False
                if (w < ans - tol) or (w > ans + tol):
                    print('Test %d: Wrong TSP (when traversing the tree via DFS from left to right)!' % ind)
                    flag_left = True
                if (w < ans2 - tol) or (w > ans2 + tol):
                    print('Test %d: Wrong TSP (when traversing the tree via DFS from right to left)!' % ind)
                    flag_right = True
                if flag_left and flag_right:
                    print("[FAILED} Test %d: Wrong TSP considering both directions of DFS traversal" % ind)
                    Tflag = True
                if (flag_left or flag_right) and not Tflag:
                    print("Test %d still passed." % ind)
        else:
            Tflag = True
        if not Mflag:
            Mpass += 1
        if not Tflag:
            Tpass += 1

    s = 'Passed %d/%d MST Tests and %d/%d TSP Tests.' \
        % (Mpass,t,Tpass,t)
    return s

################################################################################

"""
test2approx

This function will test your code on the various maps using the input alg.

INPUTS
None.

OUTPUTS
s: a string indicating number of tests passed.
"""
def test2approx():
    passed = 0
    t = 4
    tol = 1e-6

    # Check if the approximate solution is a 2-approximation.
    for ind in range(0,t):
        m = Map(ind)
        m.getMST()
        m.getTSPApprox()
        wA = 0
        for r in range(0,len(m.tour)-1):
            wA += m.adjMat[m.tour[r]][m.tour[r+1]]

        m.getTSPOptimal()
        wO = 0
        for r in range(0,len(m.tourOpt)-1):
            wO += m.adjMat[m.tourOpt[r]][m.tourOpt[r+1]]

        if wA <= 2*wO:
            passed += 1

    s = 'Passed %d/%d 2-approximation tests.' \
        % (passed,t)
    return s

################################################################################
# Here, we run the tests!
# You want to pass 9/9 MST & TSP tests (which will happen if your implementation is correct).
# You also want to pass 4/4 2-approximation tests (which will happen if ...)!

# Build MST with Prim's Algorithm, then find the approximate solution to the TSP problem.
# Print the results.
s = testMSTApprox()
print(s)

# Check if the MST approximation approach is a 2-approximation of the optimal solution.
# In interest of time, only test on the first four maps.
s = test2approx()
print(s)
