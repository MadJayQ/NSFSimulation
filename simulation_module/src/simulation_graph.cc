#include "simulation_map.h"
#include "simulation_settings.h"

#include "simulation_common.hpp"

#include <fstream>
#include <iostream>

SimulationGraph::SimulationGraph(const std::string& mapJsonFile) 
{
    auto graphJson = ReadJsonFile(mapJsonFile);
    auto nodesJson = READ_JSON_RET(graphJson, nodes, nlohmann::json);
    nodes_ = NodeMap();
    for(auto itr = nodesJson.begin(); itr != nodesJson.end(); ++itr) {
        try {
            if(!HasNode(itr.key())) {
                CreateNode(nodesJson, itr.key());
            }
        } catch (std::invalid_argument e) {
            continue;
        }
    }    
    std::cout << nodes_.size() << " nodes have been parsed." << std::endl; 
}


bool SimulationGraph::HasNode(const std::string& key) {
    return nodes_.find(key) != nodes_.end();
}

SimulationNode* SimulationGraph::GetNode(const std::string& key) {
    if(!HasNode(key)) return nullptr;

    return nodes_[key].get();
}

/*
*    CreateNode - Recursive function to populate directed graph adjacency lists
*    Parameters: 
*        1) nodeJson - JSON Object
*            This object contains the list of all of our nodes, and their adjacent nodes provided to us by our map JSON file
*        2) key - UTF-8 String
*           This string is the name of the node's key name that we wish to create
*
*/
void SimulationGraph::CreateNode(const nlohmann::json& nodesJson,
    const std::string& key) {
    nodes_[key] = std::make_unique<SimulationNode>(key); //Create our new node
    auto adjacencyArray = nodesJson[key]; //Read node adjacency key (this schema is STRICT)
    for(auto i = 0u; i < adjacencyArray.size(); i++) {
        auto adjKey = std::to_string(adjacencyArray[i].get<unsigned int>()); //HACK HACK(Jake): The key should just be stored as a string since it can be a non-integer
        if(!HasNode(adjKey)) { //Don't try to form an edge to a node that doesn't exist yet
            CreateNode(nodesJson, adjKey); //Recursively create our target node
        }
        nodes_[key]->AdjacencyList.push_back(nodes_[adjKey].get()); //Create our edge to our target node
    }
}