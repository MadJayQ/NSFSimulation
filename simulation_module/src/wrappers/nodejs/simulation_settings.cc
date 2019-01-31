#include "simulation_settings.h"

#include <napi.h>
#include <memory>
/*
    Wrapper object to N-API for the internal SimulationSettings class
*/
class SimulationSettingsWrap : public Napi::ObjectWrap<SimulationSettingsWrap>
{
public:
    //Ctor
    SimulationSettingsWrap(const Napi::CallbackInfo& info);

    //Access our internal simulation settings instance
    std::weak_ptr<SimulationSettings> GetInternalInstance() const;
    void AquireWeakReference(std::weak_ptr<SimulationSettings> weakPtr) { _internalInstance = weakPtr; }

    //Responsible for initializing our class 
    static void Init(Napi::Env env, Napi::Object exports);
    //Responsible for detailing the outline for our class to be referenced by the JavaScript runtime
    static Napi::Function GetClass(Napi::Env);
private:

    std::weak_ptr<SimulationSettings> _internalInstance;
};


std::weak_ptr<SimulationSettings> SimulationSettingsWrap::GetInternalInstance() const
{
    return _internalInstance;
}


SimulationSettingsWrap::SimulationSettingsWrap(const Napi::CallbackInfo& info) : ObjectWrap(info) {

    /*
    Napi::Env env = info.Env();

    if (info.Length() < 1) {
        Napi::TypeError::New(env, "Wrong number of arguments")
          .ThrowAsJavaScriptException();
        return;
    }

    if (!info[0].IsString()) {
        Napi::TypeError::New(env, "Please pass a settings path")
          .ThrowAsJavaScriptException();
        return;
    }
    */
}

void SimulationSettingsWrap::Init(Napi::Env env, Napi::Object exports) {
    Napi::String name = Napi::String::New(env, "SimulationSettings");
    exports.Set(name, SimulationSettingsWrap::GetClass(env));
}

Napi::Function SimulationSettingsWrap::GetClass(Napi::Env env) {
    return DefineClass(env, "SimulationSettings", {});
}