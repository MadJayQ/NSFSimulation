#pragma once

#include <napi.h>

#include <memory>

#define UNPACK_ARGUMENT(type, name, container, pos) type* name = Napi::ObjectWrap<type>::Unwrap(container[pos].As<Napi::Object>());

class CommandParser; //Forward declaration
class SimulationSettings;
class SimulationSettingsWrap;
class SimulationWorld;

class SimulationModule : public Napi::ObjectWrap<SimulationModule>
{
public:
    SimulationModule(const Napi::CallbackInfo&);
    Napi::Value Greet(const Napi::CallbackInfo&);

    void OnCommand(const Napi::CallbackInfo&);
    void Initialize(const Napi::CallbackInfo&);

    static Napi::Function GetClass(Napi::Env);

    Napi::Value GetSettings(const Napi::CallbackInfo&);


private:
    std::string _greeterName;
    std::unique_ptr<CommandParser> Commands;
    std::unique_ptr<SimulationWorld> World;

    Napi::Reference<Napi::Object> SettingsRef;
};
