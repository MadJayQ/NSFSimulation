
#include "wrappers/nodejs/simulation_module.cc"
//#include "wrappers/python/simulation_module.cc"

#include "simulation_world.h"
#include "simulation_map.h"
#include <iostream>

using json = nlohmann::json;

SimulationModule::SimulationModule() {
    
}


void SimulationModule::Initialize(const std::string& path) {
    Settings = std::make_shared<SimulationSettings>();
    Data = std::make_shared<SimulationData>();

    Settings->LoadSettingsFile(path);
    World = std::make_unique<SimulationWorld>(
        std::weak_ptr<SimulationSettings>(Settings)
    );

    World->SetCurrentMap("grid");
    World->InitializeParticipants(
        std::make_unique<SimulationParticipantSettings>(
            "F:\\Programming\\Work\\NSFSimulation\\participants.json"
        ).get()
    );

    World->RunSimulation(Data.get());

    std::cout << "World participants initialized." << std::endl;
}

