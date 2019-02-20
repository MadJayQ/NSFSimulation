
#include "wrappers/nodejs/simulation_module.cc"
//#include "wrappers/python/simulation_module.cc"

#include "simulation_common.hpp"
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
            "C:\\Users\\jakei_000\\Desktop\\NSFSimulation\\participants.json"
        ).get()

    );

    auto startTime = TimestampMS();
    World->RunSimulation(Data.get());
    auto endTime = TimestampMS();
    auto duration = (endTime - startTime);
    std::cout << "Simulation took: " << duration << " ms(real-time) " << Data->CurrentTime() << " (simulation-time)!" << std::endl;
    Data->ResetClock();
}

