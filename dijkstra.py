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

class Dijkstra(Graph):
    '''
    Graph class with naive_dijkstra and priority_dijkstra_method
    '''
    def __init__(self, **attrs):           #constructor method
        Graph.__init__(self, **attrs)

    def naive_dijkstra(self, source):    
        sourceneighbors = self.get_out_neighbors
        S = []
        Sbar = self.get_node_list()
        n = len(Sbar)
        d = {}
        for k in Sbar:
            d[k] = MAXINT
        d[source] = 0
        pred = {}
        pred[source] = None
        while len(S)<n:
            # find the min d[i] in Sbar and get i
            i = Sbar[-1]
            for k in Sbar:
                if d[i]>d[k]:
                    i = k
            # end
            S.append(i)
            Sbar.remove(i)
            for j in sourceneighbors(i):
                cij = self.get_edge_attr(i,j,'cost')
                if d[j] > d[i] + cij:
                    d[j] = d[i] + cij
                    pred[j] = i
        self.naive_dijkstra_pred = pred
        self.naive_dijkstra_d = d

    def priority_dijkstra(self, source):
        sourceneighbors = self.get_out_neighbors
        S = []
        Sbar = PriorityQueue()
        n = len(self.get_node_list())
        for k in self.get_node_list():
            Sbar.push(k, MAXINT)
        d = {}
        for k in self.get_node_list():
            d[k] = MAXINT
        d[source] = 0
        Sbar.push(source, 0)
        pred = {}
        pred[source] = None
        while len(S)<n:
            # find the min d[i] in Sbar and get i
            i = Sbar.pop()
            # end
            S.append(i)
            for j in sourceneighbors(i):
                cij = self.get_edge_attr(i,j,'cost')
                if d[j] > d[i] + cij:
                    d[j] = d[i] + cij
                    Sbar.push(j, d[j])
                    pred[j] = i
        self.priority_dijkstra_pred = pred
        self.priority_dijkstra_d = d

# test parameters
NODE = [10, 20, 50, 70, 100, 150]
#NODE = [10, 20]
#DENSITY = [0.5, 0.7, 1]
DENSITY = [0.2, 0.3, 0.4, 0.5]
SEED_INPUT = [0, 1]
LENGTH_RANGE = [10,50]

if __name__ == '__main__':
    '''
    compare naive_dijkstra and priority_dijkstra empirically.
    '''
    naive_result = open('naive_dijkstra.txt','w')
    priority_result = open('priority_dijkstra.txt','w')
    for f in [naive_result, priority_result]:
        f.write('# Node    : '+ NODE.__str__()+'\n')
        f.write('# Density : '+ DENSITY.__str__()+'\n')
        f.write('# Seed    : '+ SEED_INPUT.__str__()+'\n')
        f.write('# Node Density Seed Time Elapsed\n')

    for n in NODE:
        for d in DENSITY:
            for s in SEED_INPUT:
                g = Dijkstra()
                g.random(numnodes=n, density=d, length_range=LENGTH_RANGE, seedInput=s)
                # measure time elapsed for naive dijkstra
                start = time.clock()
                g.naive_dijkstra('0')
                elapsed_time = time.clock() - start
                naive_result.write(str(n).ljust(5)+('%.2f'%d).ljust(8)+str(s).ljust(5)+str(elapsed_time)+'\n')
                # measure time elapsed for priority dijkstra
                start = time.clock()
                g.priority_dijkstra('0')
                elapsed_time = time.clock() - start
                priority_result.write(str(n).ljust(5)+('%.2f'%d).ljust(8)+str(s).ljust(5)+str(elapsed_time)+'\n')
    naive_result.close()
    priority_result.close()
    cProfile.run("print g.naive_dijkstra('0')",'naivedijkstraproof')
    cProfile.run("print g.priority_dijkstra('0')", 'prioritydijkstraproof')
    p = pstats.Stats('naivedijkstraproof')
    q = pstats.Stats('prioritydijkstraproof')
    p.sort_stats('time', 'cum')
    p.print_stats()
    q.sort_stats('time', 'cum')
    q.print_stats()