# Author: Quentin Goss
# Last modified: 9/3/18

from graphics import *
from Junction import Junction
from Cell import Cell
import json

# A status window displaying the grid for the current simulation.
class StatusWindow:
  
  def __init__(self,s_path_of_net_xml):
    self.s_path_of_net_xml = s_path_of_net_xml
    
    # Window Options
    self.s_window_title = ''
    self.is_cells_mode = False
    self.is_minimap_mode = False
    self.n_cell_width = 15
    self.n_graph_padding = 10
    self.n_edge_length_scale = 1
    self.n_window_max_width = 999999
    self.n_window_max_height = 999999
    
    # .json files
    self.s_junctions_json = './json/junctions.json'
    self.s_edges_json = './json/edges.json'
    
    # Generated window parameters
    self.n_window_width = -1
    self.n_window_height = -1
    
    # Stores boundary info as [float x,float y]
    self.lf_bottom_left_boundaries = [0.00,0.00]
    self.lf_top_right_boundaries = [0.00,0.00]
    self.f_boundary_width = 0
    self.f_boundary_height = 0
    
    # Cell storage
    self.ll_cells = []
    
    # Junction storage
    self.l_junctions = []
    self.n_junctions = -1
    self.n_edges = -1
    
    # Grid dimension initialization
    # [int columns, int rows]
    self.ln_grid_dimensions = [-1,-1]
  
  def get_window_title(self):
    return self.s_window_title
  def set_window_title(self,s_title):
    self.s_window_title = s_title
    
  def get_window_width(self):
    return self.n_window_width
  def get_window_height(self):
    return self.n_window_height
    
  def get_window_max_width(self):
    return self.n_window_max_width
  def get_window_max_height(self):
    return self.n_window_max_height
  # @ param n_width = width of window in pixels
  # @ param n_height = height of window in pixels
  def set_window_max_dimensions(self, n_width, n_height):
    self.n_window_max_width = n_width
    self.n_window_max_height = n_height
  
  def get_cells_mode(self):
    return self.is_cells_mode
  def set_cells_mode(self,is_option):
    self.is_cells_mode = is_option
    
  def get_minimap_mode(self):
    return self.is_minimap_mode
  def set_minimap_mode(self,is_option):
    self.is_minimap_mode = is_option
  
  def get_cell_width(self):
    return self.n_cell_width
  def set_cell_width(self,n_pixels):
    self.n_cell_width = n_pixels
    
  def get_graph_padding(self):
    return self.n_graph_padding
  def set_graph_padding(self,n_pixels):
    self.n_graph_padding = n_pixels
    
  def get_edge_length_scale(self):
    return self.n_edge_length_scale
  def set_edge_length_scale(self,n_scale):
    self.n_edge_length_scale = n_scale
  
  # Once Options are complete, create the graphic
  def build(self):
    self.initialize()
    self.update()
    self.finalize()
  
  def initialize(self):
    print("initializing...")
    # Split the grid into squares.
    self.get_boundaries()
    
    # We will always split the map into cells because the method is
    # not computationally expensive and we also use the list of cells
    # to determine the size of our status window.
    self.build_cells()
    
    # We will use the coordinates from our junctions to determine if
    # cells should remain active
    self.build_junctions()
    self.find_neighbors()
    
    if self.is_cells_mode:
      self.disable_unused_cells()
  
    self.create_window()
  # end def initialize()
  
  def update(self):
    print("\nupdating...")
  
    if self.is_cells_mode:
      self.draw_cells()
      
    if self.is_minimap_mode:
      self.draw_junctions()
      
  # end update
  
  def finalize(self):
    print("Finalizing...")
    # Close window  
    #input("Press return to finish.")
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
        
        self.f_boundary_width = self.lf_top_right_boundaries[0] - self.lf_bottom_left_boundaries[0]
        self.f_boundary_height = self.lf_top_right_boundaries[1] - self.lf_bottom_left_boundaries[1]
        #print("_Boundaries_")
        #print(self.lf_bottom_left_boundaries)
        #print(self.lf_top_right_boundaries)
        #print([self.f_boundary_width,self.f_boundary_height])
        #print()
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
      x = self.n_graph_padding + self.n_cell_width * n_cols * self.n_edge_length_scale
      for cell in l_col:
        y = self.n_graph_padding + self.n_cell_width * n_rows * self.n_edge_length_scale
        p_top_left = Point(x,y)
        p_bottom_right = Point(x+self.n_cell_width* self.n_edge_length_scale,y+self.n_cell_width* self.n_edge_length_scale)
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
    for junction in self.l_junctions:
      lf_center_coords = junction.get_center_coords()
      ln_cell_index = self.coords_to_index(lf_center_coords)
      self.ll_cells[ln_cell_index[0]][ln_cell_index[1]].activate()
    # end for
  
  def disable_unused_cells_old(self):
    # We will use the .net.xml file again since it contains all of
    # the edge information
    #net_xml = open(self.s_path_of_net_xml)
    #print(self.ln_grid_dimensions)
    with open(self.s_path_of_net_xml) as net_xml:
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
    #net_xml.close()

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
  
  # Creates the status window.
  def create_window(self):
     # Create the Window
    self.n_window_width = self.n_graph_padding * 2 + self.n_cell_width * self.ln_grid_dimensions[0] * self.n_edge_length_scale
    self.n_window_height = self.n_graph_padding * 2 + self.n_cell_width * self.ln_grid_dimensions[1] * self.n_edge_length_scale
    
    # Use custom resolution if requested.
    if not self.n_window_max_height or not self.n_window_max_width == 999999:
      self.n_window_height = self.n_window_max_height
      self.n_window_width = self.n_window_max_width
    
    self.window = GraphWin(self.s_window_title, self.n_window_width, self.n_window_height)
  # end def create_window(self)
  
  # Get junction information from the .net.xml file
  # We look for the <junction /> tags and we use the
  # id=, x=, and y= properties.
  #
  # We also create a point to be displayed on our status
  # window. The coordinates of the point are not the true
  # coordinates, but adjust to be in the visible area of
  # the window.
  def build_junctions(self): 
    # Make sure that our json file exists but the old version is cleared.
    
    with open(self.s_junctions_json,"w") as junctions_json:
      with open(self.s_path_of_net_xml,"r") as net_xml:
        
        junctions_json.write('{')
        is_first_line = True
        self.n_junctions = 0
        for s_line in net_xml:
          if '<junction ' in s_line and 'type="internal"' not in s_line:
            self.n_junctions += 1
            print('Locating Junction #{}'.format(self.n_junctions),end='\r')
            # id
            s_line = s_line[s_line.index('id="')+len('id="'):]
            s_id = s_line[:s_line.index('"')]
            # x coord
            s_line = s_line[s_line.index('x="')+len('x="'):]
            f_x_coord = float(s_line[:s_line.index('"')])
            # y coord
            s_line = s_line[s_line.index('y="')+len('y="'):]
            f_y_coord = float(s_line[:s_line.index('"')])
            
            # Create the center points for the junction that will
            # be used to draw the shapes to the window later.
            x = self.n_graph_padding + int(f_x_coord - self.lf_bottom_left_boundaries[0]) * self.n_edge_length_scale
            y = self.n_graph_padding + int(f_y_coord - self.lf_bottom_left_boundaries[1]) * self.n_edge_length_scale
            
            #x = self.f_boundary_width * self.n_edge_length_scale - x
            y = self.f_boundary_height * self.n_edge_length_scale - y
            
            # Put the junction information in a .json file
            # The , at the end of a json object. We choose to omit the
            # comma on the first junctions rather than the last because
            # we do not know how many junctions there will be in the
            # .net.xml
            if is_first_line:
              is_first_line = False
              junctions_json.write('\n')
            else:
              junctions_json.write(',\n')
            
            junctions_json.write('\t"' + s_id + '": {\n')
            junctions_json.write('\t\t "true_center_coords": [' + str(f_x_coord) + ',' + str(f_y_coord) + '],\n')
            junctions_json.write('\t\t "graphical_center_coords": [' + str(x) + ',' + str(y) + ']\n')
            junctions_json.write('\t}')
          # end if '<junction' in s_line
        # end for s_line in net_xml
      # end with net.xml
    # end with junctions.json
    
    with open(self.s_junctions_json,"a") as junctions_json:
      junctions_json.write('\n}')
    # end with junctions.json
  # end def build_junctions(self)
  
  # Create the edges between junctions by first finding each
  # Junction's neighbors. We can look for the <edge /> tags
  # and get Junction ids from the From= and To= properties
  def find_neighbors(self):
    # We will store our edge information in edges.json
    with open(self.s_edges_json,"w") as edges_json:
      edges_json.write('{\n')
    # Close edges.json
      
    # Look through the .net.xml file for edges
    is_first = True
    self.n_edges = 0 # Status Progress
    print()     # 
    with open(self.s_path_of_net_xml,"r") as net_xml:
      for s_line in net_xml:
        if '<edge' in s_line:
          if 'from="' in s_line:
            self.n_edges += 1
            print('Locating edge #{}'.format(self.n_edges),end='\r')
            # From
            s_line = s_line[s_line.index('from="')+len('from="'):]
            s_id_from = s_line[:s_line.index('"')]
            # To
            s_line = s_line[s_line.index('to="')+len('to="'):]
            s_id_to = s_line[:s_line.index('"')]
            #print([s_id_from,s_id_to])
            
            self.collect_edge_info(is_first,s_id_from,s_id_to)
            
            is_first = False
          # end if 'from="'
        # end if '<edge'
      # end for s_line in net_xml
      with open(self.s_edges_json,"a") as edges_json:
        edges_json.write('\n}')
      # end with edges.json
      #input("pause!")
  # end def find_neighbors
  
  # Creates edge info from junctions.json
  # - edge id
  # - true coordinates for the edge
  # - graphical coordinates for the edge
  # @param string s_id_from = The origin junction id
  # @param string s_id_to = the destination junction id
  # @param bool is_first = Is this the first edge?
  def collect_edge_info(self,is_first,s_id_from,s_id_to):
    # We must find the correct node to add neighbors to it.
    is_at_junction_from = False
    have_true_center_from = False
    have_graphical_center_from = False 
    is_complete_from = False
    is_at_junction_to = False 
    have_true_center_to = False
    have_graphical_center_to = False
    is_complete_to = False
    with open(self.s_junctions_json,"r") as junctions_json:
      for s_line_jj in junctions_json:
        if is_complete_to and is_complete_from:
          # Write the info to file
          self.combine_and_write_edge_json(is_first,s_id_to, s_id_from, s_true_coords_from, s_true_coords_to, s_graphical_coords_to, s_graphical_coords_from)
          break
        if not is_complete_to:
          # Locate the from id
          if not is_at_junction_to and s_id_to in s_line_jj:
            # Remove the extra formatting
            s_junct_id_to = s_line_jj[s_line_jj.index('"')+1:]
            s_junct_id_to = s_junct_id_to[:s_junct_id_to.index('"')]
            
            # Verfify that this is an exact match
            # Ex. 'j533' may be found in 'j5330'
            if s_id_to == s_junct_id_to:
              # The id_to is found, we can add neighbors to it.
              is_at_junction_to = True
            continue
          # end if verify id_to
          elif is_at_junction_to:
            if not have_true_center_to and '"true_center_coords":' in s_line_jj:
              s_true_coords_to = s_line_jj[s_line_jj.index('['): s_line_jj.index(']')+1]
              have_true_center_to = True 
            # end true_center_to
            elif not have_graphical_center_to and '"graphical_center_coords":' in s_line_jj:
              s_graphical_coords_to = s_line_jj[s_line_jj.index('['):s_line_jj.index(']')+1]
              have_graphical_center_to = True
            else:
              is_complete_to = True
            # end graphical center to
          # end elif is_at_junction_to
        # end if not is_complete_to
        if not is_complete_from:
          # Locate the from id
          if not is_at_junction_from and s_id_from in s_line_jj:
            # Remove the extra formatting
            s_junct_id_from = s_line_jj[s_line_jj.index('"')+1:]
            s_junct_id_from = s_junct_id_from[:s_junct_id_from.index('"')]
            
            # Verfify that this is an exact match
            # Ex. 'j533' may be found in 'j5330'
            if s_id_from == s_junct_id_from:
              # The id_from is found, we can add neighbors to it.
              is_at_junction_from = True
            continue
          # end if verify id_from
          elif is_at_junction_from:
            if not have_true_center_from and '"true_center_coords":' in s_line_jj:
              s_true_coords_from = s_line_jj[s_line_jj.index('['): s_line_jj.index(']')+1]
              have_true_center_from = True 
            # end true_center_from
            elif not have_graphical_center_from and '"graphical_center_coords":' in s_line_jj:
              s_graphical_coords_from = s_line_jj[s_line_jj.index('['):s_line_jj.index(']')+1]
              have_graphical_center_from = True
            else:
              is_complete_from = True
            # end graphical center from
          # end elif is_at_junction_from
        # end if not is_complete_from
      # end for junctions.json
    # end with junctions.json
  # end def write_edge_info_to_file
  
  # Creates a json for our edges and writes them to edges.json
  # Our json will look like:
  # "s_id_to_to_s_id_from": {
  #   "true_coords": [s_true_coords_from,s_true_coords_to],
  #   "graphical_coords": [s_graphical_coords_from,s_graphical_coords_to]
  # }
  # @param bool is_first = Is this the first edge to be written to file?
  def combine_and_write_edge_json(self,is_first, s_id_to, s_id_from, s_true_coords_from, s_true_coords_to, s_graphical_coords_to, s_graphical_coords_from):
    with open(self.s_edges_json,"a") as edges_json:
      if not is_first:
        edges_json.write(',\n')
      edges_json.write('\t"' + s_id_from + '_to_' + s_id_to + '": {\n')
      edges_json.write('\t\t"true_coords": [' + s_true_coords_from + ',' + s_true_coords_to + '],\n')
      edges_json.write('\t\t"graphical_coords": [' + s_graphical_coords_from + ',' + s_graphical_coords_to + ']\n')
      edges_json.write('\t}')
    # end with open edges.json
  # end def combine_and_write_edge_json
  
  def draw_junctions(self):
    n_rad = 2
    
    # Our junction information is stored in junctions.json, so we read
    # through it to find the center points.
    n_junctions = 0
    with open(self.s_junctions_json,"r") as junctions_json:
      for s_line in junctions_json:
      
        # Locate the coords of the center circles
        if '"graphical_center_coords":' in s_line:
          # Print progress to command line
          n_junctions += 1
          print('Drawing Junction #{} / '.format(n_junctions) + str(self.n_junctions),end='\r')
          
          # Extract the center coordinates
          # 'xx.xxxx,yy.yyyy'
          s_center_coords = s_line[s_line.index('[')+1:s_line.index(']')]
          # ['xx.xxxx','yy.yyyy']
          ls_center_coords = s_center_coords.split(',')
          # If the number has many points past the decimol we must first
          # cast to float then to int to reduce errors
          # xx
          n_center_x = int(float(ls_center_coords[0]))
          # yy
          n_center_y = int(float(ls_center_coords[1]))
          # Point(x,y)
          p_center = Point(n_center_x,n_center_y)
          circle = Circle(p_center,n_rad)
          circle.draw(self.window)
          
        # end if grahical_center_coords
      # end for s_line in edges_json
    # end with open juncts.json
    
    # After we plot our points we can the plot our edges.
    n_edges = 0
    print()
    with open(self.s_edges_json,'r') as edges_json:
      for s_line in edges_json:
        if '"graphical_coords":' in s_line:
          # Print progress to command line
          n_edges += 1
          print('Drawing edge #{} / '.format(n_edges) + str(self.n_edges),end='\r')
          
          # 'x1.x1,y1.y1],[x2.x2,y2.y2'
          s_coords = s_line[s_line.index('[[')+2:s_line.index(']]')]
          
          # 'x1.x1,y1.y1'
          s_coords_from = s_coords[:s_coords.index(']')]
          # ['xx.xx','yy.yy']
          ls_coords_from = s_coords_from.split(',')
          #
          n_from_x = int(float(ls_coords_from[0]))
          n_from_y = int(float(ls_coords_from[1]))
          p_from = Point(n_from_x,n_from_y)
          
          #'x2.x2,y2.y2'
          s_coords_to = s_coords[s_coords.index('[')+1:]
          # ['xx.xx','yy.yy']
          ls_coords_to = s_coords_to.split(',')
          #
          n_to_x = int(float(ls_coords_to[0]))
          n_to_y = int(float(ls_coords_to[1]))
          p_to = Point(n_to_x,n_to_y)
          
          # Draw line from point to point.
          line = Line(p_from,p_to)
          line.setArrow("last")
          line.draw(self.window)
        # end if '"graphical_coords":' in s_line:
      # end for line
    # end with open edges.json
    #
    for junction in self.l_junctions:
      p_center = junction.get_center_point()
      circle = Circle(p_center,n_rad)
      circle.draw(self.window)
      
      # Create one edge to every neighbor
      ll_sn_neighbors = junction.get_neighbors()
      if len(ll_sn_neighbors) > 0:
        for lsn_neighbor in ll_sn_neighbors:
          s_neighbor_id = lsn_neighbor[0]
          n_neighbor_index = lsn_neighbor[1]
          p_neighbor_center = self.l_junctions[n_neighbor_index].get_center_point()
          
          # Draw a line from this junction to its neighbor.
          line = Line(p_center,p_neighbor_center)
          line.setArrow("last")
          line.draw(self.window)
        # end for neighbors
      # end if len
    # end for junction in l_junctions
    
  # end def draw_junctions
  
  # Scrolls though the window by adjusting the visible objects 
  # on the screen.
  def setCoords(self,x1,y1,x2,y2):
    self.window.setCoords(x1,y1,x2,y2)
  # End setCoords
# End class StatusWinow
