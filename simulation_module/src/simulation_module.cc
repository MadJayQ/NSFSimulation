#include "simulation_module.h"
#include "command_parser.h"
#include "simulation_map.h"
#include "simulation_settings.h"
#include "simulation_world.h"
#include "simulation_participant.h"

#include <json.hpp>

using json = nlohmann::json;

using namespace Napi;

SimulationModule::SimulationModule(const Napi::CallbackInfo& info) : ObjectWrap(info) {
    Napi::Env env = info.Env();

    if (info.Length() < 1) {
        Napi::TypeError::New(env, "Wrong number of arguments")
          .ThrowAsJavaScriptException();
        return;
    }

    if (!info[0].IsString()) {
        Napi::TypeError::New(env, "You need to name yourself")
          .ThrowAsJavaScriptException();
        return;
    }

    Commands = std::make_unique<CommandParser>();
    Commands->ExecuteCommand();

    json j = "{ \"happy\": true, \"pi\": 3.141 }"_json;

    this->_greeterName = info[0].As<Napi::String>().Utf8Value();
}

Napi::Value SimulationModule::Greet(const Napi::CallbackInfo& info) {
    Napi::Env env = info.Env();

    if (info.Length() < 1) {
        Napi::TypeError::New(env, "Wrong number of arguments")
          .ThrowAsJavaScriptException();
        return env.Null();
    }

    if (!info[0].IsString()) {
        Napi::TypeError::New(env, "You need to introduce yourself to greet")
          .ThrowAsJavaScriptException();
        return env.Null();
    }

    
    Napi::String name = info[0].As<Napi::String>();

    printf("Hello %s\n", name.Utf8Value().c_str());
    printf("I am %s\n", this->_greeterName.c_str());

    return Napi::String::New(env, this->_greeterName);
}

Napi::Value SimulationModule::GetSettings(const Napi::CallbackInfo& info) {
    Napi::Env env = info.Env();

    auto settings = SettingsRef.Value();

    return SettingsRef.Value();
}

//This function is responsible for receiving commands and then handing them to the command parser
void SimulationModule::OnCommand(const Napi::CallbackInfo& info) {
    Commands->ExecuteCommand(); //Execute our command
} 

void SimulationModule::Initialize(const Napi::CallbackInfo& info) {
    Napi::Env env = info.Env();

    if (info.Length() < 1) {
        Napi::TypeError::New(env, "Must supply settings module")
            .ThrowAsJavaScriptException();
    }

    if(!info[0].IsObject()) {
        Napi::TypeError::New(env, "Invalid settings module")
            .ThrowAsJavaScriptException();
    }

    UNPACK_ARGUMENT(SimulationSettingsWrap, settingsObj, info, 0);
    SettingsRef = Napi::Reference<Napi::Object>::New(settingsObj->Value(), 1);
    World = std::make_unique<SimulationWorld>(settingsObj->GetInternalInstance());
    World->SetCurrentMap("grid");
    //Hackius Maximus(Jake): This will literally create a unique pointer that will immediately go out of scope afterwards deleting the reference :) 
    World->InitializeParticipants(
        std::make_unique<SimulationParticipantSettings>(
            "F:\\Programming\\Work\\NSFSimulation\\participants.json"
            ).get()
    );
}

Napi::Function SimulationModule::GetClass(Napi::Env env) {
    return DefineClass(env, "SimulationModule", {
        SimulationModule::InstanceMethod("greet", &SimulationModule::Greet),
        SimulationModule::InstanceMethod("onCommand", &SimulationModule::OnCommand),
        SimulationModule::InstanceMethod("initialize", &SimulationModule::Initialize),
        SimulationModule::InstanceMethod("getSettings", &SimulationModule::GetSettings),
    });
}

Napi::Object Init(Napi::Env env, Napi::Object exports) {
    Napi::String name = Napi::String::New(env, "SimulationModule");
    exports.Set(name, SimulationModule::GetClass(env));

    SimulationSettingsWrap::Init(env, exports);

    return exports;
}

NODE_API_MODULE(addon, Init)
