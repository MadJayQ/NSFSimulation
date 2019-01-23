#pragma once

#include <vector>
#include <json.hpp>
#include <unordered_map>
#include <stack>

class SimulationParticipant;

using ParticipantMap = std::unordered_map<std::string, const SimulationParticipant*>;

class SimulationGraph;

class SimulationNode
{
public:
    explicit SimulationNode(std::string nodeID, const SimulationGraph* graph);
public:
    std::vector<SimulationNode*> AdjacencyList;   

    void SetBudget(unsigned int budget) { budget_ = budget; }
    unsigned int GetBudget() { return budget_; }

    void ParticipantLeave(SimulationParticipant* participant);
    void ParticipantEnter(SimulationParticipant* participant);

    bool HasParticipant(const std::string& name);

    SimulationNode* ShortestPath(const SimulationNode* dst);

    std::string Key() const { return key_; }

    unsigned int Weight() const { return weight_; }

private: 
    std::string key_;
    unsigned int budget_; //The budget that has been dispersed to our node
    unsigned int weight_; //Weight for shortest path algortihm (NOTE): It should always be 1
    ParticipantMap participants_; //This is a list of all active participants in this node
    const SimulationGraph* graph_; 
};

using NodeMap = std::unordered_map<std::string, std::unique_ptr<SimulationNode>>;

class SimulationGraph
{
public:
    explicit SimulationGraph(const std::string&);

    SimulationNode* GetNode(const std::string& key);
    SimulationNode* ShortestPath(const SimulationNode* src, const SimulationNode* dst) const;
    
    unsigned int IndexOf(const std::string& key);
    unsigned int IndexOf(const SimulationNode* node);
    
    //Does this graph currently have the node?
    bool HasNode(const std::string& key);
    static nlohmann::json ReadMapfile(const std::string& mapFile);
private:
    void CreateNode(const nlohmann::json& nodesJson, const std::string& itr);
    void DijkstraComputePaths(const SimulationNode* src, std::unordered_map<std::string, const SimulationNode*>& previous) const;
private:
    NodeMap nodes_;
};


