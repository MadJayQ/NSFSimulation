#pragma once

#include <json.hpp>

#include <fstream>
#include <exception>
#include <random>

#define READ_JSON(dst, json, key, type) dst = json[#key].get<type>();
#define READ_JSON_RET(json, key, type) json[#key].get<type>()

static nlohmann::json ReadJsonFile(const std::string& filePath) {
    std::ifstream jsonFile(filePath);
    nlohmann::json ret;
    try {
        assert(jsonFile.good());
        jsonFile >> ret;
    } catch(...) {
        ret = "{}"_json;
    }
    jsonFile.close();
    return ret;
}

struct NoValidMapException : std::exception
{
    const char* what() const throw()
    {
        return "No valid map was supplied";
    }
};


static std::random_device s_randomDevice;
static std::mt19937 s_randomNoise;
static std::normal_distribution<float> s_dist(0.5, 0.25);