class Queue:
  #Constructor creates a list
  def __init__(self):
      self.queue = list()

  #Adding elements to queue
  def enqueue(self,data):
      #Checking to avoid duplicate entry (not mandatory)
    self.queue.insert(0,data)

  #Removing the last element from the queue
  def dequeue(self
      if len(self.queue)>0:
          return self.queue.pop()
      return ("Queue Empty!")

  #Getting the size of the queue
  def size(self):
      return len(self.queue)

def coordinatesToIndex(x, y, width):
    return x + width * y;
def indexToCoordinates(index, width):
    idx = int(index);
    x = idx % width;
    y = idx / width;
    return [x, y];
def findShortestPath(start, finish, width, height):
    moveCount = 0
    nodesLeftInLayer = 1
    nodesInNextLayer = 0
    terminated = False
    visited = [[0]*width for i in range(height)];
    xQueue = Queue();
    yQueue = Queue();
    xQueue.enqueue(start[0]);
    yQueue.enqueue(start[1]);
    while xQueue.size() > 0:
        x = xQueue.dequeue();
        y = yQueue.dequeue();
        if x == finish[0] and y == finish[1]:
            terminated = True
            break;
        neighbors = getNeighboringCells(int(x), int(y), int(width), int(height));
        for neighbor in neighbors:
            neighborCoordinates = indexToCoordinates(neighbor, width);
            nX = neighborCoordinates[0];
            nY = neighborCoordinates[1];
            if visited[nY][nX] == 1: 
                continue;
            xQueue.enqueue(nX);
            yQueue.enqueue(nY);
            visited[nY][nX] = 1;
            nodesInNextLayer += 1;
        nodesLeftInLayer -= 1
        if nodesLeftInLayer == 0:
            nodesLeftInLayer = nodesInNextLayer
            nodesInNextLayer = 0
            moveCount += 1
    if terminated:
        return moveCount;
    return -1;
def getNeighboringCells(x, y, width, height): 
    targetPos = [x, y];
    neighboringCells = [];
    if targetPos[0] - 1 >= 0:
        neighboringCells.append(
            coordinatesToIndex(targetPos[0] - 1, targetPos[1], width)
        );
        if targetPos[1] + 1 < height:
            neighboringCells.append(
                coordinatesToIndex(targetPos[0] - 1, targetPos[1] + 1, width)
            );
        if targetPos[1] - 1 >= 0:
            neighboringCells.append(
                coordinatesToIndex(targetPos[0] - 1, targetPos[1] - 1, width)
            );
    if targetPos[0] + 1 < width:
        neighboringCells.append(
            coordinatesToIndex(targetPos[0] + 1, targetPos[1], width)
        );
        if targetPos[1] + 1 < height:
            neighboringCells.append(
                coordinatesToIndex(targetPos[0] + 1, targetPos[1] + 1, width)
            );
        if targetPos[1] - 1 >= 0:
            neighboringCells.append(
                coordinatesToIndex(targetPos[0] + 1, targetPos[1] - 1, width)
            );
    if targetPos[1] - 1 > 0:
        neighboringCells.append(
            coordinatesToIndex(targetPos[0], targetPos[1] - 1, width)
        );
    if targetPos[1] + 1 < height:
        neighboringCells.append(
            coordinatesToIndex(targetPos[0], targetPos[1] + 1, width)
        );
    return neighboringCells;
#Credits: https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python
import operator as op
def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, xrange(n, n-r, -1), 1)
    denom = reduce(op.mul, xrange(1, r+1), 1)
return numer//denom
