#pragma once

#include "simulation_math.hpp"
#include "simulation_common.hpp"

#include <memory>
#include <unordered_map>

class SimulationGraph; //Forward declaration for simul
class SimulationSettings; //
class SimulationParameters;
class SimulationParticipantSettings;
class SimultionParticipant;

class SimulationMap {
public:
    SimulationMap(const std::string& mapFile);
    SimulationMap() {}

    SimulationGraph* operator ->() { return World.get(); }

    std::string Name;
    std::unique_ptr<SimulationGraph> World;
};

class SimulationWorld 
{
public:
    SimulationWorld(std::weak_ptr<SimulationSettings> settings);

    void SetCurrentMap(const std::string& map);
    void InitializeParticipants(SimulationParticipantSettings* settings);

public:
    int width;
    int height; 
private:
    std::unordered_map<std::string, SimulationMap> maps_; 
    
    SimulationMap* current_map_= nullptr;
    SimulationParameters* paramaters_;

    std::vector<std::unique_ptr<SimultionParticipant>> participants_;
    
};