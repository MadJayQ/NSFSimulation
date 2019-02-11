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
N_VEHICLES = 0
LLS_VEH_DATA = [] #[s_veh_id,s_exit_dest_edge,s_next_dest_edge]


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

  # Most of the vehicles are going to travel along the 4-lane highway
  # so we'll create two starting points, one at either end.
  traci.route.add("eastbound",["gneE52"])
  traci.route.add("westbound",["-gneE50"])
  debug("routes sucessfully added.")
  
  return
# end def intialize


###############################
# Anything that happens within the TraCI control loop goes here.
# One pass of the loop == 1 timestep.
###############################
def timestep(n_step):  
  create_vehicles(n_step)
  go_downtown(n_step)
  
  # If the vehicles that went downtown have reached their destination.
  # they will head towards their original exit.
  for ls_row in LLS_VEH_DATA:
    # 0 is the vehicle ID and 2 is the next destination
    try:
      if (traci.vehicle.getRoadID(ls_row[0]) == ls_row[2]):
        # The vehicle has arived, send it on it's way. The exit destination
        # 1 is the exit edge
        traci.vehicle.changeTarget(ls_row[0],ls_row[1])
        
        # Change the color to blue so we can recognize accomplished cars
        traci.vehicle.setColor(ls_row[0],(0,0,255,0))
        
        # remove the vehicle from the list since we no longer have a
        LLS_VEH_DATA.remove(ls_row)
      # end if
      
    # This exception is called when a vehicle teleports beyond the ending
    #  destination and doesn't get properly removed from this list. I need
    #  to find some way to recognize when something teleports and remove
    #  it, or find handle it some other way.
    except:
      LLS_VEH_DATA.remove(ls_row)
      #debug("\n" + ls_row[0] + " >> " + ls_row[2])
      #debug(LLS_VEH_DATA)
      #pause()
        
  # for (ls_row in LLS_EXIT_DEST):
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
    s_dest_edge = ""
    
    # We want half of the vehicles to travel eastbound and half
    # To travel westbound.
    if (random.uniform(0.0,1.0) > 0.5):
      traci.vehicle.add(s_vehicle_id, "eastbound", depart=n_step+1, pos=-4, speed=-3, lane=-6, typeID="chevy_s10")
      s_dest_edge = "gneE50"
    else:
      traci.vehicle.add(s_vehicle_id, "westbound", depart=n_step+1, pos=-4, speed=-3, lane=-6, typeID="chevy_s10")
      s_dest_edge = "-gneE52"
    N_VEHICLES += 1
    
    # Assign them a route.
    traci.vehicle.changeTarget(s_vehicle_id,s_dest_edge)
    
  # end if (n_step % N_VEHICLE_SPAWN_RATE == 0):
# end def create_vehicle


###############################
# Go downtown
# Sends a vehicle downtown and then reroutes to it's exit destination.
###############################
def go_downtown(n_step):
  # Every x timesteps we're going to reroute a vehicle at random to
  # some point in town.
  if (n_step % config.n_go_downtown_rate == 0 and n_step != 0):
    # Pick a vehicle at random to reroute.
    ls_veh_ids = traci.vehicle.getIDList()
    n_random_int = random.randint(0,len(ls_veh_ids)-1)
    s_veh_id = ls_veh_ids[n_random_int]
    
    # We'll makes going downtown red.
    traci.vehicle.setColor(s_veh_id,(255,0,0,0))
    
    # Store the exit destination edge before we change it's route.
    s_exit_edge = traci.vehicle.getRoute(s_veh_id)[-1]
    
    # Send it someplace downtown.
    s_dest_edge = "-gneE35"
    traci.vehicle.changeTarget(s_veh_id,s_dest_edge)
      
    # Add it to LLS_VEH_DATA to be tracked.
    global LLS_VEH_DATA
    is_found = False
    for ls_row in LLS_VEH_DATA:
      if (s_veh_id == ls_row[0]):
        is_found = True
    if (not is_found):
        LLS_VEH_DATA.append([s_veh_id,s_exit_edge,s_dest_edge])
    
  #end if (n_step % n_reroute_rate == 0):
# end deg go_downtown()


###############################
# The main entry point of the script.
###############################
main()

