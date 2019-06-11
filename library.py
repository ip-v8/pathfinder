import networkx as nx
import random


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
