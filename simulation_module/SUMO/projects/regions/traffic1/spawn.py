import config

###############################
# Add a vehicle to the simulation
#
# @param traci = traci instance
# @param N_VEHICLES = current number of vehicles
# @param s_route_start = id of the starting route
# @param s_edge_end = id of the sink edge
# @param color = color default(silver)
###############################
def add_vehicle(traci,N_VEHICLES,s_route_start,s_edge_end,color=(180,180,180)):
  s_veh_id = 'veh' + str(N_VEHICLES)
  traci.vehicle.add(s_veh_id,s_route_start,typeID='vw_super',departLane='random')
  traci.vehicle.changeTarget(s_veh_id,s_edge_end)
  traci.vehicle.setColor(s_veh_id,color)
  return(N_VEHICLES + 1)
# end def add_vehicle():

###############################
# Choose a route given a probability between 0 and 1
#
# @param f_rand = probability between 0 and 1
# @param lf_prob = list of probabilities
###############################
def sink_from_prob(f_rand,lf_prob):
  # Generate a additive list of sink probabilities
  f_val = 0.0
  llsf_sink_prob = []
  for i in range(len(config.ls_sink_ids)):
    if lf_prob[i] == 0.0: continue
    llsf_sink_prob.append([config.ls_sink_ids[i],f_val])
    f_val += lf_prob[i]
  # end for
  del f_val
  
  # Find the range which f_rand belongs
  s_sink = ''
  for lsf_sink_prob in llsf_sink_prob:
    if lsf_sink_prob[1] <= f_rand:
      s_sink = lsf_sink_prob[0]
    else: break
  # end for

  return(s_sink)
# end def sink_from_prob(f_rand,lf_prob):

###############################
# generates through traffic
#
# @param traci = traci instance
# @param n_step = simlation step
# @param N_VEHICLES = current number of vehicles
# @param random = random object
###############################
def spawn_tts(traci,n_step,N_VEHICLES,random):
  # if there's room to spawn more vehicles
  if len(traci.vehicle.getIDList()) < config.n_vehicles_max:
    for i in range(len(config.ln_tts)):
      if n_step % config.ln_tts[i] == 0:
        f_rand = random.random()
        s_sink = sink_from_prob(f_rand,config.llf_prob_sink[i])
        N_VEHICLES = add_vehicle(traci,N_VEHICLES,config.ls_ttir[i],s_sink)
      # end if
    # end for
  return(N_VEHICLES)
# end def spawn_tts
