#include "simulation_settings.h"

#include "../simulation_settings.h"

std::weak_ptr<SimulationSettings> SimulationSettingsWrap::GetInternalInstance() const
{
    return _internalInstance;
}


SimulationSettingsWrap::SimulationSettingsWrap(const Napi::CallbackInfo& info) : ObjectWrap(info) {

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

    std::string jsonPath = info[0].As<Napi::String>();
    _internalInstance = std::make_shared<SimulationSettings>(jsonPath);
}

void SimulationSettingsWrap::Init(Napi::Env env, Napi::Object exports) {
    Napi::String name = Napi::String::New(env, "SimulationSettings");
    exports.Set(name, SimulationSettingsWrap::GetClass(env));
}

Napi::Function SimulationSettingsWrap::GetClass(Napi::Env env) {
    return DefineClass(env, "SimulationSettings", {});
}