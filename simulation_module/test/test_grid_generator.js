const fs = require('fs');
const path = require('path');

let gridPath = "./grid.json";

let generateGrid = (w , h) => {
    let toIndex = (x, y, w) => {
        return x + (y * w);
    };
    let toCoords = (i, w) => {
        return [i % w, Math.floor(i / w)];
    };
    let buildAdjacency = (i, w, h) => {
        let targetPos = toCoords(i, w);
        let adjacenctCells = [];
        if(targetPos[0] - 1 >= 0) {
            adjacenctCells.push(toIndex(targetPos[0] - 1, targetPos[1], w));
            if(targetPos[1] + 1 < h) adjacenctCells.push(toIndex(targetPos[0] - 1, targetPos[1] + 1, w));
            if(targetPos[1] - 1 >= 0) adjacenctCells.push(toIndex(targetPos[0] - 1, targetPos[1] - 1, w));

        }
        if(targetPos[0] + 1 < w) {
            adjacenctCells.push(toIndex(targetPos[0] + 1, targetPos[1], w));
            if(targetPos[1] + 1 < h) adjacenctCells.push(toIndex(targetPos[0] + 1, targetPos[1] + 1, w));
            if(targetPos[1] - 1 >= 0) adjacenctCells.push(toIndex(targetPos[0] + 1, targetPos[1] - 1, w));

        }
        if(targetPos[1] - 1 >= 0) adjacenctCells.push(toIndex(targetPos[0], targetPos[1] - 1, w));
        if(targetPos[1] + 1 < h) adjacenctCells.push(toIndex(targetPos[0], targetPos[1] + 1, w));

        return adjacenctCells;
    };
    let adjacency = new Array(w * h).fill([]);
    for(var i = 0; i < h; i++)
    {
        for(var j = 0; j < w; j++) {
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
    for(var node in adjacency) {
        adjacencyJSON.nodes[node] = {};
        var edge = {
            speed: 55,
            distance: 50
        };
        for(var adjacentNode in adjacency[node]) {
            var edgeName = node.toString() + "_to_" + adjacency[node][adjacentNode].toString();
            adjacencyJSON.edges[edgeName] = edge; 
        }
    }
    var jsonData = JSON.stringify(adjacencyJSON, null, 2);
    let gridFilePath = path.resolve(gridPath);
    fs.open(gridFilePath, 'r', (err, fd) => {
        if(err) {
            fs.writeFile(gridFilePath, jsonData, (err) => {
                if(err) {
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