import os
###############################
#      Runner.py Configuration
###############################
s_absolute_path = os.path.dirname(os.path.abspath(__file__))
s_sumo_tools_dir = "/home/veins/src/sumo-0.30.0/tools"
s_route_file = s_absolute_path + "/../data/3choices.rou.xml"
s_sumocfg_file = s_absolute_path + "/../data/3choices.sumocfg"
n_time_steps = 3000

