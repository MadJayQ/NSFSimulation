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
import poi

###############################
# Global Variables
###############################
N_VEHICLES = 0
LLS_VEH_DATA = [] #[s_veh_id,s_exit_dest_edge,s_next_dest_edge]
L_POIS = [] #POI objects


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
  create_pois()
  
  return
# end def intialize


###############################
# Anything that happens within the TraCI control loop goes here.
# One pass of the loop == 1 timestep.
###############################
def timestep(n_step):  
  create_vehicles(n_step)
  go_downtown(n_step)
  handle_lls_veh_data(n_step)
  poi_value_update(n_step)
  
  return
# end timestep


###############################
# Create POIs
###############################
def create_pois():
  # We're going to add a few points of interest before we start. This
  # will give our vehicles something to travel too.
  s_poi_id = ""
  n_pois = 0
  global L_POIS
  for lf_poi in config.llf_poi_coords:
    s_poi_id = "poi" + str(n_pois)
    
    # traci.poi.add( ID, x, y, Color, arbitrary desc., layer) 
    traci.poi.add(s_poi_id, lf_poi[0], lf_poi[1], (100,100,100,0), poiType="taco_cart",layer=0)
    
    # Finds the closest edge to an xy coordinate.
    # (edgeID, closest_edge_x, closest_edge_y)
    s_sff_road = traci.simulation.convertRoad(lf_poi[0],lf_poi[1],isGeo=False)
    
    # Create a POI object
    o_poi = poi.poi(s_poi_id,lf_poi[0],lf_poi[1], config.f_initial_poi_value, s_sff_road)
    
    # Set Decrement Amount
    # This is will be the amount the Value will decrease every POI Update
    o_poi.setDecreaseValue(config.f_poi_value_dec_amt) 
    
    # Add the object to the list of POIs.
    L_POIS.append(o_poi)
    
    n_pois += 1
  # end for lf_poi in config.llf_poi_coords:
  debug("POIs sucessfully added.")
# end def create_pois()


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
    # In case the same vehicle gets rerouted, we'll make sure that
    # it doesn't set it's ecit edge to a non-exit
    global LLS_VEH_DATA 
    ls_exit_edges = ["gneE52","-gneE52","gneE50","-gneE50"]
    s_edge = traci.vehicle.getRoute(s_veh_id)[-1]
    # It's being rerouted for the 1st time.
    if (s_edge in ls_exit_edges):
      s_exit_edge = s_edge
    # It's being rerouted for the 2nd or more time.
    else:
      for ls_row in LLS_VEH_DATA:
        if (s_veh_id == ls_row[0]):
          s_exit_edge = ls_row[1]
          
    # Send it to a poi node downtown at random
    global L_POIS
    n_random_int = random.randint(0,len(L_POIS)-1)
    s_dest_edge = L_POIS[n_random_int].getClosestEdge()[0]
    traci.vehicle.changeTarget(s_veh_id,s_dest_edge)
      
    # Add it to LLS_VEH_DATA to be tracked.
    # If a record already exists remove it so we can update   
    for ls_row in LLS_VEH_DATA:
      if (s_veh_id == ls_row[0]):
        LLS_VEH_DATA.remove(ls_row)
    # Add to history.
    LLS_VEH_DATA.append([s_veh_id,s_exit_edge,s_dest_edge])
    
  #end if (n_step % n_reroute_rate == 0):
# end deg go_downtown()


###############################
# Handle LLS_VEH_DATA
#
# Loops through all vehicles in LLS_VEH_DATA and check to if they've
# arrived at their destinations.
###############################
def handle_lls_veh_data(n_step):
  # If the vehicles that went downtown have reached their destination.
  # they will head towards their original exit.
  global LLS_VEH_DATA
  global L_POIS
  s_veh_id = ""
  s_exit_edge = ""
  s_dest_edge = ""
  for ls_row in LLS_VEH_DATA:
    # 0 is the vehicle ID and 2 is the next destination
    # Is the vehicle on it's destination edge?
    s_veh_id = ls_row[0]
    s_dest_edge = ls_row[2]
    if (traci.vehicle.getRoadID(s_veh_id) == s_dest_edge):
      # The vehicle has arived, send it on it's way. The exit destination
      # 1 is the exit edge
      s_exit_edge = ls_row[1]
      traci.vehicle.changeTarget(s_veh_id,s_exit_edge)
      
      # Change the color to blue so we can recognize accomplished cars
      traci.vehicle.setColor(s_veh_id,(0,0,255,0))
      
      # Locate the POI that we arrived at. Find the POI that is 
      # nearest to the edge we're on.
      for poi in L_POIS:
        if (s_dest_edge == poi.getClosestEdge()[0]):    
          poi.vehicleHit(n_step,s_veh_id)
          break

      # remove the vehicle from the list since we no longer need to
      # track it.
      LLS_VEH_DATA.remove(ls_row)
    # end if
  # for (ls_row in LLS_EXIT_DEST):
# end def handle_lls_veh_data():


###############################
# Handle POI value update.
# Loops through the L_POIS list. Anything that happens during a POI
# value update goes here.
###############################
def poi_value_update(n_step):
  # Handle POI value update.
  if (n_step % config.n_poi_value_update_rate == 0):
    global L_POIS
    for poi in L_POIS:
      # Value increases over time
      poi.increaseValueBy(config.f_poi_value_inc_amt)
      # Make sure that the value can't increase over max
      if (poi.getValue() > config.f_poi_value_max):
        poi.setValue(config.f_poi_value_max)
      
      # Update color to reflect value
      # We want low values to be blue and high values to be green
      # Colors are (red, green, blue, alpha)
      n_color_intensity = int((poi.getValue() / config.f_poi_value_max) * 255)
      if (poi.getValue() < 0):
        traci.poi.setColor(poi.getID(),(255,0,0,0))
      elif (poi.getValue() > 255):
        traci.poi.setColor(poi.getID(),(0,255,0,0))
      else:
        traci.poi.setColor(poi.getID(),(255-n_color_intensity,0+n_color_intensity,0,0))
    # end for o_poi in L_POIS:
  # end if (n_step % config.n_poi_value_update_rate):
# end def handle_poi_operations


###############################
# The main entry point of the script.
###############################
main()

