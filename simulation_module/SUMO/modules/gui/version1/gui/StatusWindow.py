from graphics import *

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

# A status window displaying the grid for the current simulation.
class StatusWindow:
  
  def __init__(self,n_cell_width,s_path_of_net_xml):
    self.n_cell_width = n_cell_width
    self.s_path_of_net_xml = s_path_of_net_xml
    
    # Stores boundary info as [float x,float y]
    self.lf_bottom_left_boundaries = [0.00,0.00]
    self.lf_top_right_boundaries = [0.00,0.00]
    
    # Cell storage
    self.ll_cells = []
    
    # Window Options
    self.n_graph_padding = 10
    
    # Grid dimension initialization
    # [int columns, int rows]
    self.ln_grid_dimensions = [-1,-1]
    
    # Testing
    self.initialize()
    self.update()
    self.finalize()
  
  def initialize(self):
    # Split the grid into squares.
    self.get_boundaries()
    self.build_cells()
    self.disable_unused_cells()
    
    # Create the Window
    n_width = self.n_graph_padding * 2 + self.n_cell_width * self.ln_grid_dimensions[0]
    n_height = self.n_graph_padding * 2 + self.n_cell_width * self.ln_grid_dimensions[1]
    self.window = GraphWin("window title",n_width,n_height)
  # end def initialize()
  
  def update(self):
    # Draw Cells
    self.draw_cells()
  # end update
  
  def finalize(self):
    # Close window  
    input("Press return to finish.")
    self.window.close()
  # end def do_stuff
    
  # Obtain the coordinates of the bottom left and top right corner
  def get_boundaries(self):
    # We will use the net.xml file since it contains all of the edge
    # information.
    net_xml = open(self.s_path_of_net_xml)
    for s_line in net_xml:
      # "convBoundary" is an auto-generated boundary for everything
      # important in our map, so it's a good start for deciding
      # what the outer limits of our map should be.
      if "convBoundary" in s_line:
        s_line = s_line[s_line.index('convBoundary="')+len('convBoundary="'):-1]
        s_line = s_line[0:s_line.index('"')]
        self.lf_bottom_left_boundaries[0] = float(s_line[0:s_line.index(',')])
        s_line = s_line[s_line.index(',')+1:]
        self.lf_bottom_left_boundaries[1] = float(s_line[0:s_line.index(',')])
        s_line = s_line[s_line.index(',')+1:]
        self.lf_top_right_boundaries[0] = float(s_line[0:s_line.index(',')])
        s_line = s_line[s_line.index(',')+1:]        
        self.lf_top_right_boundaries[1] = float(s_line)
        print("_Boundaries_")
        print(self.lf_bottom_left_boundaries)
        print(self.lf_top_right_boundaries)
        print()
        #input("Press return to continue.")
        break
    net_xml.close()
  # end def get_boundaries
  
  # Creates cells and populates self.l_cells
  def build_cells(self):
    # The first cell starts at the top left corner of the boundary.
    x = self.lf_bottom_left_boundaries[0]
    col = []
    n_num_cells = 0
    # Load cells into the cell list starting at the upper left
    # and going all the way down, then moving one column over
    # until we run out of candidates
    while x < self.lf_top_right_boundaries[0]:
      y = self.lf_top_right_boundaries[1]
      l_col = []
      while y > self.lf_bottom_left_boundaries[1]:
        cell = Cell([x,y],n_num_cells)
        l_col.append(cell)
        y -= self.n_cell_width  
        n_num_cells += 1
      # end while column
      self.ll_cells.append(l_col)
      x += self.n_cell_width
    # end while row
    #print("_cells_\n[cols,rows]")
    #print([len(self.ll_cells),len(self.ll_cells[0])])
    self.ln_grid_dimensions = [len(self.ll_cells),len(self.ll_cells[0])]
  # end def build cells
  
  def draw_cells(self):
    # draw cells
    n_cols = 0
    for l_col in self.ll_cells:
      n_rows = 0
      x = self.n_graph_padding + self.n_cell_width * n_cols
      for cell in l_col:
        y = self.n_graph_padding + self.n_cell_width * n_rows
        p_top_left = Point(x,y)
        p_bottom_right = Point(x+self.n_cell_width,y+self.n_cell_width)
        rect = Rectangle(p_top_left,p_bottom_right)
        rect.setFill("grey")
        
        # Is the cell active?
        if cell.get_is_active():      
          rect.draw(self.window)
          
        n_rows += 1
      # end for col
      n_cols += 1
    # end for row
  # end def draw_cells
  
  # Disable cells that contain no edges.
  def disable_unused_cells(self):
    # We will use the .net.xml file again since it contains all of
    # the edge information
    net_xml = open(self.s_path_of_net_xml)
    print(self.ln_grid_dimensions)
    for s_line in net_xml:
      if '<lane' in s_line in s_line:
        if 'shape=' in s_line:
          s_line = s_line[s_line.index('shape="') + len('shape="'):]
          s_line = s_line[:s_line.index('"/>')]
          ls_coords = s_line.split(' ')
          
          for pair in ls_coords:
            lf_coords = [float(pair.split(',')[0]),float(pair.split(',')[1])]
            ln_cell_index = self.coords_to_index(lf_coords)
            self.ll_cells[ln_cell_index[0]][ln_cell_index[1]].activate()
          # end for  
          
        # end if shape
      # end if gneE
    # end for

  # end def disable_unused_cells
  
  # Converts xy coordinates to an self.ll_cells cell index
  # @param lf_coords = [float x, float y]
  # @return = Returns the index of the cell in self.ll_cells in format
  #           [int column, int row]
  def coords_to_index(self,lf_coords):
    # Find the column
    # Account for floor rounding errors during cast from float to int
    if lf_coords[1] >= self.lf_top_right_boundaries[1]:
      n_col = self.ln_grid_dimensions[0] - 1
    else:
      f_boundary_height = self.lf_top_right_boundaries[1] - self.lf_bottom_left_boundaries[1]
      y = (lf_coords[1] - self.lf_bottom_left_boundaries[1]) / f_boundary_height
      n_col = int(y * self.ln_grid_dimensions[0])
    #print(n_col)
    
    # Find the row
    # Accout for floor rounding errors during cast from float to int
    if lf_coords[0] >= self.lf_top_right_boundaries[0]:
      n_row = self.ln_grid_dimensions[1] - 1
    else:
      f_boundary_width = self.lf_top_right_boundaries[0] - self.lf_bottom_left_boundaries[0]
      x = (lf_coords[0] - self.lf_bottom_left_boundaries[0]) / f_boundary_width
      n_row = int(x * self.ln_grid_dimensions[1])
    #print(n_row)
    
    return [n_col,n_row]
  # end def coords_to_index
# End class StatusWinow
