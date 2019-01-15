#pragma once

#include <napi.h>
#include <json.hpp>

#include <memory>

#include <unordered_map>

#include "simulation_common.hpp"

/*
    SimulationParameters Class
    Wrapper class for simulation paramaters as outlined in settings.json file
*/
class SimulationParameters
{
public:
    SimulationParameters(const nlohmann::json& parametersJson);
public:
    int num_initial_participants;
    int num_initial_nonparticipants;
};


/*
    SimulationMaps Class
    Wrapper class for standard library unordered map
    This class is responsible for parsing out map data from the settings.json file
*/
class SimulationMaps
{
public:
    SimulationMaps(const nlohmann::json& parametersJson);

public:
    std::unordered_map<std::string, std::string> MapFiles;
};

/*
    Internal class representation of simulation settings
*/
class SimulationSettings
{
public:
    SimulationSettings(const std::string& settingsPath);

public:
    int width, height;
    SimulationParameters* Parameters() const { return parameters_.get(); }
    SimulationMaps* Maps() const { return maps_.get(); }
private:
    std::unique_ptr<SimulationParameters> parameters_;
    std::unique_ptr<SimulationMaps> maps_;
};

/*
    Wrapper object to N-API for the internal SimulationSettings class
*/
class SimulationSettingsWrap : public Napi::ObjectWrap<SimulationSettingsWrap>
{
public:
    //Ctor
    SimulationSettingsWrap(const Napi::CallbackInfo& info);

    //Access our internal simulation settings instance
    std::weak_ptr<SimulationSettings> GetInternalInstance() const;

    //Responsible for initializing our class 
    static void Init(Napi::Env env, Napi::Object exports);
    //Responsible for detailing the outline for our class to be referenced by the JavaScript runtime
    static Napi::Function GetClass(Napi::Env);
private:

    std::shared_ptr<SimulationSettings> _internalInstance;
};