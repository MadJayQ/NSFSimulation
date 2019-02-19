#pragma once

#include "simulation_common.hpp"

#include <functional>

class SimulationNode; //Forward declaration
class SimulationData;

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

    void MoveTo(SimulationNode* dst);
    void PreSimulationSetup();
    void ParticipantThink(SimulationData* data);
    void ParticipantPostThink(SimulationData* data);

    std::string Name() const { return name_; }
    bool IsFinished() const { return isFinished_; }
    float SampleProbabilityCurve(float time);
    
private:
    SimulationNode* current_node_; //Where we are
    SimulationNode* destination_node_; //Where we're trying to go
    std::string name_; //The name of our participant
    bool isFinished_;
};