# Traci Vehicle Module
# Origin: /sumo_master/modules/vehicle.py
# Created By: Quentin Goss
# Last Modified: 08/01/2018
class vehicle:
  def __init__(self, s_id):
    self.s_id = s_id
    self.s_next_dest_edge_id = ""
    self.s_final_dest_edge_id = ""
    self.n_capacity = -1
    self.ls_visited_pois = []
    
  def __del__(self):
    del self.s_id
    del self.s_next_dest_edge_id
    del self.s_final_dest_edge_id
    del self.n_capacity
    del self.ls_visited_pois
    
  def get_id(self):
    return self.s_id
  def set_id(self,ps_id):
    self.s_id = ps_id
    
  def get_next_dest_edge_id(self):
    return self.s_next_dest_edge_id
  def set_next_dest_edge_id(self,ps_next_dest_edge_id):
    self.s_next_dest_edge_id = ps_next_dest_edge_id
    
  def get_final_dest_edge_id(self):
    return self.s_final_dest_edge_id
  def set_final_dest_edge_id(self,ps_final_dest_edge_id):
    self.s_final_dest_edge_id = ps_final_dest_edge_id
    
  def get_capacity(self):
    return self.n_capacity
  def set_capacity(self,pn_capacity):
    self.n_capacity = pn_capacity
  def increase_capacity(self,n_amount):
    self.n_capacity += n_amount
    if self.n_capacity < 0:
      self.n_capacity = 0
    
  def get_visited_pois(self):
    return self.ls_visited_pois
  def set_visited_pois(self,pls_visited_pois):
    self.ls_visited_pois = pls_visited_pois
  def add_visited_pois(self,s_poi_id):
    if s_poi_id in self.ls_visited_pois:
      return
    else:
      self.ls_visited_pois.append(s_poi_id)
  def discard_visited_pois(self,s_poi_id):
    self.ls_visited_pois.remove(s_poi_id)
# end class vehicle 
