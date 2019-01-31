declare const addon: any;
declare const resolve: any;
interface ISimulationSettingsNative {
}
interface ISimulationModuleNative {
    initialize(settings: string): void;
    getSettings(): ISimulationSettingsNative;
}
declare class SimulationModule {
    constructor(name: string);
    initialize(settings: string): void;
    internal(): ISimulationModuleNative;
    getSettings(): ISimulationSettingsNative;
    private _addonInstance;
}
declare class SimulationSettings {
    constructor();
    internal(): ISimulationSettingsNative;
    private _addonInstance;
}
