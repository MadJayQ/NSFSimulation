#include "simulation_participant.h"
#include "simulation_map.h"

#include "simulation_data.h"
#include "combinations.h"

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

void SimulationParticipant::PreSimulationSetup()
{
    isFinished_ = false; //
}

void SimulationParticipant::MoveTo(SimulationNode *dst)
{
    if (current_node_)
    {
        current_node_->ParticipantLeave(this);
    }
    dst->ParticipantEnter(this);
    current_node_ = dst;
}

struct probability_solver
{
    float cumulativeProbability;
    std::vector<SimulationParticipant*>* allParticipantsMinusThis;
    SimulationParticipant* thisCar;
    float t;

    bool operator()(std::vector<SimulationParticipant*>::const_iterator first, std::vector<SimulationParticipant*>::const_iterator last)
    {
        std::vector<SimulationParticipant*> A;
        std::vector<SimulationParticipant*> ANot;
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

        float tempProb = thisCar->SampleProbabilityCurve(t);
        float tempNotProb = 1.f;
        for(auto participant : A)
        {
            tempProb *= participant->SampleProbabilityCurve(t);
        }
        for(auto participant : ANot)
        {
            tempNotProb *= (1.f - participant->SampleProbabilityCurve(t));
        }
        cumulativeProbability += (tempProb * tempNotProb);
        return false;
    }
};

void
SimulationParticipant::ParticipantThink(SimulationData *data)
{
    auto dstNode = current_node_->ShortestPath(destination_node_); //Default to closest path
    auto graph = const_cast<SimulationGraph *>(current_node_->GetGraph());
    auto allParticipants = graph->GetParticipants({});
    auto allParticipantsMinusThis = graph->GetParticipants({this});
    auto adjacencyList = current_node_->AdjacencyList;
    auto N = allParticipants.size();
    auto t = data->GetTime();        //Current simulation timestamp
    SimulationNode* bestNode = nullptr;
    float bestUtility = 0.f;
    for (auto &node : adjacencyList) //Foreach adjacent node
    {
        float expectedUtility = 0.f; //Our expected utility
        for (int i = 1; i <= N; i++) //For i = 1 ... N
        {
            float utility = (float)i / powf((float)node->GetBudget(), 2.f); //U(i) = i / R^2
            float cumulativeProbability = 0.f;
            if (i == 1) //If we're only calculating the utility for 1 car, it is our probability times the probability that no one else will be there
            {
                float p = this->SampleProbabilityCurve(t);
                float cumulativeOtherProbability = 1.f;
                for (auto participant : allParticipantsMinusThis)
                {
                    cumulativeOtherProbability *= (1.f - participant->SampleProbabilityCurve(t));
                }
                cumulativeProbability = p * cumulativeOtherProbability;
            }
            else if (i == N || i == N - 1) //If we're calculating the probability of all the cars being there, sample all of their probability curves
            {
                cumulativeProbability = 1.f;
                for (auto participant : allParticipants)
                {
                    cumulativeProbability *= participant->SampleProbabilityCurve(t);
                }
            }
            else //Use our super high time complexity algorithm
            {
                probability_solver prob;
                prob.cumulativeProbability = 0.f;
                prob.allParticipantsMinusThis = &allParticipantsMinusThis;
                prob.thisCar = this;
                prob.t = t;
                for_each_combination(allParticipantsMinusThis.begin(), allParticipantsMinusThis.begin() + (i - 1), allParticipantsMinusThis.end(), prob);
                cumulativeProbability = prob.cumulativeProbability;
            }
            expectedUtility += cumulativeProbability * utility;
        }
        if(expectedUtility > bestUtility)
        {
            bestUtility = expectedUtility;
            bestNode = node;
        }
    }

    if(bestNode != nullptr)
    {
        dstNode = bestNode;
    }

    data->RecordHop(this, std::make_pair(current_node_, dstNode));
    MoveTo(dstNode);
}

float SimulationParticipant::SampleProbabilityCurve(float t)
{
    //Sample our distribution at a random point
    return s_dist(s_randomNoise);
}

void SimulationParticipant::ParticipantPostThink(SimulationData *data)
{
    if (current_node_ == destination_node_)
    {
        isFinished_ = true;
    }
}