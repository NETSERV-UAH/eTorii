#!/usr/bin/python
'''
Copyright 2015 gistnetserv-uah

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
# TODO: full explanation
import os
from random import seed, randrange
from priodict import priorityDictionary

# BEGIN OF DIJKSTRA CODE

def Dijkstra(G,start,end=None):
	"""
	Find shortest paths from the start vertex to all
	vertices nearer than or equal to the end.

	The input graph G is assumed to have the following
	representation: A vertex can be any object that can
	be used as an index into a dictionary.  G is a
	dictionary, indexed by vertices.  For any vertex v,
	G[v] is itself a dictionary, indexed by the neighbors
	of v.  For any edge v->w, G[v][w] is the length of
	the edge.  This is related to the representation in
	<http://www.python.org/doc/essays/graphs.html>
	where Guido van Rossum suggests representing graphs
	as dictionaries mapping vertices to lists of neighbors,
	however dictionaries of edges have many advantages
	over lists: they can store extra information (here,
	the lengths), they support fast existence tests,
	and they allow easy modification of the graph by edge
	insertion and removal.  Such modifications are not
	needed here but are important in other graph algorithms.
	Since dictionaries obey iterator protocol, a graph
	represented as described here could be handed without
	modification to an algorithm using Guido's representation.

	Of course, G and G[v] need not be Python dict objects;
	they can be any other object that obeys dict protocol,
	for instance a wrapper in which vertices are URLs
	and a call to G[v] loads the web page and finds its links.
	
	The output is a pair (D,P) where D[v] is the distance
	from start to v and P[v] is the predecessor of v along
	the shortest path from s to v.
	
	Dijkstra's algorithm is only guaranteed to work correctly
	when all edge lengths are positive. This code does not
	verify this property for all edges (only the edges seen
 	before the end vertex is reached), but will correctly
	compute shortest paths even for some graphs with negative
	edges, and will raise an exception if it discovers that
	a negative edge has caused it to make a mistake.
	"""

	D = {}	# dictionary of final distances
	P = {}	# dictionary of predecessors
	Q = priorityDictionary()   # est.dist. of non-final vert.
	Q[start] = 0
	
	for v in Q:
		D[v] = Q[v]
		if v == end: break
		
		for w in G[v]:
			vwLength = D[v] + G[v][w]
			if w in D:
				if vwLength < D[w]:
					raise ValueError, \
  "Dijkstra: found better path to already-final vertex"
			elif w not in Q or vwLength < Q[w]:
				Q[w] = vwLength
				P[w] = v
	
	return (D,P)
			
def shortestPath(G,start,end):
	"""
	Find a single shortest path from the given start vertex
	to the given end vertex.
	The input has the same conventions as Dijkstra().
	The output is a list of the vertices in order along
	the shortest path.
	"""

	D,P = Dijkstra(G,start,end)
	Path = []
	while 1:
		Path.append(end)
		if end == start: break
		end = P[end]
	Path.reverse()
	return Path

# END OF DIJKSTRA CODE

# MAIN FUNCTION

def hierDataCenter():
    print
    print 'Builds T arbitrary hierarchical DC topologies of nL levels of switches,'
    print 'nLi nodes at level Li, lLi links between level Li and Li+1'
    print 'nH hosts (end systems) single connected to a nLth level switch'
    print '-----------------------------------------------------------------------'

# constant def
    MAX_TOP = 100
    MIN_TOP = 1
    MAX_HIERARCH = 9
    MIN_HIERARCH = 2
    MAX_NODESxLEVEL = 1000
    MIN_NODESxLEVEL = 1
    MAX_LINKSxLEVEL = 2000
    MAX_HOSTS = 100000

# Argument capture loops
    maxV = MAX_TOP
    minV = MIN_TOP
    nT = int(raw_input('Number of Topologies [nT: ' + str(minV) + '..' + str(maxV) + ']: '))
    while ((nT < minV) or (nT > maxV)):
        nT = int(raw_input('Number of Topologies [nT: ' + str(minV) + '..' + str(maxV) + ']: '))

    maxV = MAX_HIERARCH
    minV = MIN_HIERARCH
    nL = int(raw_input('Number of Hierarchical levels [nL: ' + str(minV) + '..' + str(maxV) + ']: '))
    while ((nL < minV) or (nL > maxV)):
        nL = int(raw_input('Number of Hierarchical levels [nL: ' + str(minV) + '..' + str(maxV) + ']: '))

    maxV = MAX_NODESxLEVEL
    minV = MIN_NODESxLEVEL
    nLi=[]
    for i in range(nL):
        nn = int(raw_input('Number of nodes at level-> '+ str(i) + ' [nL'+str(i)+': ' + str(minV) + '..' + str(maxV) + ']: '))
        while ((nn < minV) or (nn > maxV)):
            nn = int(raw_input('Number of nodes at level-> '+ str(i) + ' [nL'+str(i)+': ' + str(minV) + '..' + str(maxV) + ']: '))
        nLi.append(nn) 

    maxV = MAX_LINKSxLEVEL
    dlLi=[]
    for i in range(nL-1):
        if (i==0): 
            minV = max(2*nLi[0], nLi[1])
        else:
            minV = max(nLi[i], nLi[i+1])
        nl = int(raw_input('Number of links down from level-> '+ str(i) + ' [dlL'+str(i)+': '+ str(minV) + '..' + str(maxV) + ']: '))
        while ((nl < minV) or (nl > maxV)):
            nl = int(raw_input('Number of links down from level-> '+ str(i) + ' [dlL'+str(i)+': '+ str(minV) + '..' + str(maxV) + ']: '))
        dlLi.append(nl)

    maxV = MAX_HOSTS
    minV = nLi[nL-1]
    nH = 0
    nh = int(raw_input('Number of hosts [nH: '  + str(minV) + '..' + str(maxV) + ']: '))
    while ((nh < minV) or (nh > maxV)):
        nh = int(raw_input('Number of hosts [nH: '  + str(minV) + '..' + str(maxV) + ']: '))
    nH = nh 

    print
    print 'Number of topologies: ', nT
    print 'Levels per topology: ', nL
    print 'Nodes at every level: ', nLi
    print 'Down links at each level: ', dlLi
    print 'Number of hosts: ', nH

    generatedNets = 0       # Number of genrated topologies
    checkedNets = 0         # Number of checked topologies (continuity check)
    
    while checkedNets < nT:
        #set output filename
        name = 'hDC_' + 'nL-' + str(nL) + '_nLi'
        for j in range(len(nLi)):
            name += '-' + str(nLi[j])
        name += '_dlLi'
        for j in range(len(dlLi)):
            name += '-' + str(dlLi[j]) 
        name +=  '_nH' + str(nH) 
        name +=  '_n' + str(generatedNets) 
        path = os.getcwd() + '/topo'
        fn = path + '/'+ name +'.top'
        print 'Archivo de salida:', fn
        print
        
        #set random seed
        seed(generatedNets)
        
        # Creates a new topology and checks it for continuity
        if generateDCtop(nL,nLi,dlLi,nH,fn,generatedNets): checkedNets += 1
        generatedNets += 1


def generateDCtop(nl, nli, dli, nh, fn, s):
    # nl, number of levels
    # nli, number of nodes at each level
    # dli, number of down-links at each level
    # nh, number of hosts
    # fn, filename 
    # s, random seed

    """
    Creates a new topology and checks it for continuity.
    Returns the check result
    """

    
    # creates the list of nodes (switches or hosts) at every level
    nodesPerLevelList = [] 
    for i in range(nl):
        nodesPerLevelList.append(createListOfNodesAtLevel(nli[i], i))
        if VERBOSE: print nodesPerLevelList[i]
    
    nodesPerLevelList.append(createListOfHosts(nh))
    
    net = {}            # the new topology
    for i in range(nl+1):
        for item in nodesPerLevelList[i]:
            net[item] = {}
     
    f = open(fn, 'w')   

    # For each interface between two levels (starts from level 0)  
    for i in range(nl-1):
        # nodes at the upper level
        availNodesAtLevel = list(nodesPerLevelList[i])
        if (i==0): availNodesAtLevel.extend(nodesPerLevelList[i])
        
        # nodes at the lower level
        availNodesAtLevelBelow = list(nodesPerLevelList[i+1])
        availNodesAtLevelBelowPerUpNode = {}
        for item in availNodesAtLevel:
            availNodesAtLevelBelowPerUpNode[item] = list(nodesPerLevelList[i+1])
        
        # For each link at the interface
        for k in range(dli[i]):
            # chooese upper level node
            if len(availNodesAtLevel) > 0:
                idx = randrange(len(availNodesAtLevel))
                upNode = availNodesAtLevel.pop(idx)
            else:
                idx = randrange(len(nodesPerLevelList[i]))
                upNode = nodesPerLevelList[i][idx]

            if VERBOSE: print str(upNode), 

            # choose lower level node
            if len(availNodesAtLevelBelow) > 0:
                idx = randrange(len(availNodesAtLevelBelow)) 
                downNode = availNodesAtLevelBelow.pop(idx)
                availNodesAtLevelBelowPerUpNode[upNode].remove(downNode)
            else:
                idx = randrange(len(availNodesAtLevelBelowPerUpNode[upNode]))
                downNode = availNodesAtLevelBelowPerUpNode[upNode][idx]
                availNodesAtLevelBelowPerUpNode[upNode].remove(downNode)

            if VERBOSE: print str(downNode),            
            if VERBOSE: print str(upNode) + '-' + str(downNode)
            
            # add link to network
            net[upNode][downNode] = 1000
            net[downNode][upNode] = 1000
            
            line = '$topJAC duplex-link $n(' + str(upNode) + ') $n(' + str(downNode) + ')\n'
            f.write(line)

        if VERBOSE: print net 
    
    # assign hosts to lowest level of switches
    availNodesAtLevelAbove = list(nodesPerLevelList[nl-1])
    for i in range(nh):
        if len(availNodesAtLevelAbove) > 0:
            idx = randrange(len(availNodesAtLevelAbove))
            upNode = availNodesAtLevelAbove.pop(idx)
        else:
            idx = randrange(len(nodesPerLevelList[nl-1]))
            upNode = nodesPerLevelList[nl-1][idx]
        if VERBOSE: print 'un = ', str(upNode),

        downNode =  nodesPerLevelList[nl][i]
        if VERBOSE: print 'dn = ', str(downNode),
            
        if VERBOSE: print str(upNode) + '-' + str(downNode)
            
        net[upNode][downNode] = 1000
        net[downNode][upNode] = 1000
            
        line = '$topJAC duplex-link $n(' + str(upNode) + ') $n(' + str(downNode) + ')\n'
        f.write(line)
    
    f.close()
        
    # check for Network Continuity
    check = checkNetworkContinuity(nodesPerLevelList[nl-1], net)
    
    # if check fails discard new topology
    if not check: os.remove(fn)
    
    return check
    
def checkNetworkContinuity(nodeList, netMatrix): 
    # nodeList, the switches at the last level
    # netMatrix, the whole topology
    
    continuityCheck = True
    
    sourcesAlreadyCheckedList = [] 
    for i in nodeList:
        if not continuityCheck: break
        sourcesAlreadyCheckedList.append(i)
        destinationsToCheckList = list(nodeList)
        for j in sourcesAlreadyCheckedList:
            destinationsToCheckList.remove(j)
        
        print 'Source: ', i
        for j in destinationsToCheckList:
            Dist, Predec = Dijkstra(netMatrix, i, j)
            if j in Dist:
                path = []
                prevNode = j
                while prevNode in Predec:
                    path.append(prevNode)
                    prevNode = Predec[prevNode]
                path.append(i)
                path.reverse()
                if VERBOSE: print '        Destination: ', j, 'found,  Distance= ', Dist[j], ',  Route: ', path
                continuityCheck = checkPath(path)
            else: 
                continuityCheck = False
                print '        Destination: ', j, 'not found'
            if not continuityCheck: break
    
    return continuityCheck
    
def checkPath(p):
    # p, path to be checked, a list of nodes
    # a given path p is allowed if and only if ir goes always up to a node 
    # and then always down to the destination
    
    path2check = list(p)
    #print path2check
    pathOk = True
    if path2check[0] > path2check[1]: direction = 'Up'
    else: pathOk = False
    path2check.pop(0)
    #print path2check
    while pathOk and len(path2check) > 1:
        if path2check[0] > path2check[1]: 
            newDirection = 'Up'
        else: 
            newDirection = 'Down'
        path2check.pop(0)        
        if direction == 'Up': 
            direction = newDirection
        elif direction == 'Down':
            if newDirection == 'Up': pathOk = False
    if VERBOSE:
        if pathOk: print 'Path: ', p, ' is Ok'
        else: print 'Path: ', p, ' does zigzag (forbidden)'
        
    return pathOk
        
def createListOfNodesAtLevel(nn, l):
    # nn, number of nodes
    # l, level
    
    nList = []
    for i in range(nn):
        nList.append(str(l) + 's' + str(i))
    return nList

def createListOfHosts(nn):
    # nn, number of hosts
    
    nList = []
    for i in range(nn):
        nList.append('h' + str(i))
    return nList


# BEGIN MAIN LOOP, ASK FOR TYPE OF TOPOLOGY TO BUILD....

# Constant def: control full trace of code
VERBOSE = True

print
print 'Builds arbitrary datacenter topologies:'
print '    [1] Hierarchical' 
#print '    [2] Malla cubica' 
#print '    [3] Hyper cubo de grados 4 a 7' 
print 

while True:
    sel = int(raw_input('Select[1, [0 to abort]]: '))
    while ((sel < 0) or (sel > 1)):
        sel = int(raw_input('Select [1, [0 to abort]]: '))
    if sel == 1:
        hierDataCenter()
    if sel == 0:
        break
