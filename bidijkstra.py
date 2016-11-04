from gimpy import Graph
from Queues import PriorityQueue
import pdb
import sys
import time
import cProfile
import pstats
__author__ = 'Onur Babat'
__email__  = 'onur.babat@lehigh.edu'

MAXINT = sys.maxint

class Bidijkstra(Graph):
    '''
    Graph class with naive_dijkstra and priority_dijkstra_method and reverse dijkstra
    '''
    def __init__(self, **attrs):
        Graph.__init__(self, **attrs)
    
    def intersect(self,a,b):
        return list(set(a) & set(b))

    def naive_bidijkstra(self, source, sink):
        sourceneighbors = self.get_out_neighbors
        sinkneighbors=self.get_in_neighbors #incoming arcs are neighbors of the sink
        S = []                                    
        T = []                                  #T is the version of S in reverse dijksta
        Sbar = self.get_node_list()
        Tbar = self.get_node_list()             #Tbar is the version of Sbar in reverse dijkstra
        d = {}
        e = {}
        for k in Sbar:
            d[k] = MAXINT
        for l in Tbar:
            e[l] = MAXINT
        d[source] = 0
        e[sink] = 0
        pred = {}
        succ = {}
        pred[source] = None
        succ[sink] = None
        while len(self.intersect(S,T))==0:
            # find the min d[i] in Sbar and get i
            i = Sbar[-1]
            for k in Sbar:
                if d[i]>d[k]:
                    i = k
            # end
            # find the min e[q] in Tbar and get l
            q = Tbar[0]
            for l in Tbar:
                if e[q]>e[l]:
                    q = l
            # end        
            S.append(i)
            T.append(q)
            Sbar.remove(i)
            Tbar.remove(q)
            for j in sourceneighbors(i):
                cij = self.get_edge_attr(i,j,'cost')
                if d[j] > d[i] + cij:
                    d[j] = d[i] + cij
                    pred[j] = i
            for p in sinkneighbors(q):
                cpq=self.get_edge_attr(p,q,'cost')
                if e[p] > e[q] + cpq:
                    e[p] = e[q] + cpq
                    succ[p] = q
        self.naive_bidijkstra_pred = pred
        self.naive_bidijkstra_succ = succ
        self.naive_bidijkstra_d = d
        self.naive_bidijkstra_e = e

    def priority_bidijkstra(self, source, sink):
        sourceneighbors = self.get_out_neighbors
        sinkneighbors = self.get_in_neighbors
        S = []
        T = []                                  #T is the version of S in reverse dijksta
        Sbar = PriorityQueue()
        Tbar = PriorityQueue()                  #Tbar is the version of Sbar in reverse dijkstra
        for k in self.get_node_list():
            Sbar.push(k, MAXINT)
        for l in self.get_node_list():
            Tbar.push(l, MAXINT)
        d = {}
        e = {}
        for k in self.get_node_list():
            d[k] = MAXINT
        for l in self.get_node_list():
            e[l] = MAXINT
        d[source] = 0
        e[sink] = 0
        Sbar.push(source, 0)
        Tbar.push(sink, 0)
        pred = {}
        succ = {}
        pred[source] = None
        succ[sink] = None
        while len(self.intersect(S,T))==0:
            # find the min d[i] in Sbar and get i
            i = Sbar.pop()
            # end
            # find the min e[q] in Tbar and get q
            q = Tbar.pop()
            # end
            S.append(i)
            T.append(q)
            for j in sourceneighbors(i):
                cij = self.get_edge_attr(i,j,'cost')
                if d[j] > d[i] + cij:
                    d[j] = d[i] + cij
                    Sbar.push(j, d[j])
                    pred[j] = i
            for p in sinkneighbors(q):
                cpq = self.get_edge_attr(p,q,'cost')
                if e[p] > e[q] + cpq:
                    e[p] = e[q] + cpq
                    Tbar.push(p, e[p])
                    succ[p] = q
        self.priority_bidijkstra_pred = pred
        self.priority_bidijkstra_d = d
        self.priority_bidijkstra_succ = succ
        self.priority_bidijkstra_e = e
        
# test parameters
NODE = [10, 20, 50, 70, 100, 150]
#NODE = [10, 20]
#DENSITY = [0.5, 0.7, 1]
DENSITY = [0.2, 0.3, 0.4, 0.5]
SEED_INPUT = [0, 1]
LENGTH_RANGE = [10,50]

if __name__ == '__main__':
    '''
    compare naive_bidijkstra and priority_bidijkstra empirically.
    '''
    naive_result = open('naive_bidijkstra.txt','w')
    priority_result = open('priority_bidijkstra.txt','w')
    for f in [naive_result, priority_result]:
        f.write('# Node    : '+ NODE.__str__()+'\n')
        f.write('# Density : '+ DENSITY.__str__()+'\n')
        f.write('# Seed    : '+ SEED_INPUT.__str__()+'\n')
        f.write('# Node Density Seed Time Elapsed\n')

    for n in NODE:
        for d in DENSITY:
            for s in SEED_INPUT:
                g = Bidijkstra()
                g.random(numnodes=n, density=d, length_range=LENGTH_RANGE, seedInput=s)
                # measure time elapsed for naive bidijkstra
                start = time.clock()
                g.naive_bidijkstra('0', n-1)
                elapsed_time = time.clock() - start
                naive_result.write(str(n).ljust(5)+('%.2f'%d).ljust(8)+str(s).ljust(5)+str(elapsed_time)+'\n')
                # measure time elapsed for priority bidijkstra
                start = time.clock()
                g.priority_bidijkstra('0', n-1)
                elapsed_time = time.clock() - start
                priority_result.write(str(n).ljust(5)+('%.2f'%d).ljust(8)+str(s).ljust(5)+str(elapsed_time)+'\n')
    naive_result.close()
    priority_result.close()
    cProfile.run("print g.naive_bidijkstra('0', n-1)",'naivebidijkstraproof')
    cProfile.run("print g.priority_bidijkstra('0', n-1)", 'prioritybidijkstraproof')
    p = pstats.Stats('naivebidijkstraproof')
    q = pstats.Stats('prioritybidijkstraproof')
    p.sort_stats('time', 'cum')
    p.print_stats()
    q.sort_stats('time', 'cum')
    q.print_stats()
    
