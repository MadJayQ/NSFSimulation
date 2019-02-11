import os
###############################
#      Runner.py Configuration
###############################
s_absolute_path = os.path.dirname(os.path.abspath(__file__))
s_sumo_tools_dir = "C:\Program Files (x86)\Eclipse\Sumo\tools"
s_route_file = s_absolute_path + "\..\data\diverging_diamond.rou.xml"
s_sumocfg_file = s_absolute_path + "\..\data\diverging_diamond.sumocfg"
s_net_file = s_absolute_path + "\..\data\diverging_diamond.net.xml"
n_time_steps = 10000

###############################
#      ex4 configuration
###############################

# Random Seed
n_seed = 666

# The properties of our vehicles
s_vtype = """<vType id="chevy_s10" accel="0.6" decel="1.3" sigma="0.4" length="5" minGap="2.5" maxSpeed="3" guiShape="passenger"/>"""

# Maximum number of vehicles in the simulation
n_vehicles_max = 30
# Timesteps between vehicle spawns
n_vehicle_spawn_rate = 1
# Timesteps between vehicle reroute
# if 0 they do not reroute
n_vehicle_reroute_rate = 0

# If a vehicle is on these edges, remove it.
ls_exit_edges = ["gneE71","gneE40","gneE62","gneE59"]

# Starting Edges
ls_init_edges = ["gneE35","gneE54","gneE61","gneE67"]

ls_interstate_edges = ["gneE54","gneE67"]