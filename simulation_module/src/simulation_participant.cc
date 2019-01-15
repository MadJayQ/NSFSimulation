#include "simulation_participant.h"

SimulationParticipant::SimulationParticipant()
{
    //Uhhhh?
    current_node_ = nullptr;
    destination_node_ = nullptr; 
}

SimulationParticipant::SimulationParticipant(SimulationNode* node, SimulationNode* dst) 
    : current_node_(node), destination_node_(dst)
{

}

SimulationParticipantSettings::SimulationParticipantSettings(const std::string& participantsFile)
{
    auto participantsJson = ReadJsonFile(participantsFile);
    for(auto itr = participantsJson.begin(); itr != participantsJson.end(); ++itr) 
    {
        SimulationParticipantSetting setting;
        setting.Name = itr.key();
        setting.StartKey = READ_JSON_RET(participantsJson[itr.key()], startKey, std::string);
        setting.EndKey = READ_JSON_RET(participantsJson[itr.key()], endKey, std::string);

        settings_.push_back(setting);
    }
}
