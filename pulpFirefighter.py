from pulp          import LpVariable, LpInteger, LpProblem, LpMinimize, lpSum
from minizinc      import Instance, Model, Solver
import numpy as np
import os


# ===== Pre-Defined Variables ===== #
testDir = "benchmarkSet/BBGRL/"     #
budget  = 1                         #
# ================================= #


def loadGraph(lines):
    """
     - Loads a graph from the BBGRL benchmark set with the given format found at 
     - https://www.ic.unicamp.br/~cid/Problem-instances/Firefighter-in-Graphs/
     - Args:
        - lines - The lines of the file
     - Returns:
        - n     - The number of nodes in the graph
        - T     - An approximate maximum time (floor(n / 2))
        - f     - A list of initial fire locations
        - G     - A graph as an adjacency matrix
    """
    n = int(lines[1].strip())
    f = [int(i)  for i in lines[3].strip().split(" ")]
    G = [[0] * n for i in range(n)]

    for line in lines[6::]:
        line = line.split(" ")

        G[int(line[0])][int(line[1])] = 1
        G[int(line[1])][int(line[0])] = 1

    return (n, (n // 2), f, G)


def pulpSolver(n, T, f, G):
    """
     - 0-1 encoding based on the PulP Python library using the default
     - solver (CBC MILP Solver) found at https://github.com/coin-or/Cbc
     - Args:
        - n - Number of nodes in the graph G
        - T - Maximum time limit
        - f - Initial fire locations
        - G - Adjacency list graph
    """
    b = LpVariable.dicts("b", (range(n), range(T + 1)), 0, 1, LpInteger)    #Burning nodes
    d = LpVariable.dicts("d", (range(n), range(T + 1)), 0, 1, LpInteger)    #Defended nodes

    lp = LpProblem("Firefighter_Problem", LpMinimize)
 
    lp += (lpSum(b[x][T] for x in range(n)), "Objective_Function")  #Minimize number of burned nodes
    lp += (lpSum(d[x][0] for x in range(n)) == 0, "")               #No nodes defended at t = 0

    for t in range(1, T):
        lp += (lpSum(d[x][t] - d[x][t - 1] for x in range(n)) <= budget, "")    #Stay in budget at each time t

        for x in range(n):
            lp += (b[x][0] == 1 if x in f else 0, "")   #Initial fires at t = 0
            lp += (b[x][t] >= b[x][t - 1], "")          #Burnt nodes remain burnt
            lp += (d[x][t] >= d[x][t - 1], "")          #Defended nodes remain defended
            lp += ((b[x][t] + d[x][t]) <= 1, "")        #Burnt nodes cant be defended etc

            nX = list(np.where(np.array(G[x]) == 1)[0])
            lp += (lpSum(b[y][t - 1] for y in nX) >= b[x][t], "")

            for y in nX:
                lp += (b[x][t] + d[x][t] >= b[y][t - 1], "")    #Determines the fire's spread
            
    lp.solve()


def minizincSolver(n, T, f, G):
    """
     - Calls the minizinc encoding/solver found in the file "firefighter.mzn".
     - Uses the gecode solver found at https://www.gecode.org/
     - Args:
        - n - Number of nodes in the graph G
        - T - Maximum time limit
        - f - Initial fire locations
        - G - Adjacency list graph
    """
    model  = Model("firefighter.mzn")   #Load the model
    solver = Solver.lookup("gecode")    #Set solver to gecode

    instance = Instance(solver, model)

    instance["n"] = n
    instance["T"] = T
    instance["f"] = f
    instance["G"] = G
    instance["budget"] = budget

    result = instance.solve()
    print(result)


for testFile in os.listdir(testDir):
    gFile = open(testDir + testFile)
    n, T, f, G = loadGraph(gFile.readlines())

    #pulpSolver(n, T, f, G)
    minizincSolver(n, T, f, G)
    
