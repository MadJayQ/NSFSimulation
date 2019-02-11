##############################
# @file   ex2.py
# @author Quentin Goss
# @date   7/3/18
#
# the goal of this script is to assign all vehicles a route with the
# TraCI API while the simulation is running. Unlike ex1.py.
#
# Goals:
# [ ] Run without error.
# [ ] Create a route file with NO VEHICLES.
# [ ] Create a vehicle with the TraCI API.
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
S_SUMO_TOOLS_DIR = "/home/veins/src/sumo-0.30.0/tools"
S_ROUTE_FILE = S_ABSOLUTE_PATH + "/data/3choices.rou.xml"
S_SUMOCFG_FILE = S_ABSOLUTE_PATH + "/data/3choices.sumocfg"
N_SEED = 777333
N_TIME_STEPS=3000
N_VEHICLE_SPAWN_RATE=10 # How many time steps between new vehicles spawning?
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
  global N_TIME_STEPS
  global S_ROUTE_FILE
  global S_VTYPE
  global S_ROUTE_TOP
  global S_ROUTE_MIDDLE
  global S_ROUTE_BOTTOM
  
  with open(S_ROUTE_FILE,"w") as routes:
    print("<routes>", file=routes)
    
    # Vehicle Types
    print("\t" + S_VTYPE + "\n", file=routes)
    
    # Routes
    print("\t" + S_ROUTE_TOP + "\n\t" + S_ROUTE_MIDDLE + "\n\t" + S_ROUTE_BOTTOM + "\n", file=routes)
        
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
  global N_VEHICLE_SPAWN_RATE # 10
  global N_SEED #777333
  global N_TIME_STEPS # 3000
  n_vehicles = 0
  s_vehicle_id = ""
  random.seed(N_SEED)
  
  n_step = 0
  
  while (n_step < N_TIME_STEPS):
    traci.simulationStep()
    
    # Add some vehicles
    if (n_step % N_VEHICLE_SPAWN_RATE == 0): # Every 10 timesteps make a new vehicle
      n_random_int = random.randint(1,3) # Random between 1-3
      s_vehicle_id = "veh"+str(n_vehicles) # ehicle ID
      
      if (n_random_int == 1): # Top
        traci.vehicle.add(s_vehicle_id, "top", depart=n_step+1, pos=-4, speed=-3, lane=-6, typeID="chevy_s10")
        traci.vehicle.setColor(s_vehicle_id,(255,0,0,0))
        
      elif(n_random_int == 2): # Middle
        traci.vehicle.add(s_vehicle_id, "middle", depart=n_step+1, pos=-4, speed=-3, lane=-6, typeID="chevy_s10")
        traci.vehicle.setColor(s_vehicle_id,(0,255,0,0))
        
      else: # Bottom
        traci.vehicle.add(s_vehicle_id, "bottom", depart=n_step+1, pos=-4, speed=-3, lane=-6, typeID="chevy_s10")
        traci.vehicle.setColor(s_vehicle_id,(0,0,255,0))
        
      n_vehicles += 1
    # end if (n_step % N_VEHICLE_SPAWN_RATE == 0):
    
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
    global S_SUMOCFG_FILE
    debug("S_SUMOCFG_FILE="+S_SUMOCFG_FILE)
    
    sumo_cmd = [s_sumo_binary, "-c", S_SUMOCFG_FILE]
    traci.start(sumo_cmd)
    
    run()
# End main


###############################
# The main entry point of the script.
###############################
main()
