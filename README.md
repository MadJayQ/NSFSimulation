# Incentive Mechanisms for Mobile Crowdsourcing, Reaching Spatial and Temporal Coverage Under Budget Constraints

**About**

This is a simulation software for the [NSF Project](https://nsf.gov/awardsearch/showAward?AWD_ID=1739409&HistoricalAwards=false) on Mobile Crowdsourcing by Luis. G Jaimes at Florida Polytechnic University

A basic Simulation setup needs these files:

- `settings.json` - Points to the simulation's parameters, and available maps
- `participants.json` - Lists all of the participants that will exist in the smimulation, where they originate from and where they traverse to.
- `<maps>.json` - Any map needs to be detailed in a json format listing all of the nodes, and edges

## How to compile
**Python**
Project files for the python binding are generated by [Premake](https://premake.github.io/) and are defined in */simulation_module/premake5.lua*

```
workspace "NSF Simulation"
    configurations { "Debug x86", "Release x86", "Debug x64", "Release x64" }
    location "build\\SUMO"
    filter "configurations:*64"
        architecture "x64"
    configuration "vs*"
        defines { "_CRT_SECURE_NO_WARNINGS" }
    filter "configurations:Debug x64"
        targetdir "bin/x64/Debug"
        defines { "DEBUG" }
        symbols "On"
    filter "configurations:*86"
        architecture "x86"
    filter "configurations:Debug x86"
        targetdir "bin/x86/Debug"
        defines { "DEBUG" }
        symbols "On"
project "nsf"
    kind "SharedLib"
    language "C++"
    targetextension ".pyd"
    libdirs {
        "F:\\Programming\\Libraries\\boost_1_69_0\\stage\\lib",
        "F:\\Programming\\Languages\\Python\\Python34\\libs"
    }
    includedirs {
        "F:\\Programming\\Libraries\\boost_1_69_0",
        "F:\\Programming\\Work\\NSFSimulation\\simulation_module\\lib\\json\\single_include\\nlohmann",
        "F:\\Programming\\Languages\\Python\\Python34\\include"
    }
    files { 'src/simulation_module.cc', 'src/simulation_settings.cc', 'src/simulation_world.cc', 'src/simulation_node.cc', 'src/simulation_graph.cc', 'src/simulation_participant.cc', 'src/simulation_data.cc' }
    configuration "vs*"
        characterset "MBCS"
```

The includedirs and libdirs for boost, and python need to be configured to your particular project setup

**NodeJS**

With NodeJS compile the NodeJS binary with [node-gyp](https://github.com/nodejs/node-gyp)
Instead of premake5.lua for NodeJS the binding is specified in binding.gyp

## To Use

To clone and run this repository you'll need [Git](https://git-scm.com) and either [Node.js](https://nodejs.org/en/download/) (which comes with [npm](http://npmjs.com)) installed on your computer, or [Python](https://www.python.org/)

```bash
# Clone this repository
git clone https://github.com/MadJayQ/NSFSimulation.git
# Go into the repository
cd NSFSimulation
# Install dependencies
npm install
# Run the test case if you're using NodeJS
node /simulation_module/test_binding.js 
#if you're using python to launch the simulation
python3 /simulation_module/test_binding.py
```

## License

[CC0 1.0 (Public Domain)](LICENSE.md)
