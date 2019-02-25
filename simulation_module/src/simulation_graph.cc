#include "simulation_map.h"
#include "simulation_settings.h"

#include "simulation_common.hpp"

#include <fstream>
#include <iostream>
#include <limits>
#include <random>

std::list<const SimulationNode *> GetShortestPath(const SimulationNode *node, const std::unordered_map<std::string, const SimulationNode *> &previous);
std::random_device rd;
std::mt19937 e2(rd());
std::uniform_int_distribution<> dist(300, 500);

SimulationGraph::SimulationGraph(const std::string &mapJsonFile)
{
    auto graphJson = ReadJsonFile(mapJsonFile);
    auto nodesJson = READ_JSON_RET(graphJson, nodes, nlohmann::json);
    auto edgesJson = READ_JSON_RET(graphJson, edges, nlohmann::json);
    nodes_ = NodeMap();
    for (auto itr = nodesJson.begin(); itr != nodesJson.end(); ++itr)
    {
        try
        {
            if (!HasNode(itr.key()))
            {
                CreateNode(itr.key());
            }
        }
        catch (std::invalid_argument e)
        {
            continue;
        }
    }
    for (auto itr = edgesJson.begin(); itr != edgesJson.end(); ++itr)
    {
        try
        {
            auto edge = (*itr).get<nlohmann::json>();
            std::string edgeName = itr.key();
            std::pair<SimulationNode *, SimulationNode *> edgeNodes = {nullptr, nullptr};
            std::string delimeter = "_to_";
            std::string token;
            size_t pos = 0;
            pos = edgeName.find(delimeter);
            token = edgeName.substr(0, pos);
            auto nodeName = edgeName.substr(0, pos);
            auto dstNode = GetNode(edgeName.substr(pos + delimeter.length(), edgeName.size()));
            if (dstNode == nullptr)
            {
                throw InvalidEdgeException(edgeName);
            }
            edgeNodes.first = GetNode(nodeName);
            edgeNodes.second = dstNode;
            EdgeConstructData params(
                edge["distance"].get<float>(),
                edge["speed"].get<float>(),
                0.001f);
            ConstructEdge(edgeName, edgeNodes, &params);
        }
        catch (std::invalid_argument e)
        {
            continue;
        }
    }
    std::cout << nodes_.size() << " nodes have been parsed." << std::endl;
}

bool SimulationGraph::HasNode(const std::string &key)
{
    return nodes_.find(key) != nodes_.end();
}

SimulationNode *SimulationGraph::GetNode(const std::string &key)
{
    if (!HasNode(key))
        return nullptr;

    return nodes_[key].get();
}

void SimulationGraph::CreateNode(const std::string &key)
{
    nodes_[key] = std::make_unique<SimulationNode>(key, this); //Create our new node
    nodes_[key]->SetBudget(dist(e2));
}

unsigned int SimulationGraph::IndexOf(const std::string &key)
{
    return 0u;
}

unsigned int SimulationGraph::IndexOf(const SimulationNode *node)
{
    return IndexOf(node->Key());
}

SimulationNode *SimulationGraph::ShortestPath(const SimulationNode *src, const SimulationNode *dst) const
{
    std::unordered_map<std::string, const SimulationNode *> previous;
    DijkstraComputePaths(src, previous); //Compute all pathes using Dijkstra's algorithm
    auto path = GetShortestPath(dst, previous);
    path.pop_front();
    return (path.size() > 0) ? const_cast<SimulationNode *>(path.front()) : nullptr;
}

std::vector<SimulationParticipant *> SimulationGraph::GetParticipants(std::initializer_list<SimulationParticipant *> ignoreList)
{
    std::vector<SimulationParticipant *> ret;
    for (auto &&node : nodes_)
    {
        auto participants = node.second->GetParticipants();
        for (auto participantItr = participants->begin();
             participantItr != participants->end();
             ++participantItr)
        {
            auto participant = const_cast<SimulationParticipant *>((*participantItr).second);
            if (ignoreList.size() == 0)
            {
                ret.push_back(participant);
            }
            else
            {

                if (std::find(ignoreList.begin(), ignoreList.end(), participant) == ignoreList.end())
                {
                    ret.push_back(participant);
                }
            }
        }
    }
    return ret;
}

std::list<const SimulationNode *> GetShortestPath(const SimulationNode *node, const std::unordered_map<std::string, const SimulationNode *> &previous)
{
    std::list<const SimulationNode *> path;
    for (; node != nullptr; node = previous.at(node->Key()))
    {
        path.push_front(node);
    }
    return path;
}

/*  
* Dijkstra's Path Finding Algorithm
* Plot all the SHORTEST pathes from the source node to all other nodes
* Store these results in the 'previous' map
*/

void SimulationGraph::DijkstraComputePaths(const SimulationNode *src,
                                           std::unordered_map<std::string, const SimulationNode *> &previous) const
{
    std::unordered_map<std::string, unsigned int> dists;
    for (auto nodeItr = nodes_.begin(); nodeItr != nodes_.end(); ++nodeItr)
    {
        dists[nodeItr->second->Key()] = std::numeric_limits<unsigned int>::max();
        previous[nodeItr->second->Key()] = nullptr;
    }
    dists[src->Key()] = 0u;
    std::vector<const SimulationNode *> vertices;

    vertices.push_back(src);

    while (!vertices.empty())
    {
        const SimulationNode *node = *vertices.begin();
        auto weight = node->Weight();
        vertices.erase(vertices.begin());

        auto adjacencyList = &node->EdgeList;
        for (auto adjItr = adjacencyList->begin(); adjItr != adjacencyList->end(); ++adjItr)
        {
            auto adjNode = (*adjItr);
            auto distance = weight + (*adjNode)->Weight();

            if (distance < dists[(*adjNode)->Key()])
            {
                dists[(*adjNode)->Key()] = distance;
                previous[(*adjNode)->Key()] = node;
                vertices.push_back(adjNode->Destination());
            }
        }
    }
}

/*
    ConstructEdge
    Allows the realtime addition of edges to our simulation
*/
void SimulationGraph::ConstructEdge(const std::string &name, std::pair<SimulationNode *, SimulationNode *> &pair)
{
    edges_[name] = std::make_unique<SimulationEdge>(
        pair.first,
        pair.second);
    pair.first->EdgeList.push_back(edges_[name].get());
}

/*
    ConstructEdge - Parameters
    Allows the realtime addition of edges to our simulation
    Pass parameter object to set the specific edge parameters
*/
void SimulationGraph::ConstructEdge(const std::string &name, std::pair<SimulationNode *, SimulationNode *> &pair, EdgeConstructData *params)
{
    edges_[name] = std::make_unique<SimulationEdge>(
        pair.first,
        pair.second,
        params->distance,
        params->avgSpeed,
        params->speedDev);
    pair.first->EdgeList.push_back(edges_[name].get());
}
