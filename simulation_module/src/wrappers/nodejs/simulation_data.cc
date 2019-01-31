#include "simulation_data.h"

#include <napi.h>
#include <memory>


class SimulationDataWrap : public Napi::ObjectWrap<SimulationDataWrap>
{
public:
    SimulationDataWrap(const Napi::CallbackInfo& info);

    std::weak_ptr<SimulationData> GetInternalInstance() const;
    void AquireWeakReference(std::weak_ptr<SimulationData> weakPtr) { _internalInstance = weakPtr; }

    Napi::Value GetHopCount(const Napi::CallbackInfo&);

    static void Init(Napi::Env env, Napi::Object exports);
    static Napi::Function GetClass(Napi::Env); 
private:
    std::weak_ptr<SimulationData> _internalInstance; 
};



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
    //auto hopCount = _internalInstance->GetHopCount(name.Utf8Value());

    return Napi::Number::New(env, 0.0);

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