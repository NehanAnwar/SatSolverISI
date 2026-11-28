from argparse import ArgumentParser
import subprocess


class Graph:
    def __init__(self,id):
        self.ID = id
        self.VerticeCount = 0
        self.Vertices = []
        self.Edges = {} # Adjacency list of edges
    
    def has_edge(self,u,v): # check if edge contained in graph
        return True if v in self.Edges[u] else False





def load_instance(input_file_name):
    # read the input instance
    # the instance is The vertice count in G1, Edge count in G1, Vertice count in G2, Edge count in G2
    # Edge set of G1
    # Edge set of G2

    g1 = Graph(1)
    g2 = Graph(2)
    with open(input_file_name, "r") as file:

        g1.Vertices = [int(x) for x in next(file).split()] # Reads Vertices of Graph 1
        print(g1.Vertices)
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

    # print(f"{g1.Vertices} \n\n {g2.Vertices}")
    # print(f"{g1.Edges}\n\n{g2.Edges}")
    return g1,g2


def var(i,a,host_count):
    #  vertex i in pattern -> vertex a in Host
    return (i-1) * host_count + (a-1) + 1

def encode(pattern_graph, host_graph):

    clauses = []
    k = pattern_graph.VerticeCount
    n = host_graph.VerticeCount

    def pattern_vertices_map_to_one_host_vertex_each(pattern,host):  #every vertex in the pattern graph maps to exactly one vertex in the host graph, (God please rename this function before submission)
        for i in pattern.Vertices:
            ### foreach i in patten, i maps to at least one vertex in host
            clauses.append([var(i,a,n) for a in host.Vertices])

            for a in host.Vertices:
                for b in host.Vertices:
                    if a<b:
                        # for each i in pattern, for every distinct a,b . NOT((i mapped to a) AND (i mapped to b)) = (NOT(i mapped to a) OR NOT(i mapped to b))
                        # so every vertex in pattern be mapped to at most 1 vertex in host
                        clauses.append([-var(i,a,n),-var(i,b,n)])

    def injectivity(pattern,host):
        for i in pattern.Vertices:
            for j in pattern.Vertices:
                if i<j:
                    for a in host.Vertices:
                        # for every distinct vertices i,j in pattern, vertex a in host, if i maps to a then j must not map to a
                        # NOT((i maps to a) AND (j maps to a)) = (NOT(i maps to a) OR NOT(j maps to a)) 
                        clauses.append([-var(i,a,n),-var(j,a,n)])

    def inductivity(pattern,host):
        for i in pattern.Vertices:
            for j in pattern.Vertices:
                if i < j:
                    for a in host.Vertices:
                        for b in host.Vertices:
                            if a != b:

                                # for every unique pair of vertices i,j in pattern, we check if the unique vertices they are mapped to in host, a,b have the same connectivity
                                pattern_edge = pattern.has_edge(i, j)
                                host_edge = host.has_edge(a, b)

                                # IF (edge ij and not edge ab) OR (not edge ij and edge ab) 
                                if pattern_edge != host_edge:
                                    # NOT((i mapped to a) AND (j mapped to b)) = (NOT(i maps to a) OR Not(j maps to b))
                                    clauses.append([-var(i, a, n),-var(j, b, n)])



    pattern_vertices_map_to_one_host_vertex_each(pattern_graph,host_graph)
    injectivity(pattern_graph,host_graph)
    inductivity(pattern_graph,host_graph)
    return clauses
    ## TODO: result printing


def call_solver(cnf,nr_vars,output_name,solver_name,verbosity):
    # print CNF into formula.cnf in DIMACS format
    with open(output_name, "w") as file:
        file.write("p cnf " + str(nr_vars) +" " + str(len(cnf)) + '\n')
        for clause in cnf:
            file.write(' '.join(str(lit) for lit in clause) + " 0" +'\n')

    # call the solver and return the output
    print("running solver")
    return subprocess.run(['./' + solver_name, '-model', '-verb=' + str(verbosity) , output_name], stdout=subprocess.PIPE)
    print("done running solver")

def print_result(result):
    for line in result.stdout.decode('utf-8').split('\n'):
        print(line)                 # print the whole output of the SAT solver to stdout, so you can see the raw output for yourself

    # check the returned result
    if result.returncode == 10:
        print("PASS : Pattern graph is an induced Subgraph of Host")
    elif result.returncode == 20:
        print("FAIL : Pattern graph is NOT an induced subgraph of Host")
    else:
        print("Unknown result code")



parser = ArgumentParser()

parser.add_argument(
    "-i",
    "--input",
    default="input.in",
    type=str,
    help=(
        "The instance file."
    ),
)
parser.add_argument(
    "-o",
    "--output",
    default="formula.cnf",
    type=str,
    help=(
        "Output file for the DIMACS format (i.e. the CNF formula)."
    ),
)
parser.add_argument(
    "-s",
    "--solver",
    default="glucose",
    type=str,
    help=(
        "The SAT solver to be used."
    ),
)
parser.add_argument(
    "-v",
    "--verb",
    default=1,
    type=int,
    choices=range(0,2),
    help=(
        "Verbosity of the SAT solver used."
    ),
)
args = parser.parse_args()


Pattern,Host = load_instance(args.input)
print(Pattern.Vertices)
print(Host.Vertices)
cnf = encode(Pattern,Host)
print(cnf)
result = call_solver(cnf,Pattern.VerticeCount * Host.VerticeCount,args.output,args.solver,args.verb)

print_result(result)

print("Result Done!")


