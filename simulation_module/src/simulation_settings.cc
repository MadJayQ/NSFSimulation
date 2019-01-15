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
    _internalInstance = std::make_shared<SimulationSettings>(jsonPath);
}

Napi::Function SimulationSettingsWrap::GetClass(Napi::Env env) {
    return DefineClass(env, "SimulationSettings", {});
}

std::weak_ptr<SimulationSettings> SimulationSettingsWrap::GetInternalInstance() const
{
    return std::weak_ptr<SimulationSettings>(_internalInstance);
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
        assert(jsonFile.good()); //Check sanity of input json file
        auto parametersJson = READ_JSON_RET(settingsJson, parameters, nlohmann::json); //Rip parameters out
        auto mapsJson = READ_JSON_RET(settingsJson, maps, nlohmann::json);
        parameters_ = std::make_unique<SimulationParameters>(parametersJson);
        maps_ = std::make_unique<SimulationMaps>(mapsJson);
        READ_JSON(width, settingsJson, width, int);
        READ_JSON(height, settingsJson, height, int);
        std::cout << "Running simulation\nVersion:" << READ_JSON_RET(settingsJson, version, std::string) << "\nWidth: " << width << "\nHeight: " << height << std::endl;
    } catch (detail::parse_error error) {
        auto errorMsg = error.what();
        std::cout << errorMsg << std::endl;
    }
    jsonFile.close();
}

SimulationParameters::SimulationParameters(const nlohmann::json& parametersJson)
{
    READ_JSON(num_initial_participants, 
        parametersJson, numInitialParticipants, int);
    READ_JSON(num_initial_nonparticipants,
        parametersJson, numInitialNonParticipants, int);
}

SimulationMaps::SimulationMaps(const nlohmann::json& mapsJson)
{
    for(auto itr = mapsJson.begin(); itr != mapsJson.end(); ++itr) {
        MapFiles.emplace(itr.key(), *itr);
    }
}