#pragma once

#include <napi.h>
#include <json.hpp>

class SimulationSettings
{
public:
    SimulationSettings(const std::string& settingsPath);

public:
    int width, height;
};

class SimulationSettingsWrap : public Napi::ObjectWrap<SimulationSettingsWrap>
{
public:
    //Ctor
    SimulationSettingsWrap(const Napi::CallbackInfo& info);

    //Access our internal simulation settings instance
    SimulationSettings* GetInternalInstance() const;

    //Responsible for initializing our class 
    static void Init(Napi::Env env, Napi::Object exports);
    //Responsible for detailing the outline for our class to be referenced by the JavaScript runtime
    static Napi::Function GetClass(Napi::Env);

private:

    std::unique_ptr<SimulationSettings> _internalInstance;


};