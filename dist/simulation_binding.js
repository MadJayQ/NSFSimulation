"use strict";
const addon = require('../simulation_module/build/Debug/simulation_module-native');
const resolve = require('path').resolve;
;
;
class SimulationModule {
    constructor(name) {
        this._addonInstance = new addon.SimulationModule(name);
    }
    greet(strName) {
        return this._addonInstance.greet(strName);
    }
    initialize(settings) {
        this._addonInstance.initialize(settings.internal());
    }
    onCommand() {
        return this._addonInstance.onCommand();
    }
    internal() {
        return this._addonInstance;
    }
    getSettings() {
        return this._addonInstance.getSettings();
    }
}
class SimulationSettings {
    constructor(jsonPath) {
        this._addonInstance = new addon.SimulationSettings(resolve(jsonPath));
    }
    internal() {
        return this._addonInstance;
    }
}
module.exports.SimulationModule = SimulationModule;
module.exports.SimulationSettings = SimulationSettings;
