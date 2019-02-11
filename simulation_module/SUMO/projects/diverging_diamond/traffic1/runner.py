import os
import sys
import optparse
import config # ./config.py
import time

__IS_DEBUG_MODE = False # global flag used when calling debug()
__F_START_TIME = time.time()

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
    global __F_START_TIME
    print("\n----- runtime takes %s seconds -----" % (time.time() - __F_START_TIME))
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
N_VEHICLES = 0

###############################
# Add element(s) to routefiles
#
# @return string = The elements that will be added to the #                             routefile.
###############################
def generate_elements():
  s_elements = "\t" + config.s_vtype + "\n"
  return s_elements
# End def generate_elements()


###############################
# Initilize anything that needs to happen at step 0 here.
###############################
def initialize():
  return
# end def intialize


###############################
# Anything that happens within the TraCI control loop goes here.
# One pass of the loop == 1 timestep.
###############################
def timestep(n_step):  
  create_vehicles(n_step)
  create_vehicles(n_step)
  create_vehicles(n_step)
  reroute_vehicles(n_step)
  remove_vehicles_at_exits()
  return
# end timestep


###############################
# Creates a vehicle with a random route and destination.
###############################
def create_vehicles(n_step):
  
  # Check if the maximum amount of vehicles are in the simulation
  if (config.n_vehicles_max <= len(traci.vehicle.getIDList())):
    return
  
  # Vehicle Creation
  if (n_step % config.n_vehicle_spawn_rate == 0):
    global N_VEHICLES
    s_vehicle_id = "veh" + str(N_VEHICLES) # vehX
    s_edge_init = ""
    s_edge_dest = ""
    
    # Choose an edge to start at.
    n_index_init = random.randint(0,len(config.ls_init_edges)-1)
    s_edge_init = config.ls_init_edges[n_index_init]
	
    if not s_edge_init in config.ls_interstate_edges:
      n_random_number = random.randint(1,3)
      if not n_random_number == 3:
        return
    
    # Create a route to start at if neccesary.
    if not ('RT' + s_edge_init) in traci.route.getIDList():
      traci.route.add('RT' + s_edge_init,[s_edge_init])
    
    # We want half of the vehicles to travel eastbound and half
    # To travel westbound.
    traci.vehicle.add(s_vehicle_id, 'RT' + s_edge_init, typeID="chevy_s10")
    
    # Choose an edge to end at.
    while True:
      n_index_dest = random.randint(0,len(config.ls_init_edges)-1)
      if not n_index_dest == n_index_init:
        break
    s_edge_dest = config.ls_init_edges[n_index_dest]
    
    # Increment vehicle num counter to keep IDs unique.
    N_VEHICLES += 1
    
    try:
      # Assign them a route.
      traci.vehicle.changeTarget(s_vehicle_id,s_edge_dest)
    except:
      pause()
    
    return
  # end if (n_step % N_VEHICLE_SPAWN_RATE == 0):
# end def create_vehicle


###############################
# Reroutes a vehicle someplace else
###############################
def reroute_vehicles(n_step):
  if (config.n_vehicle_reroute_rate == 0):
    return
  
  ls_vehicle_ids = traci.vehicle.getIDList()
  if len(ls_vehicle_ids) == 0:
    return
  
  # Vehicle Creation
  if (n_step % config.n_vehicle_reroute_rate == 0):
    # Initial Variables
    s_vehicle_id = ""
    s_edge_dest = ""
    
    # Pick a vehicle at random
    n_index_vehicle = random.randint(0,len(ls_vehicle_ids)-1)
    s_vehicle_id = ls_vehicle_ids[n_index_vehicle]
    
    # Pick a destination at random
    n_index_edge = random.randint(0,len(config.ls_exit_edges)-1)
    s_edge_dest = config.ls_exit_edges[n_index_edge]
    
    # Reroute it
    traci.vehicle.changeTarget(s_vehicle_id,s_edge_dest)

    return
  # end if (n_step % config.n_vehicle_reroute_rate == 0):
# end def reroute_vehicles(n_step)


###############################
# Remove vehicles on exit edges
###############################
def remove_vehicles_at_exits():
  ls_vehicle_ids = traci.vehicle.getIDList()
  for s_veh_id in ls_vehicle_ids:
    if traci.vehicle.getRoadID(s_veh_id) in config.ls_exit_edges:
      traci.vehicle.remove(s_veh_id)
# end def remove_veh_at_exits():


###############################
# The main entry point of the script.
###############################
main()

