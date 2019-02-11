import os
###############################
#      Runner.py Configuration
###############################
s_absolute_path = os.path.dirname(os.path.abspath(__file__))
s_sumo_tools_dir = "C:/Program Files (x86)/Eclipse/Sumo/tools"
s_route_file = s_absolute_path + "/../data/regions.rou.xml"
s_sumocfg_file = s_absolute_path + "/../data/regions.sumocfg"
s_net_file = s_absolute_path + "/../data/regions.net.xml"
n_time_steps = 10000

###############################
#      ex4 configuration
###############################

# Random Seed
n_seed = 666

# The properties of our vehicles
s_vtype = """<vType id="vw_super" accel="0.6" decel="1.3" sigma="0.4" length="5" minGap="2.5" maxSpeed="3" guiShape="passenger"/>"""

# Maximum number of vehicles in the simulation
n_vehicles_max = 100

# Through Traffic Initial Route names
ls_ttir = ['north','east','west','southwest','southeast'] 

# Through Traffic spawnrates (by tick)
n_tts_north = 5
n_tts_east = 3
n_tts_west = 3
n_tts_southwest = 20
n_tts_southeast = 20
ln_tts = [n_tts_north,n_tts_east,n_tts_west,n_tts_southwest,n_tts_southeast]

# Edge IDs of Map Spawns
s_spawn_north = 'gneE71'
s_spawn_east = 'gneE160'
s_spawn_west = 'gneE172'
s_spawn_southwest = '-gneE14'
s_spawn_southeast = '-gneE110'
ls_spawn_ids = [s_spawn_north,s_spawn_east,s_spawn_west,s_spawn_southwest,s_spawn_southeast]

# Edge IDs of Map Sinks
s_sink_north = '-gneE71'
s_sink_east = 'gneE159'
s_sink_west = 'gneE166'
s_sink_southwest = 'gneE14'
s_sink_southeast = 'gneE110'
ls_sink_ids = [s_sink_north,s_sink_east,s_sink_west,s_sink_southwest,s_sink_southeast]

# Probablities of visiting each sink from a spawn
# [north, east, west, southwest, southeast]
lf_prob_sink_north = [0.0,0.4,0.4,0.1,0.1]
lf_prob_sink_east = [0.2,0.0,0.6,0.1,0.1]
lf_prob_sink_west = [0.2,0.6,0.0,0.1,0.1]
lf_prob_sink_southwest = [0.4,0.1,0.4,0.0,0.1]
lf_prob_sink_southeast = [0.3,0.3,0.3,0.1,0.0]
llf_prob_sink = [lf_prob_sink_north,lf_prob_sink_east,lf_prob_sink_west,lf_prob_sink_southwest,lf_prob_sink_southeast]
