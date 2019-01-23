#pragma once

#include <napi.h>
#include <json.hpp>

#include <memory>
#include <unordered_map>

#include "simulation_common.hpp"

/*
    SimulationData class
    This class stores the recorded data for the simulation results
*/

class SimulationParticipant;
class SimulationNode;

using SimulationHop = std::pair<SimulationNode*, SimulationNode*>;

class SimulationData
{
public:
    explicit SimulationData();
    void RecordHop(SimulationParticipant* participant, SimulationHop hop);
    int GetHopCount(const std::string& name);
private:
    std::unordered_map<std::string, std::vector<SimulationHop>> hop_data_;
};

class SimulationDataWrap : Napi::ObjectWrap<SimulationDataWrap>
{
public:
    SimulationDataWrap(const Napi::CallbackInfo& info);

    SimulationData* GetInternalInstance() { return _internalInstance.get(); }

    Napi::Value GetHopCount(const Napi::CallbackInfo&);

    static void Init(Napi::Env env, Napi::Object exports);
    static Napi::Function GetClass(Napi::Env); 
private:
    std::shared_ptr<SimulationData> _internalInstance; 
};

