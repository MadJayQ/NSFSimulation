const addon = require('../simulation_module/build/Debug/simulation_module-native');
const resolve = require('path').resolve;

interface ISimulationModuleNative
{
    greet(strName: string): string;
    onCommand() : void;

};
interface ISimulationSettingsNative
{

};

class SimulationModule {
    constructor(name: string) {
        this._addonInstance = new addon.SimulationModule(name);
    }

    greet (strName: string) {
        return this._addonInstance.greet(strName);
    }

    onCommand () {
        return this._addonInstance.onCommand();
    }

    private _addonInstance: ISimulationModuleNative;
}

class SimulationSettings {
    constructor(jsonPath: string) {
        this._addonInstance = new addon.SimulationSettings(resolve(jsonPath));
    }

    private _addonInstance: ISimulationSettingsNative;
}

module.exports.SimulationModule = SimulationModule;
module.exports.SimulationSettings = SimulationSettings;