const SimulationBinding = require("../../dist/simulation_binding");
const SimulationModule = SimulationBinding.SimulationModule;
const SimulationSettings = SimulationBinding.SimulationSettings;
const assert = require("assert");

const Grid = require('./test_grid_generator.js');

assert(SimulationModule, "The expected module is undefined");

var relativeSettingsPath = "./settings.json";

function testBasic()
{
    const instance = new SimulationModule("mr-yeoman");
    const settingsInstance = new SimulationSettings(relativeSettingsPath);
    instance.initialize(settingsInstance);
    var settings = instance.getSettings();
    Grid.generateGrid(4, 4);
    assert(instance.greet, "The expected method is not defined");
    assert.strictEqual(instance.greet("kermit"), "mr-yeoman", "Unexpected value returned");
}

function testInvalidParams()
{
    const instance = new SimulationModule();
}

assert.doesNotThrow(testBasic, undefined, "testBasic threw an expection");
assert.throws(testInvalidParams, undefined, "testInvalidParams didn't throw");

console.log("Tests passed- everything looks OK!");