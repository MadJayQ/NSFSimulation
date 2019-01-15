#pragma once

#include <vector>
#include <json.hpp>
#include <unordered_map>


class SimulationNode
{
public:
    explicit SimulationNode(std::string nodeID);
public:
    std::vector<SimulationNode*> AdjacencyList;   
private: 
    std::string key_;
};

using NodeMap = std::unordered_map<std::string, std::unique_ptr<SimulationNode>>;

class SimulationGraph
{
public:
    explicit SimulationGraph(const std::string&);

    SimulationNode* GetNode(const std::string& key);
    
    //Does this graph currently have the node?
    bool HasNode(const std::string& key);
    static nlohmann::json ReadMapfile(const std::string& mapFile);
private:
    void CreateNode(const nlohmann::json& nodesJson, const std::string& itr);
private:
    NodeMap nodes_;
};


