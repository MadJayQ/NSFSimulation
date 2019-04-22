#include "simulation_data.h"

#include "simulation_map.h"
#include "simulation_participant.h"

#include <algorithm>
#include <iostream>
#include <iterator>
#include <string>
#include <vector>


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

int SimulationData::GetHops()
{
    int totalHops = 0;
    for(auto hop : hop_data_)
    {
        totalHops += hop.second.size();
    }
    return totalHops;
}

float SimulationData::GetCoverage(int totalNodes)
{
    std::vector<std::string> visits = {};
    for(auto participantHops : hop_data_)
    {
        for(auto hop : participantHops.second)
        {
            visits.push_back(hop.second->Key());
        }
        std::unique(visits.begin(), visits.end(), [](std::string a, std::string b)
        {
            return !a.compare(b);
        });
    }

    return (float)visits.size() / (float)totalNodes;

}
