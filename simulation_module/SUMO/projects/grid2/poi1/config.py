import os
###############################
#      Runner.py Configuration
###############################
s_absolute_path = os.path.dirname(os.path.abspath(__file__))
s_sumo_tools_dir = "/home/veins/src/sumo-0.30.0/tools"
s_route_file = s_absolute_path + "/../data/grid2.rou.xml"
s_sumocfg_file = s_absolute_path + "/../data/grid2.sumocfg"
n_time_steps = 10000

###############################
#      ex4 configuration
###############################

# The properties of our vehicles
s_vtype = """<vType id="chevy_s10" accel="0.6" decel="1.3" sigma="0.4" length="5" minGap="2.5" maxSpeed="3" guiShape="passenger"/>"""

# Some premade colors
lsn_colors = [(255,0,0,0),(0,255,0,0),(0,0,255,0),(255,255,0,0),(255,0,255,0),(0,255,255,0)]

# Seed for Random
n_seed = 777333

# How many time steps between new vehicles spawning?
n_vehicle_spawn_rate=10

# The maximum number of vehicles that may exist in the simulation.
n_vehicles_max=100 

# How often to reroute a vehicle into town.
n_go_downtown_rate=20

#[x,y] coordinates of all POI.
llf_poi_coords = [[23.0,-25.0],[24.0,34.0],[95.0,33.0],[104.0,-15.0],[142.0,-45.0],[187.0,32.0]] 

# Initial worth of a fresh POI node
f_initial_poi_value=0.50

# How many timesteps should a pass between increasing poi value.
n_poi_value_update_rate=10 

# The amount of value that the poi gains each update.
f_poi_value_inc_amt=0.10 

# The amount that the poi value will decrease with every hit.
f_poi_value_dec_amt=1.50

# The maximum value that a POI may be.
f_poi_value_max=2.00
