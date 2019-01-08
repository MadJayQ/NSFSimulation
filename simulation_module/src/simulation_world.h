#pragma once

class SimulationSettings;

class SimulationWorld 
{
public:
    SimulationWorld(const SimulationSettings& settings);

public:
    int width;
    int height;

}