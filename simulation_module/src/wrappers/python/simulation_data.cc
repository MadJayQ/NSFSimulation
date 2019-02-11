#include <string>

class SimulationDataWrap
{
public:
    SimulationDataWrap() {}

    int GetHopCount(const std::string& name);
	void AquireWeakReference(std::weak_ptr<SimulationData> weakPtr) { _internalInstance = weakPtr;  }

    static boost::python::class_<SimulationDataWrap> InitPyWrapper();
private:
	std::weak_ptr<SimulationData> _internalInstance;
};

int SimulationDataWrap::GetHopCount(const std::string& name)
{
	return _internalInstance.lock()->GetHopCount(name);
}

using namespace boost::python;

class_<SimulationDataWrap> SimulationDataWrap::InitPyWrapper()
{
    return class_<SimulationDataWrap>("SimulationData", init<>())
        .def("getHopCount", &SimulationDataWrap::GetHopCount);
}