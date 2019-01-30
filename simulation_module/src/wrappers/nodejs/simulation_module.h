#pragma once

#include <napi.h>

#include <memory>

#define UNPACK_ARGUMENT(type, name, container, pos) type* name = Napi::ObjectWrap<type>::Unwrap(container[pos].As<Napi::Object>());

class SimulationModule;

class SimulationModuleWrap : public Napi::ObjectWrap<SimulationModuleWrap>
{
public:
    SimulationModuleWrap(const Napi::CallbackInfo&);

    void Initialize(const Napi::CallbackInfo&);

    static Napi::Function GetClass(Napi::Env);

    Napi::Value GetSettings(const Napi::CallbackInfo&);
    Napi::Value GetData(const Napi::CallbackInfo&);

    Napi::Reference<Napi::Object> SettingsRef; //NodeJS Reference to our settings object, this is exposed to NodeJS
    Napi::Reference<Napi::Object> DataRef; //NodeJS Reference to our Data Collection module, this is exposed to NodeJS

private:
    std::unique_ptr<SimulationModule> module_;
};
