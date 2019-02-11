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
import poi
import vehicle


###############################
# Global Variables
###############################
N_VEHICLES = 0
IS_FIFTH_VEH_SPAWNED = False
L_POIS = [] #POI objects
L_VEHICLES = [] #Vehicle objects


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
  choose_vehicle_to_reroute(n_step)
  handle_vehicles(n_step)
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
    t_sff_road = traci.simulation.convertRoad(lf_poi[0],lf_poi[1],isGeo=False)
    
    # Create a POI object
    o_poi = poi.poi(s_poi_id,lf_poi[0],lf_poi[1], config.f_initial_poi_value, t_sff_road)
    
    # Set Decrement Amount
    # This is will be the amount the Value will decrease every POI Update
    o_poi.setDecreaseValue(config.f_poi_value_dec_amt) 
    
    # Add the object to the list of POIs.
    L_POIS.append(o_poi)
    
    n_pois += 1
  # end for lf_poi in config.llf_poi_coords:
  del s_poi_id
  del n_pois
  del o_poi
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
      traci.vehicle.add(s_vehicle_id, "eastbound", typeID="chevy_s10")
      s_dest_edge = "gneE50"
    else:
      traci.vehicle.add(s_vehicle_id, "westbound", typeID="chevy_s10")
      s_dest_edge = "-gneE52"
    N_VEHICLES += 1
    
    # Assign them a route.
    traci.vehicle.changeTarget(s_vehicle_id,s_dest_edge)
    
    del n_step
    del s_vehicle_id
    del s_dest_edge
  # end if (n_step % N_VEHICLE_SPAWN_RATE == 0):
# end def create_vehicle


###############################
# Picks a vehicle at random to reroute.
###############################
def choose_vehicle_to_reroute(n_step):
  # The fifth vehicle to spawn will always be rerouted first.
  global IS_FIFTH_VEH_SPAWNED
  if not IS_FIFTH_VEH_SPAWNED:
    if "veh5" in traci.vehicle.getIDList():
      IS_FIFTH_VEH_SPAWNED = True
      s_veh_id = "veh5"
      
      # Change color to orange.
      traci.vehicle.setColor(s_veh_id,(255,0,0,0))
      
      # Create a new vehicle object
      veh = retrieve_vehicle(s_veh_id)
      
      # Route the vehicle to the first poi
      go_to_poi(veh)
      
      del n_step
      del s_veh_id
      del veh

  # Every x timesteps we're going to reroute a vehicle at random to
  # some point in town.
  else:
    if (n_step % config.n_go_downtown_rate == 0 and n_step != 0):
      # Pick a vehicle at random to reroute.
      ls_veh_ids = traci.vehicle.getIDList()
      n_random_int = random.randint(0,len(ls_veh_ids)-1)
      s_veh_id = ls_veh_ids[n_random_int]
      
      # Change color to orange.
      traci.vehicle.setColor(s_veh_id,(255,0,0,0))
      
      # Create a new vehicle object
      veh = retrieve_vehicle(s_veh_id)
      
      # Route the vehicle to the first poi
      go_to_poi(veh)
      
      del n_step
      del ls_veh_ids
      del n_random_int
      del s_veh_id
      del veh
# end def choose_vehicle_to_reroute:


###############################
# Go to POI
# Sends a vehicle to a POI
###############################
def go_to_poi(veh):       
  # Send it to the POI with the most value
  global L_POIS
  n_max_val = -1
  l_poi_max = []
  s_dest_edge = ""
  for poi in L_POIS:
    # If we've already visited it, don't check it.
    if poi.getID() in veh.get_visited_pois():
      continue
    
    # Find the POI with the most value
    elif poi.getValue() >= n_max_val:
      l_poi_max.append(poi)
      # Compare vs the record list if there's more than one item in it.
      if len(l_poi_max) > 1:
        # If the recorded pois are less than the current, remove it 
        # from the tracking list.
        for poi_max in l_poi_max:
          if poi_max.getValue() < poi.getValue():
            l_poi_max.remove(poi_max)
    # End elif
  # End for
 
  # If there are more than one candidates, meaning that at least two
  # POIs have the same value, we'll compare distances.
  if len(l_poi_max) > 1:
    f_distance = -1.0
    f_closest_dist = -1.0
    l_poi_closest = []
    for poi_max in l_poi_max:
      # We can determine the distance by assigning a route to each poi
      # and then calling getDrivingDistance to find the distance retured
      # as a double
      s_dest_edge = poi_max.getClosestEdge()[0]
      traci.vehicle.changeTarget(veh.get_id(),s_dest_edge)
      f_distance = traci.vehicle.getDrivingDistance(veh.get_id(),s_dest_edge,1.0)
      
      # Compare distances
      # We automatically consider the first one
      if f_closest_dist == -1.0:
        f_closest_dist = f_distance
        l_poi_closest.append([poi_max,f_distance])
      # We check the other ones in the list
      else:
        # Add possible contendors to list.
        if f_distance <= f_closest_dist:
          f_closest_dist = f_distance
          l_poi_closest.append([poi_max,f_distance])
          # Remove non-contendors from the list
          for poi_closest in l_poi_closest:
            if poi_closest[1] > f_distance:
              l_poi_closest.remove(poi_closest)
          # end for poi_closest in l_poi_closest:
        # end if f_distance <= f_closest_dist:
      # end else
    # end for poi_max in l_poi_max:
    
    # If the two values are the same, one of POIs will be picked at random.
    if len(l_poi_closest) > 1:
      n_random_int = random.randint(0,len(l_poi_closest))
      s_dest_edge = l_poi_closest[n_random_int][0]
      del n_random_int
    # end if len(l_poi_closest) > 1:
    else:
      s_dest_edge = l_poi_closest[0][0].getClosestEdge()[0]
    
    del f_distance
    del f_closest_dist
    del l_poi_closest
  # end if len(l_poi_max) > 1:
  else:
    s_dest_edge = l_poi_max[0].getClosestEdge()[0]
  
  # Send it to the POI
  traci.vehicle.changeTarget(veh.get_id(),s_dest_edge)
    
  # Store the current destination edge
  veh.set_next_dest_edge_id(s_dest_edge)
  
  # Add it to L_VEHICLES to be tracked.
  global L_VEHICLES
  L_VEHICLES.append(veh)
  
  del veh
  del n_max_val
  del l_poi_max
  del s_dest_edge
