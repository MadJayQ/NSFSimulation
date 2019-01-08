declare const addon: any;
declare const resolve: any;
interface ISimulationModuleNative {
    greet(strName: string): string;
    onCommand(): void;
}
interface ISimulationSettingsNative {
}
declare class SimulationModule {
    constructor(name: string);
    greet(strName: string): string;
    onCommand(): void;
    private _addonInstance;
}
declare class SimulationSettings {
    constructor(jsonPath: string);
    private _addonInstance;
}
