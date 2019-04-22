#include "simulation_map.h"
#include "simulation_participant.h"

SimulationNode::SimulationNode(std::string key, const SimulationGraph* graph) 
    : key_(key), graph_(graph)
{
    weight_ = 1u;
}

void SimulationNode::ParticipantEnter(SimulationParticipant* participant)
{
    if(HasParticipant(participant->Name())) {
        throw "Participant is already in cell";
    }

    //Store a readonly pointer to our participant
    participants_[participant->Name()] = const_cast<const SimulationParticipant*>(participant);

    //Dispatch OnParticipantEnter event
}

void SimulationNode::ParticipantLeave(SimulationParticipant* participant)
{
    if(!HasParticipant(participant->Name())) {
        throw "Participant is not in the cell";
    } 

    participants_.erase(participant->Name());
}

bool SimulationNode::HasParticipant(const std::string& name) 
{
    return participants_.find(name) != participants_.end();
}

SimulationNode* SimulationNode::ShortestPath(const SimulationNode* dst)
{
    return graph_->ShortestPath(const_cast<const SimulationNode*>(this), dst);
}

std::list<const SimulationNode*> SimulationNode::ShortestPathAsList(const SimulationNode* dst)
{
    return graph_->ShortestPathAsList(const_cast<const SimulationNode*>(this), dst);
}
