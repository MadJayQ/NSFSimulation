#pragma once

#include "simulation_common.hpp"


#include <functional>

class SimulationParticipant;
class SimulationData;
class SimulationEdge; 
class SimulationNode;

class SimulationJob;
using JobFinishCallback = std::function<void(SimulationJob*, SimulationData*)>;

class SimulationJob 
{
public:
    SimulationJob(SimulationParticipant* participant, SimulationData* data, float duration);
    SimulationJob(SimulationParticipant* participant, SimulationData* data, float duration, JobFinishCallback onComplete);
    SimulationJob() {}
    virtual void Process(float deltaTime);
protected:
    SimulationParticipant* participant_;
    SimulationData* currentData_;
    float duration_;
    float durationComplete_;
    
    JobFinishCallback onComplete_; 
};

class TraversalJobInitializer
{
public:
    TraversalJobInitializer() {}
    TraversalJobInitializer(SimulationEdge* edge);
protected:
    float duration;
};


class TraversalJob : public TraversalJobInitializer, SimulationJob
{
public:
    TraversalJob(SimulationParticipant*, SimulationData*, SimulationEdge* edge, JobFinishCallback);
    TraversalJob(){}
    ~TraversalJob() {}
    void Process(float deltaTime) override;
    float ProbabilityOfArrival(SimulationNode* node = nullptr);

    SimulationNode* Destination();
private:
    SimulationEdge* edge_;
};