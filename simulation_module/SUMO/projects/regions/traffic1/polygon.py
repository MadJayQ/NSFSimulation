# polygon.py
# Author: Quentin Goss
# Last Modified: 12/17/18
#
# This module has many methods improving the functionality of polygons in SUMO.

def main():
    s_poly_xml = '../data/regions.poly.xml'
    
    # Retrieve a list of polygons from a file
    l_poly = file2obj(s_poly_xml)
    print('Untrimmed: ' + str(len(l_poly)))
    
    # Remove the buildings (The rest are zones).
    # We identify buildings from the color [130,130,130] (grey)
    l_poly = lpolytrim(l_poly,color=[130,130,130])
    print('  Trimmed: ' + str(len(l_poly)))
    
    # Show directions
    msg =  '+---- Direction Key ---+\n'
    msg += '|    up down left right|\n'
    msg += '|bit: 1   2    4     8 |\n'
    msg += '+----------------------+'
    print(msg)
    ccsplit(l_poly[0])
# end def main

# Splits up a shape into 1 or more concave subshapes
#
# @param poly = Polygon to be split
def ccsplit(poly):
    shape_coords = []
    shape_dir = []
    n_vertices = len(poly.shape)
    for n in range(n_vertices):
        # With the current vertex and the following vertex we 
        # may determine the direction the shape is moving.
        
        # Coords for Vertices 0 and 1 (w/ wrap around)
        xy0 = poly.shape[n]
        xy1 = poly.shape[(n+1)%n_vertices]
        
        # Add xy0 to coordinates
        shape_coords.append(xy0)
        
        # Find the direction the edge moves
        direct = calcdir(xy0,xy1)
        
        # Add the direction to the list of directions
        shape_dir.append(direct)
        
        # Direction between 
        print([xy0,xy1,direct])
# end def ccsplit

# Determines the direction of a line originating at xy0 and ending at xy1
#           x      y
# @param [float, float] xy0, xy1 
# @return 0-15, a bitwise result
#              up down left right
#        bit:   1   2    4     8
def calcdir(xy0,xy1):
    direct = 0
    # up
    if xy0[1] < xy1[1]:
        direct = direct | 1
    # right
    if xy0[0] < xy1[0]:
        direct = direct | 8 
    # down
    if xy0[1] > xy1[1]:
        direct = direct | 2
    # left
    if xy0[0] > xy1[0]:
        direct = direct | 4
    return(direct)
    
# end calcdir

# Trims a list of poly objects if a parameter is met
#
# @param l_poly = List of Polygon objects to be trimmed
# @param _id,color,fill,layer,shape = Optional Parameters to be checked
#   By default, incomplete polygons are trimmed.
# @return l_poly = a trimmed list of Polygon objects
def lpolytrim(l_poly,_id=None,color=None,fill=None,layer=None,shape=None):
    for poly in l_poly:
        if poly._id == _id or poly.color == color or poly.fill == fill or poly.layer == layer or poly.shape == shape:
            l_poly.remove(poly)
    return(l_poly)
# end def lpolytrim

# Converts a SUMO poly xml file into a list of polygon objects
#
# @param s_filename = Path to xml file
# @return l_poly = List of polygon objects 
def file2obj(s_filepath):
    l_poly = []
    with open(s_filepath,'r') as xml:
        for s_line in xml:
            if '<poly id=' in s_line:
                l_poly.append(xml2obj(s_line))
    return l_poly
# end file2obj

# Converts a SUMO poly xml string into a python object
#
# @param s_xml = polygon as an XML string
# @return poly = polygon object
def xml2obj(s_xml):
    if not '<poly' in s_xml:
        raise Exception('Not a polygon object.\n' + s_xml)
    # ID
    s_id = s_xml[s_xml.index('id="')+len('id="'):s_xml.index('" ')]
    _id = s_id
    del s_id
    #print(s_id)
    
    # Color
    s_xml = s_xml[s_xml.index('" ')+len('" '):]
    s_color = s_xml[s_xml.index('color="')+len('color="'):s_xml.index('" ')]
    #print(s_color)
    # The color is either a color name or list of values
    if s_color.isalpha():
        color = s_color
    else:
        ls_color = s_color.split(',')
        ln_color = []
        for item in ls_color:
            ln_color.append(int(item))
        color = ln_color
        del ls_color
        del ln_color
    del s_color

    # Fill
    s_xml = s_xml[s_xml.index('" ')+len('" '):]
    s_fill = s_xml[s_xml.index('fill="')+len('fill="'):s_xml.index('" ')]
    fill = bool(int(s_fill))
    del s_fill
    #print(fill)

    # Layer
    s_xml = s_xml[s_xml.index('" ')+len('" '):]
    s_layer = s_xml[s_xml.index('layer="')+len('layer="'):s_xml.index('" ')]
    layer = float(s_layer)
    del s_layer
    #print(layer)
    
    # Shape
    s_xml = s_xml[s_xml.index('" ')+len('" '):]
    s_shape = s_xml[s_xml.index('shape="')+len('shape="'):s_xml.index('"/>')]
    ls_shape = s_shape.split(' ')
    lls_shape = []
    for item in ls_shape:
        lls_shape.append(item.split(','))
    lln_shape = []
    for item in lls_shape:
        lln_shape.append([float(item[0]),float(item[1])])
    shape = lln_shape
    del s_shape
    del ls_shape
    del lls_shape
    del lln_shape
    #print(lln_shape)
    
    del s_xml
    return(Polygon(_id,color,fill,layer,shape))
# end xml2obj

# polygon object
class Polygon:
    # @param string _id
    # @param [int,int,int] | string color
    # @param bool fill
    # @param float layer
    # @param [float,...,float] shape
    def __init__(self,_id,color,fill,layer,shape):
        self._id = _id
        self.color = color
        self.fill = fill
        self.layer = layer
        self.shape = shape
# End polygon object

main()
