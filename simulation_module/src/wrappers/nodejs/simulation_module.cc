#include <napi.h>
#include <memory>


#include "simulation_module.h"

#include "simulation_settings.cc"
#include "simulation_data.cc"

#include "simulation_participant.h"


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


SimulationModuleWrap::SimulationModuleWrap(const Napi::CallbackInfo& info) : ObjectWrap(info)
{
    module_ = std::make_unique<SimulationModule>();
}

void SimulationModuleWrap::Initialize(const Napi::CallbackInfo& info) {
    Napi::Env env = info.Env();

    if(info.Length() < 1) {
        Napi::TypeError::New(env, "Must supply settings module!").ThrowAsJavaScriptException();
    }

    if(!info[0].IsString()) {
        Napi::TypeError::New(env, "Invalid settings path").ThrowAsJavaScriptException();
    }

    try {
        Napi::String settingsPath = info[0].As<Napi::String>();
        module_->Initialize(settingsPath.Utf8Value());
        auto settingsWrap = Napi::ObjectWrap<SimulationSettingsWrap>::Unwrap(
            Napi::Persistent(SimulationSettingsWrap::GetClass(env)).New({})
        );
        settingsWrap->AquireWeakReference(
            std::weak_ptr<SimulationSettings>(module_->Settings)
        );
        SettingsRef = Napi::Reference<Napi::Object>::New(settingsWrap->Value(), 1);

        auto dataWrap = Napi::ObjectWrap<SimulationDataWrap>::Unwrap(
            Napi::Persistent(SimulationDataWrap::GetClass(env)).New({})
        );
        dataWrap->AquireWeakReference(
            std::weak_ptr<SimulationData>(module_->Data)
        );
        DataRef = Napi::Reference<Napi::Object>::New(dataWrap->Value(), 1);
    } catch (std::exception e) {
        Napi::TypeError::New(env, e.what()).ThrowAsJavaScriptException();
    }
}

Napi::Value SimulationModuleWrap::GetSettings(const Napi::CallbackInfo& info)
{
    return info.Env().Null();
}
Napi::Value SimulationModuleWrap::GetData(const Napi::CallbackInfo& info)
{
    return info.Env().Null();
}


/*
*   GetClass is a static method for each JavaScript - Exposed object
*   It is responsible for outlining the class method callbacks for the module exports section
*/

Napi::Function SimulationModuleWrap::GetClass(Napi::Env env) {
    return DefineClass(env, "SimulationModule", {
        SimulationModuleWrap::InstanceMethod("initialize", &SimulationModuleWrap::Initialize),
        SimulationModuleWrap::InstanceMethod("getSettings", &SimulationModuleWrap::GetSettings),
    });
}


Napi::Object Init(Napi::Env env, Napi::Object exports) {
    Napi::String name = Napi::String::New(env, "SimulationModule");
    exports.Set(name, SimulationModuleWrap::GetClass(env));

    SimulationSettingsWrap::Init(env, exports);
    SimulationDataWrap::Init(env, exports);

    return exports;
}

NODE_API_MODULE(addon, Init)
