#include "simulation_participant.h"
#include "simulation_map.h"

#include "simulation_data.h"

SimulationParticipant::SimulationParticipant()
{
    //Uhhhh?
    current_node_ = nullptr;
    destination_node_ = nullptr; 
}

SimulationParticipant::SimulationParticipant(SimulationNode* node, SimulationNode* dst, const std::string& name) 
    : current_node_(node), destination_node_(dst), name_(name)
{
    current_node_->ParticipantEnter(this);
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

void SimulationParticipant::PreSimulationSetup()
{
    isFinished_ = false; //
}

void SimulationParticipant::MoveTo(SimulationNode* dst) 
{
    if(current_node_)
    {
        current_node_->ParticipantLeave(this);
    }
    dst->ParticipantEnter(this);
    current_node_ = dst;
}

void SimulationParticipant::ParticipantThink(SimulationData* data)
{
    auto dstNode = current_node_->ShortestPath(destination_node_);
    data->RecordHop(this, std::make_pair(current_node_, dstNode));
    MoveTo(dstNode);
}


void SimulationParticipant::ParticipantPostThink(SimulationData* data)
{
    if(current_node_ == destination_node_)
    {
        isFinished_ = true;
    }
}