# end deg go_downtown()


###############################
# Handle L_VEHICLES
#
# Control loop for tracked vehicles
###############################
def handle_vehicles(n_step):
  global L_VEHICLES
  global L_POIS
  for veh in L_VEHICLES:
    # If the vehicle has arrived at it's destination
    if traci.vehicle.getRoadID(veh.get_id()) == veh.get_next_dest_edge_id():     
      # Locate the POI that we arrived at. Find the POI that is 
      # nearest to the edge we're on.
      for poi in L_POIS:
        if (veh.get_next_dest_edge_id() == poi.getClosestEdge()[0]):    
          # "Hit" the POI
          poi.vehicleHit(n_step,veh.get_id())
          
          # Add the POI to list of visited POIs.
          veh.add_visited_pois(poi.getID())
          
          # Reduce Capacity
          n_amt = int(poi.getValue() * 100.0)
          veh.increase_capacity(0-n_amt)
          
          # Update vehicle Color
          update_vehicle_color(veh)
          break
      # End for
      
      # Is the vehicle full (capacity = 0) or has it visted all the POIs?
      # We'll use some flags to reduce redundant checks
      is_full = False
      is_bored = False
      if veh.get_capacity() == 0:
        is_full = True
      elif len(veh.get_visited_pois()) == len(L_POIS):
        is_bored = True
        
      if is_full or is_bored :
        # Go home
        traci.vehicle.changeTarget( veh.get_id(), veh.get_final_dest_edge_id())
        
        # Change color so we can see when cars go home. The colors will
        # vary by reason for going home.
        # REASON: No more capacity. Cars will turn CYAN.
        if is_full:
          traci.vehicle.setColor(veh.get_id(),(0,255,255,0))
        # REASON: Visited every unique POI. Cars will turn GREEN  
        elif is_bored:
          traci.vehicle.setColor(veh.get_id(),(0,255,0,0))
        # REASON: Unknown. Cars will turn DARK GREY
        # If cars are grey, there's a logic problem!
        else:
          traci.vehicle.setColor(veh.get_id(),(30,30,30,0))
        
        # remove the vehicle from the list since we no longer need to
        # track it.
        L_VEHICLES.remove(veh)
        
      # Otherwise send it to another poi
      else:
        # Reroute vehicles to another POI
        go_to_poi(veh)
        
    # end if target arrives at destination
  # end for veh in L_VEHICLES:
# end def handle_vehicles(n_step):


###############################
# Update vehicle Color
###############################
def update_vehicle_color(veh):
  n_capacity = veh.get_capacity()
  s_veh_id = veh.get_id()
  if n_capacity > 510:
    traci.vehicle.setColor(s_veh_id,(255,0,0,0))
  elif n_capacity > 255 and n_capacity <= 510:
    traci.vehicle.setColor(s_veh_id,(255,0,510-n_capacity,0))
  elif n_capacity >= 0 and n_capacity <= 255:
    traci.vehicle.setColor(s_veh_id,(0+n_capacity,0,255,0))
  else:
    traci.vehicle.setColor(s_veh_id,(0,255,255,0))
    
  del veh
  del n_capacity
  del s_veh_id
# def update_vehicle_color(veh):


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
  
  del n_step
# end def handle_poi_operations


###############################
# Retrieve vehicle
#
# Get a vehicle already being tracked in L_VEHICLES
# or create a new one if it doesn't exist.
###############################
def retrieve_vehicle(s_veh_id):
  global L_VEHICLES
  veh = vehicle.vehicle(s_veh_id)
  # If we're already tracking the vehicle in L_VEHICLES then we
  # can copy the existing one. We'll remove it from the list until
  # we're finished modifying it.
  for _veh in L_VEHICLES:
    if _veh.get_id() == s_veh_id: 
      veh = _veh
      L_VEHICLES.remove(_veh)
      break
        
  # Store the exit destination edge before we change route
  # so that we keep memory of where the vehicle was supposed
  # to go.
  if veh.get_final_dest_edge_id() == "":
    veh.set_final_dest_edge_id(traci.vehicle.getRoute(s_veh_id)[-1])
    
  # Set the capacity of the vehicle if it doesn't have one yet
  if veh.get_capacity() == -1:
    veh.set_capacity(random.randint(config.n_min_capacity, config.n_max_capacity))
    
  del s_veh_id
  return veh
# end def retrieve_vehicle(veh):


###############################
# The main entry point of the script.
###############################
main()

