#pragma once

#include <json.hpp>

#include <fstream>
#include <exception>

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