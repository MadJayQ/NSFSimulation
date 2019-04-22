#pragma once


class SimulationParticipant;
class SimulationData;
class SimulationEdge;

class TraversalJob;

class SimulationBehaviour 
{
public:
    virtual void CalculateExpectedUtility(SimulationData* data, SimulationParticipant* participant) = 0;
    virtual float CalculateProbability(SimulationEdge* edge, SimulationParticipant* participant) = 0;
    virtual void InitialTick(SimulationData* data, SimulationParticipant* participant);
};

class GridBehaviour : public SimulationBehaviour
{
public:
    void CalculateExpectedUtility(SimulationData* data, SimulationParticipant* participant) override;
    float CalculateProbability(SimulationEdge* edge, SimulationParticipant* participant) override;
};

class GraphBehaviour : public SimulationBehaviour
{
public:
    void CalculateExpectedUtility(SimulationData* data, SimulationParticipant* participant) override;
    float CalculateProbability(SimulationEdge*, SimulationParticipant* participant) override;
};