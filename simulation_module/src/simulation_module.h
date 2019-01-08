#pragma once

#include <napi.h>

#include <memory>

class CommandParser; //Forward declaration
class SimulationSettings;

class SimulationModule : public Napi::ObjectWrap<SimulationModule>
{
public:
    SimulationModule(const Napi::CallbackInfo&);
    Napi::Value Greet(const Napi::CallbackInfo&);

    void OnCommand(const Napi::CallbackInfo&);

    static Napi::Function GetClass(Napi::Env);

private:
    std::string _greeterName;
    std::unique_ptr<CommandParser> Commands;
};
