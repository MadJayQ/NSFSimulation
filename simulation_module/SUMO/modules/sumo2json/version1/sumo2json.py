# Author: Quentin Goss
# Last Modified: 9/12/2018
# Converts select sumo .net.xml data into .json format.

def main():
  
  options = get_options()
  print('Using .net.xml >> \'{}\''.format(options.net_xml))
  
  convert_junctions(options.net_xml)
  convert_edges(options.net_xml)
# end test

# Get options from optparse
# @return options - Flag options
def get_options():
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--net_xml', help='Path of the NET_XML file', action='store', type='string', dest='net_xml', default='None')
  (options, args) = parser.parse_args()
  
  if options.net_xml == 'None':
    raise Exception('.net.xml not declared. Please point to the .net.xml using --net_xml NET_XML.')
  elif options.net_xml[0-len('.net.xml'):] != '.net.xml':
    raise Exception('Incorrect .net.xml file extension >> \'{}\'. Must end in .net.xml!' .format(options.net_xml))
  
  return options

# end def get_options()

# Get the boundaries from the .net.xml
#
# @param string s_net_xml = The path to the .net.xml
# @return float lf_boundaries = [ [btm_lft.x, btm_lft.y],
#                                 [btm_rgt.x, btm_rgt.y] ]
def get_boundaries(s_net_xml):
  with open(s_net_xml,'r') as net_xml:
    for s_line in net_xml:
      # "convBoundary" is an auto-generated boundary for everything
      # important in our map, so it's a good start for deciding
      # what the outer limits of our map should be.
      if "convBoundary" in s_line:
        s_line = s_line[s_line.index('convBoundary="')+len('convBoundary="'):-1]
        s_line = s_line[0:s_line.index('"')]
        ls_boundaries = s_line.split(',')
        lf_boundaries = [[float(ls_boundaries[0]),float(ls_boundaries[1])],[float(ls_boundaries[2]),float(ls_boundaries[3])]]
        break
  # end with open(s_net_xml,'r') as net_xml:
  return lf_boundaries
# end def get_boundaries():

# Converts sumo junctions within the .net.xml to junctions.json
#
# @param string s_net_xml = The path to the .net.xml
# @param float lf_boundaries = boundaries 
def convert_junctions(s_net_xml): 
  s_junctions_json = "junctions.json"
  
  # We must get boundaries before we open .net.xml
  lf_boundaries = get_boundaries(s_net_xml)
  # We'll use the width and heigh to normalize values later
  f_width = lf_boundaries[1][0] - lf_boundaries[0][0]
  f_height = lf_boundaries[1][1] - lf_boundaries[0][1]
  
  # Make sure that our json file exists but the old version is cleared.
  
  with open(s_junctions_json,"w") as junctions_json:
    with open(s_net_xml,"r") as net_xml:
      
      junctions_json.write('{')
      is_first_line = True
      n_junctions = 0
      for s_line in net_xml:
        if '<junction ' in s_line and 'type="internal"' not in s_line:
          n_junctions += 1
          print('Locating Junction [{}]'.format(n_junctions),end='\r')
          
          # id
          s_line = s_line[s_line.index('id="')+len('id="'):]
          s_id = s_line[:s_line.index('"')]
          
          # True Coordinates
          # x coord
          s_line = s_line[s_line.index('x="')+len('x="'):]
          f_x_coord = float(s_line[:s_line.index('"')])
          # y coord
          s_line = s_line[s_line.index('y="')+len('y="'):]
          f_y_coord = float(s_line[:s_line.index('"')])

          # Normalized coordinates
          f_normal_x = (f_x_coord - lf_boundaries[0][0]) / f_width
          f_normal_y = (f_y_coord - lf_boundaries[0][1]) / f_height
          
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
          junctions_json.write('\t\t "normal_center_coords": [' + str(f_normal_x) + ',' + str(f_normal_y) + ']\n')
          junctions_json.write('\t}')
        # end if '<junction' in s_line
      # end for s_line in net_xml
    # end with net.xml
  # end with junctions.json
  
  with open(s_junctions_json,"a") as junctions_json:
    junctions_json.write('\n}')
  # end with junctions.json
  
  print()
