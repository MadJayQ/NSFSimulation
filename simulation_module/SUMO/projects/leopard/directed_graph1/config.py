import os
###############################
#      Runner.py Configuration
###############################
s_absolute_path = os.path.dirname(os.path.abspath(__file__))
s_sumo_tools_dir = "/home/veins/src/sumo-0.30.0/tools"
s_route_file = s_absolute_path + "/../data/leopard.rou.xml"
s_sumocfg_file = s_absolute_path + "/../data/leopard.sumocfg"
n_time_steps = 10000

###############################
#      ex4 configuration
###############################

# Random Seed
n_seed = 666

# The properties of our vehicles
s_vtype = """<vType id="chevy_s10" accel="0.6" decel="1.3" sigma="0.4" length="5" minGap="2.5" maxSpeed="3" guiShape="passenger"/>"""

# Maximum number of vehicles in the simulation
n_vehicles_max = 100
# Timesteps between vehicle spawns
n_vehicle_spawn_rate = 1
# Timesteps between vehicle reroute
n_vehicle_reroute_rate = 1
