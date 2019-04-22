#include "simulation_behaviour.h"

#include "../simulation_participant.h"
#include "../simulation_map.h"
#include "../simulation_job.h"
#include "../simulation_data.h"
#include "../combinations.h"

#include "../simulation_common.hpp"

int NCR(int n, int r)
{
    if (r == 0)
        return 1;

    /*
     Extra computation saving for large R,
     using property:
     N choose R = N choose (N-R)
    */
    if (r > n / 2)
        return NCR(n, n - r);

    long res = 1;

    for (int k = 1; k <= r; ++k)
    {
        res *= n - k + 1;
        res /= k;
    }

    return res;
}

void SimulationBehaviour::InitialTick(SimulationData *data, SimulationParticipant *participant)
{
    CalculateExpectedUtility(data, participant);
}

void GridBehaviour::CalculateExpectedUtility(SimulationData *data,
                                             SimulationParticipant *participant)
{
    //Use the old model here
    auto dstNode = participant->Location()->ShortestPath(
        participant->Destination());

    auto graph = const_cast<SimulationGraph *>(participant->Location()->GetGraph());
    auto adjacencyList = participant->Location()->EdgeList;
    auto t = data->GetTime(); //Current simulation timestamp
    SimulationEdge *bestEdge = nullptr;
    float bestUtility = 0.f;
    auto start = TimestampMS();
    if (participant->ShouldTrace())
        participant->BeginTrace(participant);

    std::sort(adjacencyList.begin(), adjacencyList.end(), [](SimulationEdge *a, SimulationEdge *b) {
        return a->Destination()->GetBudget() > b->Destination()->GetBudget();
    });

    for (auto &node : adjacencyList)
    {
        auto N = graph->GetAdjacentParticipants(node->Destination(), {}).size();
        float expectedUtility = 0.f;
        if (N == 0)
        {
            expectedUtility = (*node)->GetBudget();
        }
        else
        {
            for (int i = 1; i <= N; i++)
            {
                auto neighbors = N + 1;
                float utility = (float)(*node)->GetBudget() / powf(i, 2);
                float cumulativeProbability = 0.f;
                auto pnumer = NCR(N - 1, i - 1);
                auto pdenomSum = 0;
                for (int j = 1; j <= N; j++)
                {
                    pdenomSum += NCR(N - 1, j - 1);
                }
                float probability = (float)((float)pnumer / (float)pdenomSum);
                expectedUtility += (utility * probability);
                if (participant->ShouldTrace())
                {
                    participant->TraceEdgeIteration(node, i, probability, (*node)->GetBudget(), expectedUtility, (i == N));
                }
            }
        }
        if (expectedUtility > bestUtility)
        {
            if (participant->Capacity < expectedUtility)
            {
                continue;
            }
            bestUtility = expectedUtility;
            bestEdge = node;
        }
    }
    auto end = TimestampMS();
    //std::cout << "Itr took: " << (end - start) << " MS!" << std::endl;
    if (bestEdge != nullptr)
    {
        if (participant->ShouldTrace())
        {
            participant->EndTrace(participant, bestEdge, bestUtility);
        }
        participant->Capacity -= bestUtility;
        data->RecordHop(participant, std::make_pair(participant->Location(), bestEdge->Destination()));
        participant->TeleportTo(bestEdge->Destination(), data);
    }
    else
    {
        //std::cout << "Car " << participant->Name() << " is taking the shortest path!" << std::endl;
        data->RecordHop(participant, std::make_pair(participant->Location(), dstNode));
        participant->TeleportTo(dstNode, data);
    }
}

float GridBehaviour::CalculateProbability(SimulationEdge *edge,
                                          SimulationParticipant *participant)
{
    return 0.f;
}