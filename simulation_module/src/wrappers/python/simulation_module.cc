#ifndef BOOST_PYTHON_STATIC_LIB
#define BOOST_PYTHON_STATIC_LIB
#endif 

#include <python.h>
#include <boost\python.hpp>
#include "simulation_module.h"
#include "simulation_map.h"
#include "simulation_settings.h"
#include "simulation_world.h"
#include "simulation_participant.h"
#include "simulation_data.h"

#include <json.hpp>
#include <memory>
#include <string>

#include <iostream>

#include <boost/python/class.hpp>
#include <boost/python/module.hpp>
#include <boost/python/def.hpp>

class SimulationModule;

class SimulationModuleWrap
{
public:
    SimulationModuleWrap();
	SimulationModuleWrap(const SimulationModuleWrap &) {}

    void Initialize(const std::string&);

	boost::python::object GetSettings();
private:
	std::unique_ptr<SimulationModule> module_;
};

SimulationModuleWrap::SimulationModuleWrap()
{
	module_ = std::make_unique<SimulationModule>();
}

boost::python::object SimulationModuleWrap::GetSettings()
{
	boost::python::object ret;
	return ret;
}

void SimulationModuleWrap::Initialize(const std::string& path)
{
	std::cout << "Initializing simulation..." << std::endl;
	try {
		module_->Initialize(path);
	} catch (std::exception e) {

	}
}


BOOST_PYTHON_MODULE(nsf)
{
	using namespace boost::python;
	auto simulationModule = class_<SimulationModuleWrap>("SimulationModule", init<>())
		.def("initialize", &SimulationModuleWrap::Initialize);
	
}