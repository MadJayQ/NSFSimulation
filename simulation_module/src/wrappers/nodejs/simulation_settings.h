#pragma once

#include <napi.h>
#include <memory>

class SimulationSettings;
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