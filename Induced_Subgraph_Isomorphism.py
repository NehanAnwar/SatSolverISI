from argparse import ArgumentParser

def load_instance(input_file_name):
    # read the input instance
    # the instance is The vertice count in G1, Edge count in G1, Vertice count in G2, Edge count in G2
    # Edge set of G1
    # Edge set of G2
    class Graph():
        V = []
        E = {} # Adjacency list of edges


    global V1, E1, V2, E2
    g1 = Graph()
    g2 = Graph()

    with open(input_file_name, "r") as file:
        for line in file: # Edge set of G1
            print(line == "#####\n")
            
            if line.removesuffix("\n") == "#####":
                break
            line = line.split()
            if line:
                line = [int(i) for i in line]
                if line[0] in g1.E.keys():
                    g1.E[line[0]].append(line[1])
                else:
                    g1.E[line[0]] = [line[1]]
                if line[1] in g1.E.keys():
                    g1.E[line[1]].append(line[0])
                else:
                    g1.E[line[1]] = [line[0]]

        for line in file: # Edge set of G2
            if line == "#####":
                break
            line = line.split()
            if line:
                line = [int(i) for i in line]
                if line[0] in g2.E.keys():
                    g2.E[line[0]].append(line[1])
                else:
                    g2.E[line[0]] = [line[1]]

                if line[1] in g2.E.keys():

                    g2.E[line[1]].append(line[0])
                else:
                    g2.E[line[1]] = [line[0]]
    
    g1.V = g1.E.keys()
    g2.V = g2.E.keys()

    print(g1.V, g2.V)

load_instance("test.in")