import networkx as nx
import random
import sys

# Variables for setting up.
ROUNDS = 1000000
NODE_TARGET = 10000
ENTRY_NODES = 20
TARGET_EDGES = 20

# Do not change below this line.
currentNodes = 0
cycle = 0

G = nx.Graph()
for i in range(0, ENTRY_NODES - 1):
  G.add_node(i)
  if(i != 0):
    G.add_edge(i, i - 1)

  if(i == ENTRY_NODES - 1):
    G.add_edge(i, 0)

  currentNodes += 1

while cycle < ROUNDS:
  # Add a new node.
  if currentNodes < NODE_TARGET and random.random() <= 0.7:
    G.add_node(currentNodes)
    G.add_edge(currentNodes, random.randint(0, ENTRY_NODES - 1))
    currentNodes += 1

  # Add a new connection
  for i in range(0, currentNodes - 1):
    # There is a 90% change per node of not making a new connection.
    if random.random() <= 0.9:
      continue

    # If the node already has enough connection skip it.
    if len(list(G.neighbors(i))) >= TARGET_EDGES:
      continue

    ls = list(G.neighbors(i))
    top = (i, -1)
    for j in range(0, 4):
      if(len(ls) == 0):
        continue

      best = (top[0], -1)

      for item in ls:
        neigh = len(list(G.neighbors(item)))

        if best[1] <= neigh:
          best = (item, neigh)

      if(top[1] < best[1]):
        continue

      top = best
      ls = list(G.neighbors(top[0]))

    if top[0] == i or top[0] in list(G.neighbors(i)):
      continue

    G.add_edge(i, top[0])

  # Report the percentage
  if cycle % 500 == 0:
    if round((cycle / ROUNDS) * 100, 2) == 1:
        exit()

    sys.stdout.write("\rBuilding graph %s%%" %
                     str(round((cycle / ROUNDS) * 100, 2))
                     )
    sys.stdout.flush()
  cycle += 1

sys.stdout.write("\r\n")

print("Total nodes: ", len(G.nodes()))
print("Total edges: ", len(G.edges()))
print("Average degree: ", sum(i[1] for i in G.degree()) / len(G.nodes))
print("Average clustering: ", nx.average_clustering(G))
print("Average shortest path: ", nx.average_shortest_path_length(G))

