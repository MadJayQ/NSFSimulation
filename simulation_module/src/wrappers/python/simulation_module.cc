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

#include "simulation_data.cc"

class SimulationModule;

class SimulationModuleWrap
{
public:
    SimulationModuleWrap();
	SimulationModuleWrap(const SimulationModuleWrap &) {}

    void Initialize(const std::string&);

	boost::python::object GetSettings();
	SimulationDataWrap* GetData();

private:
	std::unique_ptr<SimulationModule> module_;
	SimulationDataWrap _data;
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

SimulationDataWrap* SimulationModuleWrap::GetData()
{
	return &_data;
}

void SimulationModuleWrap::Initialize(const std::string& path)
{
	std::cout << "Initializing simulation..." << std::endl;
	try {
		module_->Initialize(path);
		_data = SimulationDataWrap();
		_data.AquireWeakReference(
			std::weak_ptr<SimulationData>(module_->Data)
		);
		module_->World->RunSimulation(module_->Data.get());
	} catch (std::exception e) {

	}
}


BOOST_PYTHON_MODULE(nsf)
{
	using namespace boost::python;
	auto simulationDataWrap = SimulationDataWrap::InitPyWrapper();
	auto simulationModule = class_<SimulationModuleWrap>("SimulationModule", init<>())
		.def("initialize", &SimulationModuleWrap::Initialize)
		.def("settings", &SimulationModuleWrap::GetSettings)
		.def("data", &SimulationModuleWrap::GetData, return_internal_reference<>());
}