#pragma once

#include <memory>
#include <string>

class SimulationSettings;
class SimulationWorld;
class SimulationData;

class SimulationModule
{
public:
    SimulationModule();

    void Initialize(const std::string& path);

    std::unique_ptr<SimulationWorld>    World; //Internal world pointer
    std::shared_ptr<SimulationSettings> Settings;
    std::shared_ptr<SimulationData> Data;
};
