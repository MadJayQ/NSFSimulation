from utils import indexToCoordinates
from utils import coordinatesToIndex
from utils import getNeighboringCells
from utils import ncr;
from utils import findShortestPath
import random
import json

paths = [];
skipSelf = False;
def calculateTimeSensing(world, targetCell):
    width = world["settings"]["worldSettings"]["tileWidth"];
    height = world["settings"]["worldSettings"]["tileHeight"];
    tile = world["tiles"][str(targetCell)];
    reward = float(tile["reward"]);
    cost = float(tile["cost"]);
    numParticipants = len(tile["attachedEnts"]) + 1; #Add one to the number of entities to represent ourselves in the current iteration
    if(numParticipants < 2):
        numParticipants = 2;
    #print("COST, NUMPARTIC");
    #print(cost);
    #print(numParticipants)
    #print("/COST");
    totalCost = float(cost)  * float(numParticipants);
    predictedReward = float(numParticipants - 1) * reward;
    timeSensingPlan = float(predictedReward / totalCost) * (1.0 / float(numParticipants));
    #print(timeSensingPlan);
    return timeSensingPlan;
def calculateMaximumTimeSensing(world):
    tiles = world["tiles"];
    maxTS = -99999;
    for tileIdx in tiles:
        ts = calculateTimeSensing(world, tileIdx);
        if(ts > maxTS):
            maxTS = ts;
    return maxTS;
def calculateExpectedUtility(world, targetCell, currentCar):
    width = world["settings"]["worldSettings"]["tileWidth"];
    height = world["settings"]["worldSettings"]["tileHeight"];
    reward = int(world["tiles"][str(targetCell)]["reward"]);
    #print(reward);
    cellPosition = indexToCoordinates(targetCell, width);
    neighboringCells = getNeighboringCells(cellPosition[0], cellPosition[1], width, height); #Calculate our neighboring cells
    #print(cellPosition);
    #print("~~~");
    neighboringCars = [];
    for neighbor in neighboringCells: #Loop through all these cells, and count the number of cars
        #print(indexToCoordinates(neighbor, width));
        neighborTile = world["tiles"][str(neighbor)];
        neighborEnts = neighborTile["attachedEnts"];
        #print("///");
        for ent in neighborEnts: #If not a car, discard
            if "car-" not in ent: 
                continue;
            if ent == currentCar and skipSelf: #Don't count ourselves?
                continue;
            neighboringCars.append(neighborEnts[ent]);
    totalNeighbors = len(neighboringCars);
    #print(totalNeighbors);
    combinedProbabilityDenominator = 0
    combinedProbability = 0
    expectedUtility = 0
    #print("...............");
    for n in range(0, totalNeighbors): #Sum the combined combinations formula
        combinedProbabilityDenominator += ncr(totalNeighbors - 1, n - 1);
    #print(combinedProbabilityDenominator)
    #print("...............");
    for n in range(1, totalNeighbors):
        n = ncr(totalNeighbors - 1, n - 1);
        utility = float(n * reward) / float(combinedProbabilityDenominator * (n ** 2));
        expectedUtility += utility; 
    #print("/////////////////");
    #print(expectedUtility);
    return expectedUtility;

def simulationTick(world, timestamp):
    cars = world["settings"]["carSettings"];
    tiles = world["tiles"];
    width = int(world["settings"]["worldSettings"]["tileWidth"]);
    height = int(world["settings"]["worldSettings"]["tileHeight"]);
    #Calculate the cost of the cell by taking the maximum time sensing plan across the whole game, and then multiplying it by an arbitrary value.
    moves = {};
    for tileIdx in tiles:
        tile = world["tiles"][tileIdx];
        attachedEnts = tile["attachedEnts"];
        if len(attachedEnts) > 0:
            tilePos = indexToCoordinates(tileIdx, width);
            for currentCar in list(attachedEnts):
                if currentCar != '':
                    carObj = attachedEnts[currentCar];
                    start = carObj["startPos"];
                    finish = carObj["endPos"];
                    if start[0] == finish[0] and start[1] == finish[1]:
                        continue;
                    adjacentCells = getNeighboringCells(tilePos[0], tilePos[1], width, height);
                    evs = [];
                    shortestPathes = [];
                    coords = [];
                    timeSensingPlans = [];
                    capacity = carObj["capacity"];
                    for i in range(0, len(adjacentCells)):
                        adjacentCell = adjacentCells[i];
                        evs.append(calculateExpectedUtility(world, adjacentCell, currentCar));
                        timeSensingPlans.append(calculateTimeSensing(world, adjacentCell));
                        coords.append(indexToCoordinates(adjacentCell, width));
                        shortestPathes.append(findShortestPath(coords[i], finish, width, height));
                    print("BEFORE PRUNTING========");
                    print(evs);
                    print(timeSensingPlans);
                    print(coords);
                    print(shortestPathes);
                    print("==============");
                    availableTiles = [];
                    newIdx = -1;
                    newCapacity = capacity;
                    for i in range(0, len(timeSensingPlans)): #Determine which of our adjacent cells we can ever possibly traverse to.
                        timeSensingPlan = timeSensingPlans[i];
                        if(capacity > timeSensingPlan):
                            availableTiles.append(i);
                    if len(availableTiles) > 0:
                        #Pick tile with greatest utility
                        largestUtility = -999999;
                        largestUtilityIdx = [-1];
                        for i in range(0, len(evs)):
                            ev = evs[i];
                            if abs(ev - largestUtility) < 1e-13:
                                largestUtilityIdx.append(i);
                            if ev > largestUtility:
                                largestUtility = ev;
                                largestUtilityIdx = [i];
                        if len(largestUtilityIdx) > 1: #Multiple tiles with similar Utility? Choose shortest path
                            shortestPath = 9999999;
                            shortestPathIdx = [-1];
                            for i in range(0, len(largestUtilityIdx)):
                                if abs(shortestPathes[largestUtilityIdx[i]] - shortestPath) < 1e-13:
                                    shortestPathIdx.append(largestUtilityIdx[i]);
                                if shortestPathes[largestUtilityIdx[i]] < shortestPath:
                                    shortestPath = shortestPathes[largestUtilityIdx[i]];
                                    shortestPathIdx = [largestUtilityIdx[i]];
                            if len(shortestPathIdx) > 1:
                                #Return random point at this point...
                                newInternalIdx = random.randint(0, len(shortestPathIdx) - 1);
                                newIdx = shortestPathIdx[newInternalIdx];
                            else:
                                newIdx = shortestPathIdx[0];
                        else:
                            newIdx = largestUtilityIdx[0]; 
                        newCapacity -= timeSensingPlans[newIdx];
                    else:
                        #Pick tile with shortest path
                        shortestPath = 9999999;
                        shortestPathIdx = [-1];
                        for i in range(0, len(shortestPathes)):
                            if abs(shortestPathes[i] - shortestPath) < 1e-13:
                                shortestPathIdx.append(i);
                            if shortestPathes[i] < shortestPath:
                                shortestPath = shortestPathes[i];
                                shortestPathIdx = [i];
                        if len(shortestPathIdx) > 1:
                            #Return random point
                            newInternalIdx = random.randint(0, len(shortestPathIdx) - 1);
                            newIdx = shortestPathIdx[newInternalIdx];
                        else:
                            newIdx = shortestPathIdx[0];
                    moves[currentCar] = {
                        'previous': tileIdx,
                        'new': adjacentCells[newIdx],
                        'newCapacity': newCapacity
                    };
return json.dumps(moves);
