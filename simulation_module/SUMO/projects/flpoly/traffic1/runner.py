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
N_PEDS = 0

###############################
# Add element(s) to routefiles
#
# @return string = The elements that will be added to the #                             routefile.
###############################
def generate_elements(): 
  s_elements = "\t" + config.s_vtype_passenger + "\n"
  s_elements += "\t" + config.s_vtype_pedestrian
  return s_elements
# End def generate_elements()


###############################
# Initilize anything that needs to happen at step 0 here.
###############################
def initialize():
  traci.route.add("cw_route",config.cw_route)
  traci.route.add("ccw_route",config.ccw_route)
  debug("Routes sucessfully added.")
  
  # Create all the possible routes for pedestrians.
  n = 0
  for s_ped_edge in config.ls_ped_edges:
    ls_temp = []
    ls_temp.append(s_ped_edge)
    s_ped_edge_id = "pedge" + str(n) # pedgeX
    traci.route.add(s_ped_edge_id,ls_temp)
    n += 1
    
    #print()
    #debug(ls_temp)
    #pause()
  
  return
# end def intialize


###############################
# Anything that happens within the TraCI control loop goes here.
# One pass of the loop == 1 timestep.
###############################
def timestep(n_step): 
  create_vehicles(n_step)
  
  # Route building Logic
  if n_step < 0 :
    ls_veh_ids = traci.vehicle.getIDList()
    for s_veh_id in ls_veh_ids:
      s_dest_edge = "370373767#0"
      traci.vehicle.changeTarget(s_veh_id,s_dest_edge)
      
      print()
      debug(traci.vehicle.getRoute(s_veh_id))
      pause()
  
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
    s_veh_id = "veh" + str(N_VEHICLES) # vehX

    # We want half of the vehicles to travel eastbound and half
    # To travel westbound.
    f_rand_num = random.uniform(0,1)
    if f_rand_num < 0.5:
      traci.vehicle.add(s_veh_id, "ccw_route", depart=n_step+1, pos=-4, speed=-3, lane=-6, typeID="chevy_s10")
    else:
      traci.vehicle.add(s_veh_id, "cw_route", depart=n_step+1, pos=-4, speed=-3, lane=-6, typeID="chevy_s10")
    N_VEHICLES += 1
    
    del s_veh_id
    del f_rand_num
  # end if (n_step % N_VEHICLE_SPAWN_RATE == 0):
  """
  # Pedestrian creation
  if (n_step % config.n_ped_spawn_rate == 0):
    global N_PEDS
    s_ped_id = "ped" + str(N_PEDS) # pedX
    
    # Randomize the starting edge for pedestrians
    n_rand_int = random.randint(0,len(config.ls_ped_edges)-1)
    s_start_edge_id = "pedge" + str(n_rand_int)
    traci.vehicle.add(s_ped_id, s_start_edge_id, depart=n_step+1, pos=-4, speed=-3, lane=-6, typeID="bob")
    
    # Make the pedestrian's red
    traci.vehicle.setColor(s_ped_id,(255,0,0,0))
    
    
    # Sidewalk nodes are not complete enough to connect together
    # A complete revision of the pathways in this are required to
    # successfully move pedestrians along.
    try:
      n_old = n_rand_int
      while True:
        n_rand_int = random.randint(0,len(config.ls_ped_edges)-1)
        s_dest_edge = config.ls_ped_edges[n_rand_int]
        if n_old != n_rand_int:
          break
      traci.vehicle.changeTarget(s_ped_id,s_dest_edge)
    except:
      flag = True
      pause()
    
    N_PEDS += 1
    """
  # end if (n_step % config.n_ped_spawn_rate == 0):
  del n_step
# end def create_vehicle

###############################
# The main entry point of the script.
###############################
main()

