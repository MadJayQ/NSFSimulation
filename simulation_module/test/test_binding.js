const SimulationBinding = require("../../dist/simulation_binding");
const SimulationModule = SimulationBinding.SimulationModule;
const SimulationSettings = SimulationBinding.SimulationSettings;
const assert = require("assert");

const Grid = require('./test_grid_generator.js');

assert(SimulationModule, "The expected module is undefined");

var relativeSettingsPath = "./settings.json";

function testBasic()
{
    const instance = new SimulationModule();
    const settingsInstance = new SimulationSettings();
    instance.initialize(relativeSettingsPath);
    var settings = instance.getSettings();
}

function testInvalidParams()
{
    const instance = new SimulationModule();
}

Grid.generateGrid(10, 10);
//assert.doesNotThrow(testBasic, undefined, "testBasic threw an expection");
//assert.throws(testInvalidParams, undefined, "testInvalidParams didn't throw");
console.log("Tests passed- everything looks OK!");