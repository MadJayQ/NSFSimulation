#pragma once

#include <json.hpp>

#include <fstream>


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