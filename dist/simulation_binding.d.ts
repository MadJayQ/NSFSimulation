declare const addon: any;
declare const resolve: any;
interface ISimulationSettingsNative {
}
interface ISimulationModuleNative {
    greet(strName: string): string;
    initialize(settings: ISimulationSettingsNative): void;
    onCommand(): void;
    getSettings(): ISimulationSettingsNative;
}
declare class SimulationModule {
    constructor(name: string);
    greet(strName: string): string;
    initialize(settings: SimulationSettings): void;
    onCommand(): void;
    internal(): ISimulationModuleNative;
    getSettings(): ISimulationSettingsNative;
    private _addonInstance;
}
declare class SimulationSettings {
    constructor(jsonPath: string);
    internal(): ISimulationSettingsNative;
    private _addonInstance;
}
