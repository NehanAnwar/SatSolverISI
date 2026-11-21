from argparse import ArgumentParser
import subprocess


class Graph:
    def __init__(self,id):
        self.ID = id
        self.VerticeCount = 0
        self.Vertices = []
        self.Edges = {} # Adjacency list of edges




def load_instance(input_file_name):
    # read the input instance
    # the instance is The vertice count in G1, Edge count in G1, Vertice count in G2, Edge count in G2
    # Edge set of G1
    # Edge set of G2

    g1 = Graph(1)
    g2 = Graph(2)
    with open(input_file_name, "r") as file:

        g1.Vertices = [int(x) for x in next(file).split()] # Reads Vertices of Graph 1
        g2.Vertices = [int(x) for x in next(file).split()] # Reads Vertices of Graph 2

        for line in file: # Reads Edge set of G1
            
            if line.removesuffix("\n") == "#####":
                break
            line = line.split()
            if line:
                line = [int(i) for i in line]
                if line[0] in g1.Edges.keys():
                    g1.Edges[line[0]].append(line[1])
                else:
                    g1.Edges[line[0]] = [line[1]]
                if line[1] in g1.Edges.keys():
                    g1.Edges[line[1]].append(line[0])
                else:
                    g1.Edges[line[1]] = [line[0]]


        for line in file: # Reads Edge set of G2

            if line == "#####":
                break
            line = line.split()
            if line:
                line = [int(i) for i in line]
                if line[0] in g2.Edges.keys():
                    g2.Edges[line[0]].append(line[1])
                else:
                    g2.Edges[line[0]] = [line[1]]

                if line[1] in g2.Edges.keys():

                    g2.Edges[line[1]].append(line[0])
                else:
                    g2.Edges[line[1]] = [line[0]]

        g1.VerticeCount = len(g1.Vertices)
        g2.VerticeCount = len(g2.Vertices)

        if g2.VerticeCount < g1.VerticeCount:
            raise Exception("Vertices in pattern cannot be greater than Vertices in host")

    print(f"{g1.Vertices} \n\n {g2.Vertices}")
    print(f"{g1.Edges}\n\n{g2.Edges}")
    return g1,g2


def var(i,a,host_count):
    #  vertex i in pattern -> vertex a in Host
    return i * host_count + a + 1

def encode(pattern_graph, host_graph):

    clauses = []
    k = pattern_graph.VerticeCount
    n = host_graph.VerticeCount

        


Pattern,Host = load_instance("test.in")