##############################
# @file   ex1.py
# @author Quentin Goss
# @date   7/3/18
#
# This is the first attempt at using TraCI and python alongside SUMO.
# The goals of this script:
# [x] Run without error.
# [x] Create a route file.
# [x] Launch SUMO as a subprocess through TraCI.
# [x] Implement a very basic TraCI Control Loop.
#
##############################
import os
import sys
import optparse
import random

###############################
#      Global Variables
###############################
S_ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
S_SUMO_TOOLS_DIR = "F:\\Programs\\sumo-1.1.0\\tools"
S_ROUTE_FILE = S_ABSOLUTE_PATH + "/data/3choices.rou.xml"
N_SEED = 777333
N_TIME_STEPS=3000
N_VEHICLE_SPAWN_RATE=10 # How many time steps between vehicle spawn?
IS_DEBUG = False
S_VTYPE = """<vType id="chevy_s10" accel="0.6" decel="1.3" sigma="0.4" length="5" minGap="2.5" maxSpeed="10" guiShape="passenger"/>"""
S_ROUTE_TOP = """<route id="top" edges="gneE0 gneE5 gneE6 gneE4" />"""
S_ROUTE_MIDDLE = """<route id="middle" edges="gneE0 gneE2 gneE4" />"""
S_ROUTE_BOTTOM = """<route id="bottom" edges="gneE0 gneE7 gneE8 gneE4"/>"""


###############################
#      Import sumolib
###############################
try:
  sys.path.append(S_SUMO_TOOLS_DIR) # Path to SUMO python modules
  from sumolib import checkBinary  
  print("sumolib sucessfully imported.")
except ImportError:  
  sys.exit("Could not locate sumolib in " + S_SUMO_TOOLS_DIR + ".")
import traci


###############################
# Uses optparse to add a --nogui option to run without using the gui.
###############################
def get_options():
  opt_parser = optparse.OptionParser()
  opt_parser.add_option("--nogui",action="store_true",default=False, help="run the commandline version of sumo")
  opt_parser.add_option("--debug",action="store_true",default=False, help="Adds additional print statements for debugging.")
  options, args = opt_parser.parse_args()
  
  # Set our debug global so we only check once
  global IS_DEBUG
  IS_DEBUG = options.debug
  
  return options
# end get_options()


###############################
# @param s_msg = message to be printed to console.
# Check if options.debug=true, then print to console.
###############################
def debug(s_msg):
  global IS_DEBUG
  if IS_DEBUG:
    print(s_msg)
# end debug(s_msg)


###############################
# Generates a routefile
###############################
def generate_routefile():
  debug("Starting to generate routefile...")
  global N_SEED
  global N_TIME_STEPS
  global N_VEHICLE_SPAWN_RATE
  global S_ROUTE_FILE
  global S_VTYPE
  global S_ROUTE_TOP
  global S_ROUTE_MIDDLE
  global S_ROUTE_BOTTOM
  random.seed(N_SEED)
  
  with open(S_ROUTE_FILE,"w") as routes:
    print("<routes>", file=routes)
    
    # Vehicle Types
    print("\t" + S_VTYPE + "\n", file=routes)
    
    # Routes
    print("\t" + S_ROUTE_TOP + "\n\t" + S_ROUTE_MIDDLE + "\n\t" + S_ROUTE_BOTTOM + "\n", file=routes)
    
    # Vehicles
    n_vehicle_count = 0
    n_random_int = 0
    # Vehicles will spawn at an interval until the time limit is reached
    for i in range(0,N_TIME_STEPS,N_VEHICLE_SPAWN_RATE):
      n_random_int = random.randint(1,3)
      
      # Top
      if (n_random_int == 1):
        print("""\t<vehicle id="top_%i" type="chevy_s10" route="top" depart="%i" color="1,0,0"/>""" % (n_vehicle_count, i), file=routes)
        n_vehicle_count += 1
        
      # Middle
      elif (n_random_int == 2):
        print("""\t<vehicle id="middle_%i" type="chevy_s10" route="middle" depart="%i" color="0,1,0"/>""" % (n_vehicle_count, i), file=routes)
        n_vehicle_count += 1
        
      # Bottom
      else:
        print("""\t<vehicle id="bottom_%i" type="chevy_s10" route="bottom" depart="%i" color="0,0,1"/>""" % (n_vehicle_count,i), file=routes)
        n_vehicle_count += 1
        
    # end for i in range(N_TIME_STEPS)
    
    print("</routes>", file=routes)
  debug("Routefile created.")
# end generate_routefile


###############################
# Execute the TraCI control loop
# ??? Not quite sure what this does yet but it is required to run
#  without error.
###############################
def run():
  n_step = 0
  
  while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    
    # TraCI stuff happens here
    
    n_step += 1
  # end while
  
  traci.close()
  
# end run()


###############################
# The 'if__name__ == "__main__":' makes sure that this code only runs
# when this module is ran but not when it is called as another module
# in a function. 
###############################
def main():
  if __name__ == "__main__":
    debug("The main script is running.")
    options = get_options()
    debug("options.nogui=" + str(options.nogui))
    
    # This script has been called from the command line.
    # It will start sumo as a server, then connect and run.
    if options.nogui:
      s_sumo_binary = checkBinary('sumo')
    else:
      s_sumo_binary = checkBinary('sumo-gui')
    debug("s_sumo_binary=" + s_sumo_binary)
    
    # We need to generate a routefile for this simulation
    generate_routefile()
    
    # Have TraCI start sumo as a subprocess, then the python script
    # can connect and run
    global S_ABSOLUTE_PATH
    s_sumocfg_path = S_ABSOLUTE_PATH + "/data/3choices.sumocfg"
    debug("s_sumocfg_path="+s_sumocfg_path)
    
    sumo_cmd = [s_sumo_binary, "-c", s_sumocfg_path]
    traci.start(sumo_cmd)
    
    run()
# End main


###############################
# The main entry point of the script.
###############################
main()
