"use strict";
const addon = require('../simulation_module/build/Debug/simulation_module-native');
const resolve = require('path').resolve;
;
;
class SimulationModule {
    constructor(name) {
        this._addonInstance = new addon.SimulationModule(name);
    }
    initialize(settings) {
        this._addonInstance.initialize(resolve(settings));
    }
    internal() {
        return this._addonInstance;
    }
    getSettings() {
        return this._addonInstance.getSettings();
    }
}
class SimulationSettings {
    constructor() {
        this._addonInstance = new addon.SimulationSettings();
    }
    internal() {
        return this._addonInstance;
    }
}
class SimulationData {
    constructor() {
        throw "No";
    }
    getHopCount(name) {
        return this._addonInstance.getHopCount(name);
    }
}
module.exports.SimulationModule = SimulationModule;
module.exports.SimulationSettings = SimulationSettings;
