#pragma once

#include "simulation_common.hpp"
#include "simulation_job.h"

#include <functional>

class SimulationNode; //Forward declaration
class SimulationData;
class TraversalJob;
class SimulationEdge;
class SimulationBehaviour;

struct SimulationParticipantSetting
{
    std::string Name;
    std::string StartKey;
    std::string EndKey;
};

/*  TODO(Jake): Honestly, I think that participants should be stored in a database but that's just me.
*   SimualtionParticipantSettings Class
*   -----------------------------------
*   This class describes the layout of the participants.json file, parsing each of the individual participants and their data
*/
class SimulationParticipantSettings
{
public:
    SimulationParticipantSettings(const std::string& participantsFile);

    void ForEach(std::function<void(const SimulationParticipantSetting&)> function) { 
        for(auto setting : settings_) {
            function(setting);
        }
    }
private:
    std::vector<SimulationParticipantSetting> settings_;
};

/*
*   SimulationParticipant Class
*   ---------------------------
*   This class describes a given participant that is actively participating in a simulation
*
*/

class SimulationParticipant
{
public:
    SimulationParticipant();
    explicit SimulationParticipant(SimulationNode*, SimulationNode*, const std::string& name);

    void MoveTo(SimulationEdge* edge, SimulationData* data);
    void PreSimulationSetup();
    void ParticipantThink(SimulationData* data);
    void ParticipantPostThink(SimulationData* data);

    std::string Name() const { return name_; }
    bool IsFinished() const { return isFinished_; }
    bool ShouldTrace() const { return trace_; }
    void ToggleTrace(bool trace) { trace_ = trace; }

    void PreSimulationSetup(SimulationBehaviour* behaviour);

    void TraceEdgeIteration(SimulationEdge* edge, int n, float prob, float reward, float utility, bool finalItr);
    void EndTrace(SimulationParticipant* participant, SimulationEdge* bestEdge, float utility);
    void BeginTrace(SimulationParticipant* part);

    SimulationNode* Location() const { return current_node_; }
    SimulationNode* Destination() const { return destination_node_; }
    TraversalJob* Task() const { return current_job_.get(); }

    void TeleportTo(SimulationNode* node, SimulationData* data);

    int Capacity;

private:
    void OnTraversalComplete(TraversalJob* job, SimulationData* data);
private:
    SimulationNode* current_node_; //Where we are
    SimulationNode* destination_node_; //Where we're trying to go
    SimulationBehaviour* behaviour_;
    std::string name_; //The name of our participant
    bool isFinished_;


    bool trace_ = false;

    std::unique_ptr<TraversalJob> current_job_;
};