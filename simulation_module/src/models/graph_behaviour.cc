  #include "simulation_behaviour.h"

#include "../simulation_participant.h"
#include "../simulation_map.h"
#include "../simulation_job.h"
#include "../simulation_data.h"
#include "../combinations.h"

#include "../simulation_common.hpp"


static float s_cumulativeProbability;

struct probability_solver
{
    float cumulativeProbability;
    std::vector<SimulationParticipant *> *allParticipantsMinusThis;
    SimulationParticipant *thisCar;
    SimulationEdge *currentEdge;
    SimulationBehaviour* behaviour;
    float t;

    bool operator()(std::vector<SimulationParticipant *>::const_iterator first, std::vector<SimulationParticipant *>::const_iterator last)
    {
        std::vector<SimulationParticipant *> A;
        std::vector<SimulationParticipant *> ANot;
        if (first != last)
        {
            A.push_back(*first);
            for (++first; first != last; ++first)
                A.push_back(*first);
        }
        for (auto participant : *allParticipantsMinusThis)
        {
            if (std::find(A.begin(), A.end(), participant) == A.end())
            {
                ANot.push_back(participant);
            }
        }

        float tempProb = 1.f;
        float tempNotProb = 1.f;
        for (auto participant : A)
        {
            tempProb *= behaviour->CalculateProbability(currentEdge, participant);
        }
        for (auto participant : ANot)
        {
            tempNotProb *= (1.f - behaviour->CalculateProbability(currentEdge, participant));
        }
        s_cumulativeProbability += (tempProb * tempNotProb);
        return false;
    }
};

void GraphBehaviour::CalculateExpectedUtility(SimulationData *data,
                                              SimulationParticipant *participant)
{
    auto dstNode = participant->Location()->ShortestPath(
        participant->Destination()
    ); //Default to closest path
    auto graph = const_cast<SimulationGraph *>(participant->Location()->GetGraph());
    auto allParticipants = graph->GetParticipants({});
    auto allParticipantsMinusThis = graph->GetParticipants({participant});
    auto adjacencyList = participant->Location()->EdgeList;
    auto N = allParticipants.size();
    auto t = data->GetTime(); //Current simulation timestamp
    SimulationEdge *bestEdge = nullptr;
    float bestUtility = 0.f;
    auto start = TimestampMS();
    if(participant->ShouldTrace())
        participant->BeginTrace(participant);
    for (auto &node : adjacencyList) //Foreach adjacent node
    {
        float expectedUtility = 0.f; //Our expected utility
        for (int i = 1; i <= N; i++) //For i = 1 ... N
        {
            float utility = (float)(*node)->GetBudget() / powf(i, 2); //(float)i / powf((float)(*node)->GetBudget(), 2.f); //U(i) = i / R^2
            float cumulativeProbability = 0.f;
            if (i == 1) //If we're only calculating the utility for 1 car, it is our probability times the probability that no one else will be there
            {
                float p = 1.0; //We assume that our car is here
                float cumulativeOtherProbability = 1.f;
                for (auto participant : allParticipantsMinusThis)
                {
                    cumulativeOtherProbability *= (1.f - CalculateProbability(node, participant));
                }
                cumulativeProbability = p * cumulativeOtherProbability;
            }
            else if (i == N || i == N - 1) //If we're calculating the probability of all the cars being there, sample all of their probability curves
            {
                cumulativeProbability = 1.f;
                for (auto participant : allParticipants)
                {
                    cumulativeProbability *= CalculateProbability(node, participant);
                }
            }
            else //Use our super high time complexity algorithm
            {
                probability_solver prob;
                s_cumulativeProbability = 0.f;
                prob.allParticipantsMinusThis = &allParticipantsMinusThis;
                prob.thisCar = participant;
                prob.behaviour = this;
                prob.currentEdge = node;
                prob.t = t;
                for_each_combination(allParticipantsMinusThis.begin(), allParticipantsMinusThis.begin() + (i - 1), allParticipantsMinusThis.end(), prob);
                cumulativeProbability = s_cumulativeProbability;
            }
            expectedUtility += cumulativeProbability * utility; //If we get 0 then we just take all of the utility
            if (participant->ShouldTrace())
                participant->TraceEdgeIteration(node, i, cumulativeProbability, (*node)->GetBudget(), expectedUtility, (i == N));
        }
        if (expectedUtility > bestUtility)
        {
            bestUtility = expectedUtility;
            bestEdge = node;
        }
    }
    auto end = TimestampMS();
    if (participant->ShouldTrace())
    {
        participant->EndTrace(participant, bestEdge, bestUtility);
    }
    //std::cout << "Itr took: " << (end - start) << " MS!" << std::endl;
    if (bestEdge != nullptr)
    {
        data->RecordHop(participant, std::make_pair(participant->Location(), bestEdge->Destination()));
        participant->MoveTo(bestEdge, data);
    }
}

float GraphBehaviour::CalculateProbability(SimulationEdge *edge,
                                           SimulationParticipant *participant)
{
    if(participant->Task() == nullptr)
    {
        return 0.f;
    }
    auto prob = participant->Task()->ProbabilityOfArrival(
        edge->Destination()
    );

    return prob;
}