# end def convert_junctions()

# Create the edges between junctions by first finding each
# Junction's neighbors. We can look for the <edge /> tags
# and get Junction ids from the From= and To= properties
#
# @param string s_net_xml = The path to the .net.xml
def convert_edges(s_net_xml):
  s_edges_json = "edges.json"

  # We will store our edge information in edges.json
  with open(s_edges_json,"w") as edges_json:
    edges_json.write('{\n')
  # Close edges.json
    
  # Look through the .net.xml file for edges
  is_first = True
  n_edges = 0 # Status Progress
  with open(s_net_xml,"r") as net_xml:
    for s_line in net_xml:
      if '<edge' in s_line:
        if 'from="' in s_line:
          n_edges += 1
          print('Locating Edge [{}]'.format(n_edges),end='\r')
          # From
          s_line = s_line[s_line.index('from="')+len('from="'):]
          s_id_from = s_line[:s_line.index('"')]
          # To
          s_line = s_line[s_line.index('to="')+len('to="'):]
          s_id_to = s_line[:s_line.index('"')]
          
          collect_edge_info(is_first,s_id_from,s_id_to)
          
          is_first = False
        # end if 'from="'
      # end if '<edge'
    # end for s_line in net_xml
    with open(s_edges_json,"a") as edges_json:
      edges_json.write('\n}')
    # end with edges.json
    
    print()
# end def convert_edges

# Creates edge info from junctions.json
# - edge id
# - true coordinates for the edge
# - graphical coordinates for the edge
# @param string s_id_from = The origin junction id
# @param string s_id_to = the destination junction id
# @param bool is_first = Is this the first edge?
def collect_edge_info(is_first,s_id_from,s_id_to):
  s_junctions_json = "junctions.json"

  # We must find the correct node to add neighbors to it.
  is_at_junction_from = False
  have_true_center_from = False
  have_normal_center_from = False 
  is_complete_from = False
  is_at_junction_to = False 
  have_true_center_to = False
  have_normal_center_to = False
  is_complete_to = False
  with open(s_junctions_json,"r") as junctions_json:
    for s_line_jj in junctions_json:
      if is_complete_to and is_complete_from:
        # Write the info to file
        combine_and_write_edge_json(is_first,s_id_to, s_id_from, s_true_coords_from, s_true_coords_to, s_normal_coords_to, s_normal_coords_from)
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
          elif not have_normal_center_to and '"normal_center_coords":' in s_line_jj:
            s_normal_coords_to = s_line_jj[s_line_jj.index('['):s_line_jj.index(']')+1]
            have_normal_center_to = True
          else:
            is_complete_to = True
          # end normal center to
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
          elif not have_normal_center_from and '"normal_center_coords":' in s_line_jj:
            s_normal_coords_from = s_line_jj[s_line_jj.index('['):s_line_jj.index(']')+1]
            have_normal_center_from = True
          else:
            is_complete_from = True
          # end normal center from
        # end elif is_at_junction_from
      # end if not is_complete_from
    # end for junctions.json
  # end with junctions.json
# end def write_edge_info_to_file

 # Creates a json for our edges and writes them to edges.json
# "s_id_to_to_s_id_from": {
#   "true_coords": [s_true_coords_from,s_true_coords_to],
#   "normal_coords": [s_normal_coords_from,s_normal_coords_to]
# }
# @param bool is_first = Is this the first edge to be written to file?
def combine_and_write_edge_json(is_first, s_id_to, s_id_from, s_true_coords_from, s_true_coords_to, s_normal_coords_to, s_normal_coords_from):
  s_edges_json = "edges.json"
  with open(s_edges_json,"a") as edges_json:
    if not is_first:
      edges_json.write(',\n')
    edges_json.write('\t"' + s_id_from + '_to_' + s_id_to + '": {\n')
    edges_json.write('\t\t"true_coords": [' + s_true_coords_from + ',' + s_true_coords_to + '],\n')
    edges_json.write('\t\t"normal_coords": [' + s_normal_coords_from + ',' + s_normal_coords_to + ']\n')
    edges_json.write('\t}')
  # end with open edges.json
# end def combine_and_write_edge_json

main()
