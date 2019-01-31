#include <python.h>

#ifndef BOOST_PYTHON_STATIC_LIB
#define BOOST_PYTHON_STATIC_LIB
#endif 

#include <boost/python/class.hpp>
#include <boost/python/module.hpp>
#include <boost/python/def.hpp>

#include "simulation_module.h"

class SimulationModule;

class SimulationModuleWrap
{
public:
    SimulationModuleWrap();

    void Initialize(const std::string&);
};


BOOST_PYTHON_MODULE(nsf)
{
	using namespace boost::python;
	class_<SimulationModuleWrap>("SimulationModule", init<float>()).def_readonly("value", &Bar::value);
}