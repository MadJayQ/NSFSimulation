import os
import sys
import optparse
import config # ./config.py

__IS_DEBUG_MODE = False # global flag used when calling debug()

###############################
#      Import sumolib_and_traci and TracI
###############################
try:
  sys.path.append(config.s_sumo_tools_dir) # Path to SUMO python modules
  from sumolib import checkBinary  
  print("sumolib sucessfully imported.")
except ImportError:  
  sys.exit("Could not locate sumolib in " + config.s_sumo_tools_dir + ".")
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
  global __IS_DEBUG_MODE
  __IS_DEBUG_MODE = options.debug
  
  return options
# end get_options()


###############################
# @param s_msg = message to be printed to console.
# Check if options.debug=true, then print to console.
###############################
def debug(s_msg):
  global __IS_DEBUG_MODE
  if __IS_DEBUG_MODE:
    print(s_msg)
# end debug(s_msg)


###############################
# A quick pause
###############################
def pause():
  input("Press return to continue...")
# end def pause()


###############################
# Generates a routefile
###############################
def generate_routefile():
  debug("Starting to generate routefile...")
  
  with open(config.s_route_file,"w") as routes:
    print("<routes>", file=routes)
    s_elements = generate_elements()
    print(s_elements, file=routes)
    print("</routes>", file=routes)
    
  debug("Routefile created.")
# end generate_routefile


###############################
# Execute the TraCI control loop
###############################
def run():
  n_step = 0
  initialize()
  
  while (n_step < config.n_time_steps):
    traci.simulationStep()
    timestep(n_step)
    n_step += 1
  # end while
  
  traci.close()
# end run()

###############################
# Load in the neccesary libraries and launch SUMO + TraCI
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
    debug("config.s_sumocfg_file="+config.s_sumocfg_file)
    
    sumo_cmd = [s_sumo_binary, "-c", config.s_sumocfg_file]
    traci.start(sumo_cmd)
    
    run()
# End main

###################################################################
###################################################################
#                      START EDITING HERE
###################################################################

# Add imports here
import random
random.seed(config.n_seed)

###############################
# Global Variables
###############################
N_VEHICLES=0
LS_EDGES = []

###############################
# Add element(s) to routefiles
#
# @return string = The elements that will be added to the routefile.
###############################
def generate_elements(): 
  s_elements = "\t" + config.s_vtype + "\n"
  return s_elements
# End def generate_elements()


###############################
# Initilize anything that needs to happen at step 0 here.
###############################
def initialize():

  # Add a route that is 1 edge long so that vehicles have someplace
  # to spawn
  traci.route.add("start",["gneE0"])
  debug("Starting route sucessfully added.")
  
  # Populate drivable edges to LS_EDGES
  debug("Populting list of edges...")
  global LS_EDGES
  ls_edge_ids = traci.edge.getIDList()
  for s_edge_id in ls_edge_ids: # Look through the list of edges
    if "gneE" in s_edge_id: # Check if they're a road.
      debug(s_edge_id)
      LS_EDGES.append(s_edge_id) # Add the edge to LS_EDGES
  debug(LS_EDGES)
  
  return
# end def intialize


###############################
# Anything that happens within the TraCI control loop goes here.
# One pass of the loop == 1 timestep.
###############################
def timestep(n_step):
  create_vehicles(n_step)
  
  # Get list of active vehicle IDs
  ls_veh_ids = traci.vehicle.getIDList()
  for s_veh_id in ls_veh_ids:
    # If the vehicle is stopped, it is on the last edge of its route and 
    # needs to be assigned another route.
    if (traci.vehicle.isStopped(s_veh_id)):
      random_route(s_veh_id)
  # end for s_veh_id in ls_veh_ids:
  
  return
# end timestep


###############################
# Creates a vehicle
###############################
def create_vehicles(n_step):
  
  # Check if the maximum amount of vehicles are in the simulation
  if (config.n_vehicles_max <= len(traci.vehicle.getIDList())):
    return
  
  # Vehicle Creation
  if (n_step % config.n_vehicle_spawn_rate == 0):
    global N_VEHICLES
    s_vehicle_id = "veh" + str(N_VEHICLES) # vehX
    
    # All vehicles spawn into a 1 edge route. 
    traci.vehicle.add(s_vehicle_id, "start", depart=n_step+1, pos=-4, speed=-3, lane=-6, typeID="chevy_s10")
    N_VEHICLES += 1
    
    # Assign them a route.
    random_route(s_vehicle_id)
    
  # end if (n_step % N_VEHICLE_SPAWN_RATE == 0):
# end def create_vehicle
  
  
###############################
# Assigns a vehicle to a random route
# 
# @ param s_vehicle_id = vehicle id
###############################
def random_route(s_vehicle_id):
    # Assign the each vehicle to go to a differnt route.
    global LS_EDGES
    n_random_int = random.randint(0,len(LS_EDGES)-1)
    s_dest_edge = LS_EDGES[n_random_int]
    traci.vehicle.changeTarget(s_vehicle_id,s_dest_edge)
    
    # Set a stop when the vehice reaches it's destination.
    # Every simulation step, we will look for vehicles that are stopped
    # and reroute them.
    traci.vehicle.setStop(s_vehicle_id, s_dest_edge, pos=5.1, laneIndex=0, duration=-1, flags=0, startPos=1.0, until=-1)
    
    # Correlate a color to the route
    n_random_int = (n_random_int + 1)%(len(config.lsn_colors))-1
    traci.vehicle.setColor(s_vehicle_id,config.lsn_colors[n_random_int])
# end def random_route

###############################
# The main entry point of the script.
###############################
main()

