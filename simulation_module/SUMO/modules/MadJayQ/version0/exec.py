import sys, json, time

from model import simulationTick
from model import calculateMaximumTimeSensing

def runSimulation():
    worldJSON = json.loads(sys.argv[1]);
    timeStep = worldJSON["settings"]["timeSettings"]["timeStep"];
    time = 0
    maxTime = worldJSON["settings"]["timeSettings"]["maxTime"]
    res = simulationTick(worldJSON, time);
    print("done")
    running = False;
    return res;
def main():
    running = True;
    while running:
        command = sys.stdin.readline().split('\n')[0];
        if command == "start":
            sys.stdout.flush();
            newWorld = runSimulation();
            running = False;
            sys.stdout.flush();
            print(newWorld);
            sys.stdout.flush();
        if command == "max-ts":
            sys.stdout.flush();
            worldJSON = json.loads(sys.argv[1]);
            maxTS = calculateMaximumTimeSensing(worldJSON);
            print("done");
            print(maxTS);
            running = False;
            sys.stdout.flush();
        time.sleep(0.1);
        

if __name__ == '__main__':
main();
