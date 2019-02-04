from nsf import *
from os.path import abspath;
settingsJSON = "./Settings.json";
settingsJSONFilepath = abspath(settingsJSON);

module = SimulationModule();
module.initialize(settingsJSONFilepath);