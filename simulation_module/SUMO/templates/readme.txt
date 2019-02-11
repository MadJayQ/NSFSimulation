Provided here is a SUMO/TraCI project template created by Quentin Goss. There are a few usefull tools provided in this template:

SECITON 1: project - A barebones project directory named "project"
SECTION 2: mkprj.py - A python script for creating a project quickly
SECTION 3: Usefull Links

################################################################
################################################################

	SECTION 1: project

################################################################
################################################################

Contained within the directory 'project' is a sample SUMO/TraCI project. The breakdown of a SUMO/TraCI project is simple. There is a 'data' folder that contains the source data for the map and one or more modules. Let's look at our sample 'project':

.
./data/
./data/blank.net.xml
./data/blank.poly.xml
./data/blank.rou.xml
./data/blank.settings.xml
./data/blank.sumocfg
./ex0/
./ex0/__pycache__
./ex0/config.py
./ex0/core.py
./ex0/run.bat
./ex0/run.nogui.bat
./ex0/runner.py



.

The project directory



./data/

Source map data is stored here



./data/blank.net.xml

The SUMO map is saved as an xml file here. You can edit this using `netedit`. 

netedit blank.net.xml



./data/blank.poly.xml

If your map uses polygons, they're saved here



./data/blank.rou.xml

TraCI handles route creation but this is required if you want to view your map using `sumogui`.



./data/blank.settings.xml

This file contains settings for the visuals of SUMO. If the camera is off-center or you wish for any reason to use triangles instead of cars and grass then edit this file.



./data/blank.sumocfg

This file has pointers to the rest of the files in this directory. It is the file that SUMO uses to run the simulation. NOTE!! We're using TraCI so our ./ex0/run.bat will be running our simulation!! But if you'd like, you can view your map using `sumogui`.

sumogui -o ./data/blank.sumocfg



./ex0/

This is our example module named `ex0`



./ex0/config.py

Variables that might need to be edited go here. The variables in the first section are neccesary for running TraCI with SUMO. This is included in ./ex0/core.py and ./ex0/runner.py. If you make additional modules I reccomend importing this into those as well if they use variables that might need to be adjusted.



./ex0/core.py

This is where you write your code. 

def generate_elements()
	
	Before you can add vehicles, you need to create a vehicle object. You can use the same string from my other projects or make your own. DO NOT PUT TRACI COMMANDS HERE!!!!

def initialize(traci)	
	
	Anything you want to happen before the first simulation step goes here.

def timestep(traci,n_step)

	If something happens during the simulation, it goes here.

!!! NOTES !!!

If you want to make a TraCI call within a python function you MUST add `traci` as a parameter.



./ex0/run.bat

A windows batch script that runs your simulation with the GUI



run.nogui.bat

Runs the simulation without the GUI. Use this for checking for errors in your simulation (read: make sure the simulation runs all the way through w/o the GUI first!!)



./ex0/runner.py

This initializes TraCI and attaches it to SUMO. THERE IS NO REASON TO MODIFY THIS FILE!!! The only two files you should modify are  ./ex0/config.py and ./ex0/core.py.

################################################################
################################################################

	SECTION 2: mkprj.py

################################################################
################################################################

This script will create a basic SUMO/TraCI project and module wherever you want with one command. Use the --help flag at look at `mkprj.ex.bat` in the `example` directory for instructions.

-h --help

Display help



-d DIR, --DIR=DIR

The folder that you want your project to be in. This is an optional parameter. You can always put the project here and then copy/paste it wherever you want.



-n PROJECT_NAME, --name=PROJECT_NAME

Everything in ./data/ will have this as a prefix. Make sure you choose the name you want the first time, otherwise you'll have to change filenames in all of your configuration files and modules.



-m MODULE_NAME, --module_name=MODULE_NAME

The name of the folder where your module is placed. This is an optional parameter.This isn't as important as the project name and it can easily be changed later.



-p --polygon

Use this flag if you want to include polygons in your project. It automatically creates a .poly.xml file and a pointer in the .sumoconfig file.



-t SUMO_TOOLS, --sumo_tools=SUMO_TOOLS

In the ./ex0/config.py is a pointer to the SUMO tools directory. If your sumo is installed someplace other than the default "C:/Program Files (x86)/Eclipse/Sumo" then you'll have to point `mkprj.py` to your tools directory with

-t <Path to SUMO>/Sumo/tools


################################################################
################################################################

	SECTION 3: Usefull Links

################################################################
################################################################

http://www.sumo.dlr.de/daily/pydoc/traci._route.html#RouteDomain-add

http://sumo.dlr.de/wiki/TraCI/Add_Vehicle
