#include "simulation_data.h"
#include "../simulation_data.h"

/*
    Simulation Data N-API Wrapper
*/

SimulationDataWrap::SimulationDataWrap(const Napi::CallbackInfo& info) 
    : ObjectWrap(info)
{
    _internalInstance = std::make_unique<SimulationData>();
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
    //auto hopCount = _internalInstance->GetHopCount(name.Utf8Value());

    return Napi::Number::New(env, (double)hopCount);

}

std::weak_ptr<SimulationData> SimulationDataWrap::GetInternalInstance() const
{
    return _internalInstance;
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