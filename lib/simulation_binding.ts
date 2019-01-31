const addon = require('../simulation_module/build/Debug/simulation_module-native');
const resolve = require('path').resolve;

interface ISimulationSettingsNative
{

};

interface ISimulationModuleNative
{
    initialize(settings : string): void;
    getSettings() : ISimulationSettingsNative;

};

class SimulationModule {
    constructor(name: string) {
        this._addonInstance = new addon.SimulationModule(name);
    }


    initialize (settings: string) {
        this._addonInstance.initialize(resolve(settings));
    }

    internal (): ISimulationModuleNative {
        return this._addonInstance;
    }

    getSettings (): ISimulationSettingsNative {
        return this._addonInstance.getSettings();
    }

    private _addonInstance: ISimulationModuleNative;
}

class SimulationSettings {
    constructor() {
        this._addonInstance = new addon.SimulationSettings();
    }

    internal (): ISimulationSettingsNative {
        return this._addonInstance;
    }

    private _addonInstance: ISimulationSettingsNative;
}

module.exports.SimulationModule = SimulationModule;
module.exports.SimulationSettings = SimulationSettings;