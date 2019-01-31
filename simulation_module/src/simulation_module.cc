#include "simulation_module.h"
#include "simulation_map.h"
#include "simulation_settings.h"
#include "simulation_world.h"
#include "simulation_participant.h"
#include "simulation_data.h"

#include <json.hpp>

//#include "wrappers/nodejs/simulation_module.cc"
#include "wrappers/python/simulation_module.cc"

using json = nlohmann::json;

SimulationModule::SimulationModule() {
    
}


//This function is responsible for receiving commands and then handing them to the command parser
void SimulationModule::Initialize() {
    Settings = std::make_shared<SimulationSettings>();
    Data = std::make_shared<SimulationData>();
}

