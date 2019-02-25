#pragma once

#include <json.hpp>

#include <fstream>
#include <exception>
#include <random>
#include <chrono>

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

class InvalidEdgeException : std::exception
{
public:
    InvalidEdgeException(const std::string& edgeName)
    {
        edge_name_ = edgeName;
    }

    const char* what() const throw()
    {
        std::string errorStr = "Invalid edge format: " + edge_name_;
        return errorStr.c_str();
    }
private:
    std::string edge_name_; 
};


static unsigned long long TimestampMS() {
    return std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now().time_since_epoch()).count();
}


static std::random_device s_randomDevice;
static std::mt19937 s_randomNoise;
static std::normal_distribution<float> s_dist(0.5, 0.25);