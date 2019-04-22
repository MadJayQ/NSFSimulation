const SimulationBinding = require("../../dist/simulation_binding");
const SimulationModule = SimulationBinding.SimulationModule;
const SimulationSettings = SimulationBinding.SimulationSettings;
const assert = require("assert");
const fs = require('fs');
const path = require('path');
const Grid = require('./test_grid_generator.js');
const parse = require('csv-parse/lib/sync')
//const plotly = require('plotly')("madjayq", "Eep2scomeo1sHla0ARir");
assert(SimulationModule, "The expected module is undefined");

var relativeSettingsPath = "./settings.json";

Array.prototype.SumArray = function (arr) {
    var sum = [];
    if (arr != null && this.length == arr.length) {
        for (var i = 0; i < arr.length; i++) {
            sum.push(this[i] + arr[i]);
        }
    }

    return sum;
}


function testBasic() {
    const instance = new SimulationModule();
    const settingsInstance = new SimulationSettings();
    instance.initialize(relativeSettingsPath);
    var settings = instance.getSettings();
}

function testInvalidParams() {
    const instance = new SimulationModule();
}

function linspace(a, b, n) {
    if (typeof n === "undefined") n = Math.max(Math.round(b - a) + 1, 1);
    if (n < 2) { return n === 1 ? [a] : []; }
    var i, ret = Array(n);
    n--;
    for (i = n; i >= 0; i--) { ret[i] = (i * b + (n - i) * a) / n; }
    return ret;
}

function space(max, step) {
    ret = Array(max / step);
    var n = 0;
    for (var i = 0; i < max / step; i++) {
        ret[i] = n;
        n += step;
    }

    return ret;
}

function transformHistogram() {

    //Grab all of our relevant files
    let cologne_path = "F:\\Programming\\Work\\NSFSimulation\\maps\\cologne\\cologne.json";
    let cologne = JSON.parse(fs.readFileSync(cologne_path, 'utf8'));
    //Parse map meta data
    let rootDirectory = cologne.metadata.rootDirectory + "\\";
    let edgePathMissing = rootDirectory + "edges0.json";
    let edgePathNoMissing = rootDirectory + "edges.json";
    //Load edge list
    let edgesNoMissing = JSON.parse(fs.readFileSync(edgePathNoMissing, 'utf8'));
    let allEdges = JSON.parse(fs.readFileSync(edgePathMissing, 'utf8'));
    let missingEdges = [];
    var edgeKeys = Object.keys(allEdges);
    var edgesKeysNoMissing = Object.keys(edgesNoMissing);
    var edgeMap = {};
    var missingDataStatistics = {
        "highway.secondary": {
            data: [],
            percentage: 0,
            totalUnits: 0
        },
        "highway.primary": {
            data: [],
            percentage: 0,
            totalUnits: 0
        },
        "highway.motorway": {
            data: [],
            percentage: 0,
            totalUnits: 0
        },
        "highway.residential": {
            data: [],
            percentage: 0,
            totalUnits: 0
        },
        "highway.tertiary": {
            data: [],
            percentage: 0,
            totalUnits: 0
        },
        "highway.unclassified": {
            data: [],
            percentage: 0,
            totalUnits: 0
        },
        "highway.living_street": {
            data: [],
            percentage: 0,
            totalUnits: 0
        },
        "highway.trunk": {
            data: [],
            percentage: 0,
            totalUnits: 0
        },
        "other": {
            data: [],
            percentage: 0,
            totalUnits: 0
        }
    };

    var startTime = Date.now();
    var totalMissing = 0;
    for (var i = 0; i < edgeKeys.length; i++) {
        var edgeKey = edgeKeys[i];
        var edge = allEdges[edgeKey];
        var type = edge.type.split("_link")[0]; //Trim _link from all edges
        var keyIdx = edgesKeysNoMissing.indexOf(edgeKey);
        if (keyIdx == -1) {
            if (!(type in missingDataStatistics)) {
                type = "other";
            }
            missingDataStatistics[type].data.push(edgeKey);
            totalMissing += 1;
        }
        else {
            if (edgeMap[type] == undefined) {
                edgeMap[type] = [edgeKey];
            } else {
                edgeMap[type].push(edgeKey);
            }
        }
    }
    //Load histogram
    let histogramPath = rootDirectory + "edgehist.csv";
    let histogramCSV = fs.readFileSync(histogramPath, 'utf8');
    let binSize = parseInt(cologne.metadata.binSize);
    let bucketSize = parseInt(cologne.metadata.bucketSize);
    let records = parse(
        histogramCSV,
        {
            delimiter: ',',
            skip_empty_lines: true
        }
    );
    //Process histogram
    for (var recordIdx in records) {
        var record = records[recordIdx];
        var edge = record[0];
        var recordType = typeof record;
        if(typeof record !== 'object')
        {
            continue;
        }
        //Grab our frequencies
        var frequencies = record.slice(1);
        //Initialize our PDF
        let pdf = Array(bucketSize);
        //Calculate total samples
        var totalSamples = 0;
        var sum = 0;
        for (var i = 0; i < frequencies.length; i++) {
            var freq = parseInt(frequencies[i]);
            frequencies[i] = freq;
            totalSamples += freq;
        }
        //Probability of each sample is the frequency of that sample divided by the total samples
        for (var i = 0; i < bucketSize; i++) {
            var freq = frequencies[i];
            pdf[i] = freq / totalSamples;
            sum += pdf[i];
        }
        allEdges[edge].pdf = pdf;
    }

    for (var type in missingDataStatistics) {
        //Process missing data statistics
        missingDataStatistics[type].totalUnits = missingDataStatistics[type].data.length;
        missingDataStatistics[type].percentage = missingDataStatistics[type].totalUnits / totalMissing;
        var statistic = missingDataStatistics[type];
        if(statistic === undefined)
        {
            console.log("No data recorded for type: " + type + "!");
            continue;
        }
        for (var i = 0; i < statistic.data.length; i++) {
            var missingKey = statistic.data[i];
            var missingEdge = allEdges[missingKey];
            var type = missingEdge.type.split("_link")[0]; //Trim _link from all edges
            var sampleEdgeKeys = edgeMap[type];
            var pdf = Array(bucketSize).fill(0);
            for(var j = 0; j < sampleEdgeKeys.length; j++)
            {
                var edgeKey = sampleEdgeKeys[j];
                var sampleEdge = allEdges[edgeKey];
                pdf = pdf.SumArray(sampleEdge.pdf);
            }
            pdf = pdf.map((a) => a / sampleEdgeKeys.length);
            allEdges[missingKey].pdf = pdf;
        }
    }

    
    fs.writeFileSync(rootDirectory + "processedEdges.json", JSON.stringify(allEdges), {encoding: 'utf8', flag:'w'});
    fs.writeFileSync(rootDirectory + "edgesStatistics.json", JSON.stringify(missingDataStatistics), { encoding: 'utf8', flag: 'w' });
    var endTime = Date.now();
    console.log("Finished in " + (endTime - startTime) + " ms!");
}

//transformHistogram();
//Grid.generateGrid(5, 5);
assert.doesNotThrow(testBasic, undefined, "testBasic threw an expection");
//assert.throws(testInvalidParams, undefined, "testInvalidParams didn't throw");
console.log("Tests passed- everything looks OK!");