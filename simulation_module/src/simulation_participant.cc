#include "simulation_participant.h"
#include "simulation_map.h"
#include "simulation_job.h"
#include "simulation_data.h"
#include "combinations.h"
#include "models/simulation_behaviour.h"

#include "simulation_common.hpp"


#include <iostream>

SimulationParticipant::SimulationParticipant()
{
    //Uhhhh?
    current_node_ = nullptr;
    destination_node_ = nullptr;
}

SimulationParticipant::SimulationParticipant(SimulationNode *node, SimulationNode *dst, const std::string &name)
    : current_node_(node), destination_node_(dst), name_(name)
{
    current_node_->ParticipantEnter(this);
}

SimulationParticipantSettings::SimulationParticipantSettings(const std::string &participantsFile)
{
    auto participantsJson = ReadJsonFile(participantsFile);
    for (auto itr = participantsJson.begin(); itr != participantsJson.end(); ++itr)
    {
        SimulationParticipantSetting setting;
        setting.Name = itr.key();
        setting.StartKey = READ_JSON_RET(participantsJson[itr.key()], startKey, std::string);
        setting.EndKey = READ_JSON_RET(participantsJson[itr.key()], endKey, std::string);

        settings_.push_back(setting);
    }
}

void SimulationParticipant::TeleportTo(SimulationNode* node, SimulationData* data)
{
    if(current_node_)
    {
        current_node_->ParticipantLeave(this);
    }

    node->ParticipantEnter(this);
    current_node_ = node;

    current_job_ = nullptr;
}

void SimulationParticipant::PreSimulationSetup()
{
    isFinished_ = false; //
}

void SimulationParticipant::MoveTo(SimulationEdge *edge, SimulationData* data)
{

    JobFinishCallback cb = [this](SimulationJob* job, SimulationData* data) -> void
    {
        OnTraversalComplete(reinterpret_cast<TraversalJob*>(job), data);
    };
    current_job_.reset(
        new TraversalJob(this, data, edge, cb)
    );
}




void SimulationParticipant::OnTraversalComplete(TraversalJob *job, SimulationData *data)
{
    if (current_node_)
    {
        current_node_->ParticipantLeave(this);
    }


    auto dst = job->Destination();
    dst->ParticipantEnter(this);
    current_node_ = dst;

    behaviour_->CalculateExpectedUtility(data, this); //Start a new job
}


void SimulationParticipant::BeginTrace(SimulationParticipant* part)
{
    std::cout << "Begining trace table for participant " << part->Name() << std::endl;
    std::cout << center("edge", 15) << " | " << center("n", 15) << " | " << center("prob", 15) << " | " << center("reward", 15) << " | " << center("E(U)", 15) << "\n";
}
void SimulationParticipant::TraceEdgeIteration(SimulationEdge* edge, int n, float prob, float reward, float utility, bool finalItr)
{
    auto edgeName = edge->Source()->Key() + "->" + edge->Destination()->Key();
    if(finalItr)
    {
        edgeName += "*";
    }
    std::cout << center(edgeName, 15) << " | " << prd((double)n, 0, 15) << " | " << prd(prob, 12, 15) << " | " << prd(reward, 0, 15) << " | " << prd(utility, 12, 15) << "\n";  
}

void SimulationParticipant::EndTrace(SimulationParticipant* participant, SimulationEdge* bestEdge, float utility)
{
    auto edgeName = bestEdge->Source()->Key() + "->" + bestEdge->Destination()->Key();
    std::cout << "Car " << participant->Name() << " is traversing along " << edgeName << std::endl; 
}

void SimulationParticipant::PreSimulationSetup(SimulationBehaviour* behaviour)
{
    behaviour_ = behaviour;
    Capacity = 2500;
}


void SimulationParticipant::ParticipantThink(SimulationData *data)
{
    //Participants should always have a job, if they don't they are just being set up
    //TODO(Jake): Also when a participant is done collecting they probably shouldn't have a job either
    if (current_job_ == nullptr) //Initial setup
    {
        behaviour_->InitialTick(data, this);
    }
    else
    {
        current_job_->Process(data->GetDeltaTime());
    }
}


void SimulationParticipant::ParticipantPostThink(SimulationData *data)
{
    if (current_node_ == destination_node_)
    {
        isFinished_ = true;
    }
}