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
        auto newParticipant = std::make_unique<SimulationParticipant>(startNode, endNode, setting.Name);
        newParticipant->PreSimulationSetup();
        participantList->push_back(std::move(newParticipant));
    });
}


void SimulationWorld::RunSimulation(SimulationData* data)
{
    data->ResetClock();
    std::vector<SimulationParticipant*> activeParticiapnts; 
    for(auto participantItr = participants_.begin();
        participantItr != participants_.end();
        ++participantItr)
    {
        activeParticiapnts.push_back(participantItr->get());
    }
    while(!activeParticiapnts.empty())
    {
        for(auto participantItr = activeParticiapnts.begin();
            participantItr != activeParticiapnts.end();
            participantItr++)
        {
            auto participant = (*participantItr);
            participant->ParticipantThink(data);
            participant->ParticipantPostThink(data);
        }
        //Erase-Remove idiom
        activeParticiapnts.erase(
            std::remove_if(
                activeParticiapnts.begin(),
                activeParticiapnts.end(),
                [](SimulationParticipant* const & p) { return p->IsFinished(); }
            ),
            activeParticiapnts.end()
        );
        data->AdvanceClock(1.f);
    }
}