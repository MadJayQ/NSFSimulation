# Author: Quentin Goss
# Last Modified: 9/3/18

class Junction:
  # Constructor
  # @param lf_center_coords = [float x, float y]
  # @param n_id = int - unique id
  def __init__(self,lf_center_coords,s_id):
    self.lf_center_coords = lf_center_coords
    self.s_id = s_id
    
    # Neighors
    # Nodes in which a edge goes FROM this junction TO another Junction
    # [string id, int index]
    self.ll_sn_neighbors = []
    
    # Center Point
    # Note that this is NOT the true center but rather
    # the adjust center to be placed on the graphics window
    # Use lf_center_coords for the true center.
    self.p_center = None
    
  def get_id(self):
    return self.s_id
    
  def get_center_coords(self):
    return self.lf_center_coords
    
  def get_neighbors(self):
    return self.ll_sn_neighbors
  # Add a neighbor
  # @param s_id = id of the neighbor to be added
  # @param index of neighbor for quick accesing during drawing.
  def add_neighbor(self,s_id,n_index):
    if s_id not in self.ll_sn_neighbors:
      self.ll_sn_neighbors.append([s_id,n_index])
    
  def get_center_point(self):
    return self.p_center   
  def set_center_point(self,p_point):
    self.p_center = p_point
# End class Junction

