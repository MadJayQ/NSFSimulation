#pragma once

#include <napi.h>

#include <memory>

#define UNPACK_ARGUMENT(type, name, container, pos) type* name = Napi::ObjectWrap<type>::Unwrap(container[pos].As<Napi::Object>());

class CommandParser; //Forward declaration
class SimulationSettings;
class SimulationSettingsWrap;
class SimulationWorld;
class SimulationData;

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
    std::unique_ptr<CommandParser> Commands; //TODO(Jake): Determine whether or not this is even neccesary? 
    std::unique_ptr<SimulationWorld> World; //Internal world pointer
    std::unique_ptr<SimulationData> Data;

    Napi::Reference<Napi::Object> SettingsRef; //NodeJS Reference to our settings object, this is exposed to NodeJS
    Napi::Reference<Napi::Object> DataRef; //NodeJS Reference to our Data Collection module, this is exposed to NodeJS
};
