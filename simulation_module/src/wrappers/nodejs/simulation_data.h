#pragma once

#include <napi.h>
#include <memory>

class SimulationData;

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

