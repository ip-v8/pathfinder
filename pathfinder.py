import networkx as nx
import random
import sys

# Variables for setting up.
ROUNDS = 1000000
NODE_TARGET = 10000
ENTRY_NODES = 20
TARGET_EDGES = 50

# Do not change below this line.
currentNodes = 0
cycle = 0


def neighborsNoEntry(G: nx.Graph, i: int, entries: int):
  return list(filter(lambda n: n > entries - 1, list(G.neighbors(i))))


def getFittest(G: nx.Graph, n: int, entries: int):
  if len(neighborsNoEntry(G, n, entries)) == 0:
    return -1

  total = sum(len(neighborsNoEntry(G, i, entries))
              for i in neighborsNoEntry(G, n, entries))

  if(total == 0):
    return -1

  edgeNeighbors = map(lambda i: (
      i, len(neighborsNoEntry(G, i, entries))/total), neighborsNoEntry(G, n, entries))
  sortedList = sorted(edgeNeighbors, key=lambda i: i[1])

  chance = random.random()

  for i in range(len(sortedList) - 1):
    if(sortedList[i][1] >= chance):
      return sortedList[i][0]

    chance -= sortedList[i][1]

  return -1


G = nx.Graph()
for i in range(0, ENTRY_NODES - 1):
  G.add_node(i)
  if(i != 0):
    G.add_edge(i, i - 1)

  if(i == ENTRY_NODES - 1):
    G.add_edge(i, 0)

  currentNodes += 1

while cycle < ROUNDS:
  # Add a new node with a change of 10%.
  if currentNodes < NODE_TARGET and random.random() <= 0.1:
    G.add_node(currentNodes)
    G.add_edge(currentNodes, random.randint(0, ENTRY_NODES - 1))
    currentNodes += 1

  # Add 10 new connections every round
  for i in random.sample(range(0, currentNodes - 1), 10):
    # If the node already has enough connection skip it.
    if len(list(G.neighbors(i))) >= TARGET_EDGES:
      continue

    chosen = i
    for i in range(0, 5):
      res = getFittest(G, chosen, ENTRY_NODES)
      if res == -1:
        break
      chosen = res

    if chosen == i or chosen in (G.neighbors(i)):
      continue

    G.add_edge(i, chosen)

  # Report the percentage
  if cycle % 500 == 0:
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
