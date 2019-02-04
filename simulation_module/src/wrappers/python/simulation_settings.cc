#include <boost/python/class.hpp>
#include <boost/python/module.hpp>
#include <boost/python/def.hpp>


class SimulationDataWrap
{
public:
    SimulationDataWrap() {}
    SimulationDataWrap(SimulationDataWrap& const) {}

    int GetHopCount(const std::string&);

    static 
}