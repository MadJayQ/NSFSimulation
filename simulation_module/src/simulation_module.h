#pragma once

#include <memory>

class SimulationSettings;
class SimulationWorld;
class SimulationData;

class SimulationModule
{
public:
    SimulationModule();

    void Initialize();

    std::unique_ptr<SimulationWorld>    World; //Internal world pointer
    std::shared_ptr<SimulationSettings> Settings;
    std::shared_ptr<SimulationData> Data;
};
