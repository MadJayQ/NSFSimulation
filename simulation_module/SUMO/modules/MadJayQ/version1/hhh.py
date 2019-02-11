# utils.py
# Original code by: Jake Thorton
# Modifications by: Quentin Goss

# Author: Jake Thorton
class Queue:
  def __init__(self):
    self.queue = list()
    
  # Adding elements to queue
  def enqueue(self,data):
    # Checking to avoid duplicate entry (not mandatory)
    self.queue.insert(0,data)
    
  # Removing the last element from the queue
  def dequeue(self):
    if len(self.queue) > 0:
      return self.queue.pop()
    else:
      return("Queue Empty!")
      
  def size(self):
    return len(self.queue)
# end class Queue

# Author: Jake Thorton
# @param int x: x coordinate
# @param int y: y coordinate
# @param int width: Width of tile
# @return int index: index of tile at coords [x,y]
def coordinatesToIndex(x, y, width):
  return x + width * y
  
# Author: Jake Thorton
# @param int index: index of tile.
# @param int width: width of tile
# @return [int x,int y]: Coordinates of tile.
def indexToCoordinates(index, width):
  idx = int(index)
  x = idx % width
  y = idx / width
  return [x, y]

# Author: Jake Thorton
# @param int x: x coordinate
# @param int y: y coordinate
# @param int width: width of tile
# @param int height: height of tile
# @return int neightboringCells[] : List of indexs of cells that neighbor
#  the cell which contains [x,y].
def getNeighboringCells(x, y, width, height):
  targetPos = [x, y]
  neighboringCells = []
  if targetPos[0] - 1 >= 0:
    neighboringCells.append(coordinatesToIndex(targetPos[0]-1, targetPos[1], width))
    if targetPos[1] + 1 < height:
      neighboringCells.append(coordinatesToIndex(targetPos[0]-1, targetPos[1]+1, width))
    if targetPos[1] - 1 >= 0:
      neighboringCells.append(coordinatesToIndex(targetPos[0]-1, targetPos[1]-1, width))
  # end if targetPos[0] - 1 >= 0:
  if targetPos[0] + 1 < width:
    neighboringCells.append(coordinatesToIndex(targetPos[0]+1, targetPos[1], width))
    if targetPos[1] + 1 < height:
      neighboringCells.append(coordinatesToIndex(targetPos[0]+1, targetPos[1]+1, width))
    if targetPos[1] - 1 >= 0:
      neighboringCells.append(coordinatesToIndex(targetPos[0]+1, targetPos[1-1], width))
  # end if targetPos[0] + 1 < width:
  if targetPos[1] - 1 > 0:
    neighboringCells.append(coordinatesToIndex(targetPos[0], targetPos[1]-1, width))
  if targetPos[1] + 1 < height:
    neighboringCells.append(coordinatesToIndex(targetPos[0], targetPos[1]+1, width))

# Author: Jake Thorton
# @param int start[x,y]: [x,y] Coordinates of starting position.
# @param int finish[x,y]: [x,y] Coordinates of ending position.
# @param int width: Width of tiles
# @param int height: Height of tiles
def findShortestPath(start, finish, width, height):
  moveCount = 0
  nodesLeftInLayer = 1
  nodesInNextLayer =0
  terminated = False
  visited = [[0] * width for i in range(height)]
  xQueue = Queue()
  yQueue = Queue()
  xQueue.enqueue(start[0])
  yQueue.enqueue(start[1])
  while xQueue.size() > 0:
    x = xQueue.dequeue()
    y = yQueue.dequeue()
    if x == finish[0] and y == finish[1]:
      teriminated = True
      break;
    neighbors = getNeighboringCells(int(x), int(y), int(width), int(height))
    for neighbor in neighbors:
      neighborCoordinates = indexToCoordinates(neighbor, width)
      nX = neighborCoordinates[0]
      nY = neighborCoordinates[1]
      if visited[nY][nX] == 1:
        continue
      xQueue.enqueue(nX)
      yQueue.enqueue(nY)
      visited[nY][nX] = 1
      nodesInNextLayer += 1
    # end for neighbor in neighbors
    nodesLeftInLayer -= 1
    if nodesLeftInLayer == 0:
      nodesLeftInLayer = nodesInNextLayer
      nodesInNextLayer = 0
      moveCount += 1
    if terminated:
      return moveCount
    else:
      return -1
  # end while xQueue.size() > 0:
    
  
#Credits: https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python
# Modified to work with python3 by: Quentin Goss
import operator as op
import functools
def ncr(n, r):
  n = int(n)
  r = int(r)
  r = min(r, n-r)
  numer = functools.reduce(op.mul, range(n, n-r, -1), 1)
  denom = functools.reduce(op.mul, range(1, r+1), 1)
  return numer//denom
  
# Author: Quentin Goss
def test():
  # Queue
  q = Queue()
  print(q)
  print(q.dequeue())
  q.enqueue(100)
  q.enqueue("Hello World")
  q.enqueue(True)
  q.enqueue(7.344)
  print(q)
  print(q.size())
  print(q.dequeue())
  print(q.dequeue())
  print(q.dequeue())
  print(q.dequeue())
    
  # coordsToIndex
  print()
  print("index=" + str(coordinatesToIndex(12,50,30)))
  print("index=" + str(coordinatesToIndex(120,30,100.34)))
  
  # indexToCoordinates
  print()
  print(indexToCoordinates(30,1533))
  print(indexToCoordinates(77,375.44))
  
  # getNeighboringCells
  print()
  print(getNeighboringCells(5, 2, 25, 77))
  print(getNeighboringCells(13.4, 6, 33.4, 90.2))
  
  # findShortestPath
  #print()
  #print(findShortestPath([1,12],[3,2],57,34))
  #print(findShortestPath([5,5],[5,5],-1,0))
  
  # ncr
  print()
  print(ncr(50,12))
  print(ncr(1300,3.5))
  print(ncr(14.4,70))
test()
