#include "simulation_settings.h"

#include <memory>
#include <fstream>
#include <iostream>

#include <assert.h>

using namespace nlohmann;

SimulationSettings::SimulationSettings()
{

}

void SimulationSettings::LoadSettingsFile(const std::string& settingsPath)
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