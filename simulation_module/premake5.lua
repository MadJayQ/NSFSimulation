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