const fs = require('fs');
const path = require('path');

let gridPath = "./grid.json";

function S4() {
    return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
}


let generateGrid = (w, h) => {
    let toIndex = (x, y, w) => {
        return x + (y * w);
    };
    let toCoords = (i, w) => {
        return [i % w, Math.floor(i / w)];
    };
    let buildAdjacency = (i, w, h) => {
        let targetPos = toCoords(i, w);
        let adjacenctCells = [];
        if (targetPos[0] - 1 >= 0) {
            adjacenctCells.push(toIndex(targetPos[0] - 1, targetPos[1], w));
            if (targetPos[1] + 1 < h) adjacenctCells.push(toIndex(targetPos[0] - 1, targetPos[1] + 1, w));
            if (targetPos[1] - 1 >= 0) adjacenctCells.push(toIndex(targetPos[0] - 1, targetPos[1] - 1, w));

        }
        if (targetPos[0] + 1 < w) {
            adjacenctCells.push(toIndex(targetPos[0] + 1, targetPos[1], w));
            if (targetPos[1] + 1 < h) adjacenctCells.push(toIndex(targetPos[0] + 1, targetPos[1] + 1, w));
            if (targetPos[1] - 1 >= 0) adjacenctCells.push(toIndex(targetPos[0] + 1, targetPos[1] - 1, w));

        }
        if (targetPos[1] - 1 >= 0) adjacenctCells.push(toIndex(targetPos[0], targetPos[1] - 1, w));
        if (targetPos[1] + 1 < h) adjacenctCells.push(toIndex(targetPos[0], targetPos[1] + 1, w));

        return adjacenctCells;
    };
    let adjacency = new Array(w * h).fill([]);
    for (var i = 0; i < h; i++) {
        for (var j = 0; j < w; j++) {
            var idx = toIndex(j, i, w);
            adjacency[idx] = buildAdjacency(idx, w, h);
        }
    }
    var adjacencyJSON = {
        width: w,
        height: h,
        nodes: {

        },
        edges: {

        }
    };
    var budgetList = [200, 300, 150, 600, 170, 180, 150, 100, 80, 200, 210, 200, 150, 100, 100, 220, 180, 200, 200, 130, 80, 315, 300, 150, 190];
    for (var i = 0; i < adjacency.length; i++) {
        var node = i;
        adjacencyJSON.nodes[node] = {};
        var adjacencyList = adjacency[node];
        if(i < budgetList.length)
        {
            adjacencyJSON.nodes[node].budget = budgetList[i];
        }
        for (var j = 0; j < adjacencyList.length; j++) {
            var edgeName = S4();
            var from = node.toString();
            var to = adjacencyList[j].toString();
            adjacencyJSON.edges[edgeName] = {
                from: from,
                to: to,
                speed: 55,
                distance: 50
            };
        }
    }
    var jsonData = JSON.stringify(adjacencyJSON, null, 2);
    let gridFilePath = path.resolve(gridPath);
    fs.open(gridFilePath, 'r', (err, fd) => {
        if (err) {
            fs.writeFile(gridFilePath, jsonData, (err) => {
                if (err) {
                    console.error(err);
                }
                console.log("File saved!");
            });
        } else {
            console.log("The file exists!");
        }
    });
};

module.exports.generateGrid = generateGrid;
module.exports.gridPath = gridPath;