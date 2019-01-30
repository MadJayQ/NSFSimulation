#include "simulation_module.h"

#include "simulation_settings.cc"
#include "simulation_data.cc"

#include "../simulation_module.h" //Our actual simulation module object
#include "../simulation_participant.h"

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

    Napi::String settingsPath = info[0].As<Napi::String>();

    UNPACK_ARGUMENT(SimulationSettingsWrap, settingsObj, info, 0);
    SettingsRef = Napi::Reference<Napi::Object>::New(settingsObj->Value(), 1);
    module_->Settings = std::make_shared<SimulationSettings>();
    module_->Data = 
    module_->Settings->LoadSettingsFile(settingsPath.Utf8Value());

    settingsObj->AquireWeakReference(
        std::weak_ptr<SimulationSettings>(module_->Settings)
    );


    module_->World = std::make_unique<SimulationWorld>(settingsObj->GetInternalInstance());
    auto world = module_->World.get();
    world->SetCurrentMap("grid");

    try {
        world->InitializeParticipants(
            std::make_unique<SimulationParticipantSettings>(
                "C:\\Users\\jakei_000\\Desktop\\NSFSimulation\\participants.json"
            ).get()
        );

        auto dataWwap = Napi::ObjectWrap<SimulationDataWrap>::Unwrap(
            Napi::Persistent(SimulationDataWrap::GetClass(env)).New({})
        );
        DataRef 
    } catch (std::exception e) {
        Napi::TypeError::New(env, e.what()).ThrowAsJavaScriptException();
    }



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
