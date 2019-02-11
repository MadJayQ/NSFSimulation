# Author: Quentin Goss
# Last Modified: 9/2/18

class Cell:
  # Constructor
  # @param lf_top_left_coords = [float x, float y]
  # @param n_id = int - unique id
  #  of the top left point
  def __init__(self,lf_top_left_coords,n_id):
    self.lf_top_left_coords  = lf_top_left_coords
    self.n_id = n_id
    self.is_active = False
    
  def get_top_left_coords(self):
    return lf_top_left_coords
    
  def get_id(self):
    return self.n_id
  
  def get_is_active(self):
    return self.is_active
    
  def activate(self):
    self.is_active = True
# end class cell
