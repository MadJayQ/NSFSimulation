#include "simulation_settings.h"

#include <memory>
#include <fstream>
#include <iostream>

#include <assert.h>

using namespace nlohmann;

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
    _internalInstance = std::make_unique<SimulationSettings>(jsonPath);
}

Napi::Function SimulationSettingsWrap::GetClass(Napi::Env env) {
    return DefineClass(env, "SimulationSettings", {});
}

void SimulationSettingsWrap::Init(Napi::Env env, Napi::Object exports) {
    Napi::String name = Napi::String::New(env, "SimulationSettings");
    exports.Set(name, SimulationSettingsWrap::GetClass(env));
}

SimulationSettings::SimulationSettings(const std::string& settingsPath)
{
    std::ifstream jsonFile(settingsPath);
    try{
        json settingsJson;
        jsonFile >> settingsJson;
        assert(jsonFile.good());
        width = settingsJson["width"].get<int>();
        height = settingsJson["height"].get<int>();
        std::cout << "Running simulation\nVersion:" << settingsJson["version"].get<std::string>() << "\nWidth: " << width << "\nHeight: " << height << std::endl;
    } catch (detail::parse_error error) {
        auto errorMsg = error.what();
        std::cout << errorMsg << std::endl;
    }
}