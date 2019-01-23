#include "simulation_data.h"

#include "simulation_map.h"
#include "simulation_participant.h"

SimulationData::SimulationData()
{

}

void SimulationData::RecordHop(SimulationParticipant* participant, SimulationHop hop)
{
    hop_data_[participant->Name()].push_back(hop);
}

int SimulationData::GetHopCount(const std::string& name)
{
    return hop_data_[name].size();
}


/*
    Simulation Data N-API Wrapper
*/

SimulationDataWrap::SimulationDataWrap(const Napi::CallbackInfo& info) 
    : ObjectWrap(info)
{

}

Napi::Value SimulationDataWrap::GetHopCount(const Napi::CallbackInfo& info)
{
    Napi::Env env = info.Env();

    if(info.Length() < 1) 
    {
        Napi::TypeError::New(env, "Wrong number of arguments")
            .ThrowAsJavaScriptException();
        return env.Null();
    }

    if (!info[0].IsString())
    {
        Napi::TypeError::New(env, "Invalid participant!")
            .ThrowAsJavaScriptException();
        return env.Null();
    }

    Napi::String name = info[0].As<Napi::String>();
    auto hopCount = _internalInstance->GetHopCount(name.Utf8Value());

}

Napi::Function SimulationDataWrap::GetClass(Napi::Env env)
{
    return DefineClass(env, "SimulationData", {
        SimulationDataWrap::InstanceMethod("getHopCount", &SimulationDataWrap::GetHopCount)
    });
}

void SimulationDataWrap::Init(Napi::Env env, Napi::Object exports) 
{
    Napi::String name = Napi::String::New(env, "SimulationData");
    exports.Set(name, SimulationDataWrap::GetClass(env));
}