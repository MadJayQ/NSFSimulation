#include "simulation_job.h"
#include "simulation_data.h"
#include "simulation_map.h"
#include "simulation_participant.h"

SimulationJob::SimulationJob(SimulationParticipant *participant, SimulationData *data, float duration)
    : participant_(participant), currentData_(data), duration_(duration)
{
    durationComplete_ = 0.f;
}

SimulationJob::SimulationJob(SimulationParticipant *participant,
                             SimulationData *data, float duration,
                             JobFinishCallback onComplete) : participant_(participant), currentData_(data), duration_(duration), onComplete_(onComplete)
{

}

void SimulationJob::Process(float deltaTime)
{
    durationComplete_ += deltaTime;

    if (durationComplete_ >= duration_)
    {
        onComplete_(this, currentData_);
    }
}

TraversalJobInitializer::TraversalJobInitializer(SimulationEdge *edge)
{
    float distance = edge->Distance();
    float speed = edge->SpeedSample();

    duration = distance / speed;
}

TraversalJob::TraversalJob(SimulationParticipant *participant, SimulationData *data,
                           SimulationEdge *edge, JobFinishCallback onComplete)
    : TraversalJobInitializer(edge),
      SimulationJob(participant, data, duration, onComplete)
{
    edge_ = edge;
    durationComplete_ = 0.f;
}

void TraversalJob::Process(float deltaTime)
{
    SimulationJob::Process(deltaTime);
}

float TraversalJob::ProbabilityOfArrival(SimulationNode* src)
{
    float speed = edge_->SpeedSample();
    float distanceProbability = durationComplete_ * speed;
    float distance = edge_->Distance();
    if(src != nullptr)
    {
        auto path = edge_->Source()->ShortestPathAsList(src);
        distance = distance + (distance * path.size());
    }
    float prob = (distanceProbability > 0.f) ? distanceProbability / distance : 0.f;

    return prob; //How far we need to go over how far we've probably gone
}

SimulationNode* TraversalJob::Destination()
{
    return edge_->Destination();
}
