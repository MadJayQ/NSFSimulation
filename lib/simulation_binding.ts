const addon = require('../simulation_module/build/Debug/simulation_module-native');
const resolve = require('path').resolve;

interface ISimulationSettingsNative
{

};

interface ISimulationModuleNative
{
    greet(strName: string): string;
    initialize(settings : ISimulationSettingsNative): void;
    onCommand() : void;
    getSettings() : ISimulationSettingsNative;

};

class SimulationModule {
    constructor(name: string) {
        this._addonInstance = new addon.SimulationModule(name);
    }

    greet (strName: string) {
        return this._addonInstance.greet(strName);
    }

    initialize (settings: SimulationSettings) {
        this._addonInstance.initialize(settings.internal());
    }

    onCommand () {
        return this._addonInstance.onCommand();
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
    constructor(jsonPath: string) {
        this._addonInstance = new addon.SimulationSettings(resolve(jsonPath));
    }

    internal (): ISimulationSettingsNative {
        return this._addonInstance;
    }

    private _addonInstance: ISimulationSettingsNative;
}

module.exports.SimulationModule = SimulationModule;
module.exports.SimulationSettings = SimulationSettings;