import os
###############################
#      Runner.py Configuration
###############################
s_absolute_path = os.path.dirname(os.path.abspath(__file__))
s_sumo_tools_dir = "/home/veins/src/sumo-0.30.0/tools"
s_route_file = s_absolute_path + "/../data/3choices.rou.xml"
s_sumocfg_file = s_absolute_path + "/../data/3choices.sumocfg"
n_time_steps = 3000

###############################
#      ex4 configuration
###############################
s_vtype = """<vType id="chevy_s10" accel="0.6" decel="1.3" sigma="0.4" length="5" minGap="2.5" maxSpeed="10" guiShape="passenger"/>"""
lsn_colors = [(255,0,0,0),(0,255,0,0),(0,0,255,0),(255,255,0,0),(255,0,255,0),(0,255,255,0)]
n_seed = 777333
n_vehicle_spawn_rate=20 # How many time steps between new vehicles spawning?
n_vehicles_max=1 # The maximum number of vehicles that may exist in the simulation.
