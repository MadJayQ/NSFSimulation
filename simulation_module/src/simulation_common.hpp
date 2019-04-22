#pragma once

#include <json.hpp>

#include <fstream>
#include <exception>
#include <random>
#include <chrono>
#include <iostream>
#include <sstream>

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



/* Convert double to string with specified number of places after the decimal
   and left padding. */
static std::string prd(const double x, const int decDigits, const int width) {
    std::stringstream ss;
    ss << std::fixed << std::right;
    ss.fill(' ');        // fill space around displayed #
    ss.width(width);     // set  width around displayed #
    ss.precision(decDigits); // set # places after decimal
    ss << x;
    return ss.str();
}

/*! Center-aligns string within a field of width w. Pads with blank spaces
    to enforce alignment. */
static std::string center(const std::string s, const int w) {
    std::stringstream ss, spaces;
    int padding = w - s.size();                 // count excess room to pad
    for(int i=0; i<padding/2; ++i)
        spaces << " ";
    ss << spaces.str() << s << spaces.str();    // format with padding
    if(padding>0 && padding%2!=0)               // if odd #, add 1 space
        ss << " ";
    return ss.str();
}


static std::random_device s_randomDevice;
static std::mt19937 s_randomNoise;
static std::normal_distribution<float> s_dist(0.5, 0.25);