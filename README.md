# SatSolverISI
SAT Solver for Induced Subgraph Isomorphisms

Description:

Given 2 input graphs, Pattern P and Host H, we need to check if P is an induced subgraph of H
For P to be an induced subgraph of H, we need to check 2 conditions
1. for every vertex in i in P, there exists a corresponding vertex a in H s.t we can establish a one-one mapping f from P to H such that f(i) = a

2. for every pair of distinct vertices i,j in P s.t a,b = f(i),f(j) in H:
    for every edge (i,j) in P, edge (a,b) in H
    and for every (i,j) not in P, (a,b) not in H 

For my CNF encoding I have defined variable (i,a) where i is a vertex in pattern and a is a vertex in host, var(i,a) is positive if i maps to a and false if i does not map to a

in my implementation I implement var as var(i,a,n) (n = host vertex count) = (i-1) * n + (a-1) + 1 to make sure every mapping gets a unique var based on vertex count and the mapping is non-zero




Input format:

test.in:
________
G1 Vertex set| v1 v2 v3... 
1 2 3 4
G2 Vertex Set | v1 v2 v3...
1 2 3 4 5

Edge set of G1 in format | u v
1 2
2 4
3 2
3 4
#####
Edge set of G2 in format | u v
1 2
2 4
3 2
3 5
#####
________