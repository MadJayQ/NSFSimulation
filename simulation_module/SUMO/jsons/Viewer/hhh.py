# Author: Quentin Goss
# Last Modified: 10/17/18
# Purpose: Opens a directed graph file to view.
from graphics import *

def main():
  options = get_options()
  
  # Initialize
  project_path = options.proj_dir
  junctions_json = project_path + "junctions.json"
  edges_json = project_path + "edges.json" 

  # Global declarations
  global BORDER
  global VERBOSE
  global WA_WIDTH
  global WA_HEIGHT
  
  # Options
  title = "Map"
  win_width = options.width
  win_height = options.height
  BORDER = options.border
  VERBOSE = options.verbose
  
  # Working Area Size
  WA_WIDTH = win_width - 2 * BORDER
  WA_HEIGHT = win_height - 2 * BORDER
  
  win = GraphWin(title,win_width,win_height)
  
  # Run
  win = place_junctions(win, junctions_json, node_size=options.node_rad, toggle_node_numbers=options.node_num)
  win = place_edges(win, edges_json)  
  
  # Finalize
  try:
    while True:
      win.getMouse()
  except:
    win.close
# End def main

# Places junctions
#
# @param GraphWin win = graphics window object
# @param String junctions_json = name of the json file that stores
#        junction info
# @param int node_size = The radius node circles
# @param bool toggle_node_numbers = Show node numbers
# @return GraphWin = graphics window object
#
# Reads in junctions from a json file and plots to the window
def place_junctions(win, junctions_json, node_size=2, toggle_node_numbers=False):
  num_nodes = 0
  with open(junctions_json,'r') as jj:
    for line in jj:
      if "normal_center_coords" in line:
        if VERBOSE: print('Placing Node [%d]' % (num_nodes),end='\r')
        
        # Extract the coordinates from the json file
        line = line[line.index('[')+1:line.index(']')]
        line = line.split(',')
        coords = [float(line[0]),float(line[1])]
        
        # Create a node
        x = int(coords[0] * WA_WIDTH) + BORDER
        y = int(coords[1] * -WA_HEIGHT) + WA_HEIGHT + BORDER 
        
        center = Point(x,y)
        node = Circle(center,node_size)
        node.draw(win)
        
        if toggle_node_numbers:
          y -= node_size + 5
          center = Point(x,y)
          text = Text(center,str(num_nodes))
          text.draw(win)
        
        num_nodes += 1
      # end if
    # end for
  # End open junctions_json
  if VERBOSE: print()
  return(win)
# end def place_junctions

# Place edges
# 
# @param GraphWin win = graphics window object
# @param String edges_json = name of the json file that stores
#        edge info
# @param Bool toggle_node_snap = Adjust to end 
# @return GraphWin = graphics window object
#
# Reads in edges from a json file and plots to the window
def place_edges(win, edges_json):
  num_edges = 0
  with open(edges_json,'r') as ej:
    for line in ej:
      if "normal_coords" in line:
        if VERBOSE: print('Placing Edge [%d]' % (num_edges),end='\r')
          
        begin = line[line.index('[[')+2:line.index(']')].split(',')
        end = line[line.index('],[')+3:line.index(']]')].split(',')
        coords = [[float(begin[0]),float(begin[1])],[float(end[0]),float(end[1])]]
        
        # Find the center of start and end
        x = [0,0]
        y = [0,0]
        x[0] = int(coords[0][0] * WA_WIDTH) + BORDER
        y[0] = int(coords[0][1] * -WA_HEIGHT) + WA_HEIGHT + BORDER
        x[1] = int(coords[1][0] * WA_WIDTH) + BORDER
        y[1] = int(coords[1][1] * -WA_HEIGHT) + WA_HEIGHT + BORDER
        
        line = Line(Point(x[0],y[0]),Point(x[1],y[1]))
        line.setArrow("last")
        line.draw(win)
        
        num_edges += 1
      # end if  
    # end for
  # end open edges_json
  if VERBOSE: print()
  return(win)
# end def place_edges

# Get options from optparse
# @return options = Returns flag options
def get_options():
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('-p','--proj_dir',help='Path to project directory.',action='store', type='string', dest='proj_dir', default='None')
  parser.add_option('-W','--width',help='Window Width', action='store', type='int', dest='width', default=640)
  parser.add_option('-H','--height',help='Window Height', action='store', type='int', dest='height', default=480)
  parser.add_option('-b','--border',help='Size of border', action='store', type='int', dest='border', default=10)
  parser.add_option('-r','--node_rad',help='Node radius', action='store', type='int', dest='node_rad', default=2)
  parser.add_option('-n','--node_num',help='Turn on node numbering', action='store_true', dest='node_num', default=False)
  parser.add_option('-v','--verbose',help='Quiet mode off.', action='store_true', dest='verbose', default=False)
  (options, args) =  parser.parse_args()
  
  if options.proj_dir == 'None':
    raise Exception('Must specify project directory using --proj_dir=PATH.')
  elif (options.border * 2) >= options.width or (options.border * 2) >= options.height:
    raise Exception('Border is too large for WIDTH or HEIGHT.')
  elif options.proj_dir[-1:] != '/':
    raise Exception('Please include / at the end of project directory.')
  
  return options
# end def_options
main()
