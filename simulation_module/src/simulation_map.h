#pragma once

#include <vector>
#include <json.hpp>
#include <unordered_map>
#include <stack>

#include <random>

#include "simulation_math.hpp"

class SimulationParticipant;

using ParticipantMap = std::unordered_map<std::string, const SimulationParticipant*>;

class SimulationGraph;
class SimulationEdge;

class SimulationNode
{
public:
    explicit SimulationNode(std::string nodeID, const SimulationGraph* graph);
public:
    std::vector<SimulationEdge*> EdgeList;

    void SetBudget(unsigned int budget) { budget_ = budget; }
    unsigned int GetBudget() { return budget_; }

    void ParticipantLeave(SimulationParticipant* participant);
    void ParticipantEnter(SimulationParticipant* participant);

    bool HasParticipant(const std::string& name);

    SimulationNode* ShortestPath(const SimulationNode* dst);
    std::list<const SimulationNode*> ShortestPathAsList(const SimulationNode* dst);

    std::string Key() const { return key_; }

    unsigned int Weight() const { return weight_; }

    const SimulationGraph* GetGraph() { return graph_; }

    ParticipantMap* GetParticipants() const { return const_cast<ParticipantMap*>(&participants_); }

private: 
    std::string key_;
    unsigned int budget_; //The budget that has been dispersed to our node
    unsigned int weight_; //Weight for shortest path algortihm (NOTE): It should always be 1
    ParticipantMap participants_; //This is a list of all active participants in this node
    const SimulationGraph* graph_; 
};

class SimulationEdge
{
public:
    explicit SimulationEdge(SimulationNode* src, SimulationNode* dst) : src_(src), dst_(dst) 
    {
        distance_ = -1;
    }

    SimulationEdge(SimulationNode* src, SimulationNode* dst, float distance, ProbabilityDensityFunction pdf) 
        : src_(src), dst_(dst), distance_(distance)
    {
        pdf_ = pdf;
    }

    SimulationNode* operator -> () { return dst_; }

    SimulationNode* Destination() { return dst_; }
    SimulationNode* Source() { return src_; }

    float Distance() { return distance_; }
    double SpeedSample() { return pdf_.SampleValue(); }


private:
    friend class SimulationNode; //Allow our simulation node to know about these private members
    SimulationNode* src_, * dst_;
    float distance_;
    ProbabilityDensityFunction pdf_;
};

using NodeMap = std::unordered_map<std::string, std::unique_ptr<SimulationNode>>;
using RandomLUT = std::unordered_map<unsigned, NodeMap::const_iterator>;
using EdgeMap = std::unordered_map<std::string, std::unique_ptr<SimulationEdge>>;

struct EdgeConstructData
{
    EdgeConstructData(float distance_, ProbabilityDensityFunction pdf_) 
    {
        distance = distance_;
        pdf = pdf_;
    }
    float distance;
    ProbabilityDensityFunction pdf;
};

class SimulationGraph
{
public:
    explicit SimulationGraph(const std::string&);

    SimulationNode* GetNode(const std::string& key);
    SimulationNode* ShortestPath(const SimulationNode* src, const SimulationNode* dst) const;
    std::list<const SimulationNode*> ShortestPathAsList(const SimulationNode* src, const SimulationNode* dst) const;
    
    unsigned int IndexOf(const std::string& key);
    unsigned int IndexOf(const SimulationNode* node);
    
    //Does this graph currently have the node?
    bool HasNode(const std::string& key);
    static nlohmann::json ReadMapfile(const std::string& mapFile);

    SimulationNode* RandomNode(); 

    std::vector<SimulationParticipant*> GetParticipants(std::initializer_list<SimulationParticipant*> ignoreList);
    std::vector<SimulationParticipant*> GetAdjacentParticipants(SimulationNode* node, std::initializer_list<SimulationParticipant*> ignoreList);
    
    void ConstructEdge(const std::string& name, std::pair<SimulationNode*, SimulationNode*>& pair);
    void ConstructEdge(const std::string& name, std::pair<SimulationNode*, SimulationNode*>& pair, EdgeConstructData* edgeParams);

    int GetNodeCount() const { return nodes_.size(); }

private:
    void CreateNode(const std::string& itr);
    void DijkstraComputePaths(const SimulationNode* src, std::unordered_map<std::string, const SimulationNode*>& previous) const;
private:
    NodeMap nodes_;
    RandomLUT lut_;
    EdgeMap edges_;
};


