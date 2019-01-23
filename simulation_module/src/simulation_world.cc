#include "simulation_world.h"

#include "simulation_settings.h"
#include "simulation_map.h"
#include "simulation_participant.h"
#include "simulation_data.h"

SimulationWorld::SimulationWorld(std::weak_ptr<SimulationSettings> settings)
{
    auto settingsLock = settings.lock(); //Lock a temporary reference to our shared settings resource.
    width = settingsLock->width; //Initialize width and height
    height = settingsLock->height;
    paramaters_ = settingsLock->Parameters(); //Store a pointer to our simulation parameters. 
    maps_ = std::unordered_map<std::string, SimulationMap>();
    auto mapCollection = settingsLock->Maps();
    for(auto itr = mapCollection->MapFiles.begin(); 
        itr != mapCollection->MapFiles.end(); ++itr) {
            maps_.emplace(std::make_pair(itr->first, SimulationMap(itr->second)));
    }
    settingsLock.reset(); //Release our reference
}

SimulationMap::SimulationMap(const std::string& mapFilePath) {
    World = std::make_unique<SimulationGraph>(mapFilePath);
}

void SimulationWorld::SetCurrentMap(const std::string& map)
{
    current_map_ = &maps_[map];
}

void SimulationWorld::InitializeParticipants(SimulationParticipantSettings* settings) 
{
    SimulationMap* map = current_map_; //Push our current map pointer onto local stack
    std::vector<std::unique_ptr<SimulationParticipant>>* participantList = &participants_; //Push a pointer to our participants list onto the local stack 
    if(map == nullptr) {
        throw NoValidMapException();
    }
    //HACK HACK(Jake): Honestly I thought lambdas would be be optimal for this, I was definitely wrong.
    //This is some hackatry right here
    settings->ForEach([&](SimulationParticipantSetting setting) -> void {
        auto startNode = (*map)->GetNode(setting.StartKey);
        auto endNode = (*map)->GetNode(setting.EndKey);

        if(!startNode || !endNode) {
            return; //TODO(Jake): We should throw an exception here instead
        }

        participantList->push_back(std::make_unique<SimulationParticipant>(startNode, endNode, setting.Name));
    });
}

void SimulationWorld::RunSimulation(SimulationData* data)
{
    for(auto participantItr = participants_.begin();
        participantItr != participants_.end(); 
        ++participantItr)
    {
        (*participantItr)->ParticipantThink(data);
    }
}