#include "simulation_data.h"

#include "simulation_map.h"
#include "simulation_participant.h"

SimulationData::SimulationData()
{
    hop_data_ = std::unordered_map<std::string, std::vector<SimulationHop>>();
}

void SimulationData::RecordHop(SimulationParticipant* participant, SimulationHop hop)
{
    hop_data_[participant->Name()].push_back(hop);
}

int SimulationData::GetHopCount(const std::string& name)
{
    return hop_data_[name].size();
}
