
//#include "wrappers/nodejs/simulation_module.cc"
#include "wrappers/python/simulation_module.cc"

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

    std::cout << "World participants initialized." << std::endl;
    

    
}
