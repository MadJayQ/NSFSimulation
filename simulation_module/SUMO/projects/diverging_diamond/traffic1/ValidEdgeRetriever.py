# ValidEdgeRetriever.py
#
# Author: Quentin Goss
# Last Modified: 9/21/18
#
# Parses through the .net.xml file to retrieve drivable edges.

class ValidEdgeRetriever:
  # @param netFile = path of the .net.xml file
  def __init__(self, netFile):
    self.netFile = netFile
  
    # Every vehicle class in sumo. [vClass,isAllowed]
    self.vClassAllowed = [['pedestrian',False],['bicycle',False],['moped',False],['motorcycle',False],['passenger',False],['emergency',False],['delivery',False],['truck',False],['trailer',False],['bus',False],['tram',False],['rail_urban',False],['rail',False],['rail_electric',False],['evehicle',False],['ship',False],['private',False],['authority',False],['army',False],['vip',False],['hov',False],['coach',False],['taxi',False],['custom1',False],['custom2',False]]
    
    self.skipCheck = False
    return
  
  def __del__(self):
    del self.vClassAllowed
    return
    
  def setSkipCheck(self,flag):
    self.skipCheck = flag
    return
    
  # Retrieve the entire vClassAllowed list.
  def get_vClassAllowed(self):
    return self.vClassAllowed
    
  # set a vClass to be allowed or disallowed.
  #
  # @param l_vClass = A list of vClass to be modified. ex.
  #                   ['pedestrian','authority','bus']
  #                   Mispelled vClass will be skipped.
  # @param flag = Allow ? True : False
  def vClassAllow(self,l_vClass,flag):
    for col in range(len(self.vClassAllowed)):
      for vClass in l_vClass:
        if vClass in self.vClassAllowed[col]:
          self.vClassAllowed[col][1] = flag    
      
  # Set all vClass to be allowed or disallowed.
  #
  # @param flag = Allow ? True : False
  def vClassAllowAll(self,flag):
    for vClass in self.vClassAllowed:
      vClass[1] = flag
    print(self.vClassAllowed)
  
  # Compile a list of valid edges with the rules set in vClassAllowed
  # 
  # @return = a list of valid edge ids
  def findValidEdges(self):
    validEdges = []  
    atEdge = False
    edgeID = ''
    laneID = ''
    # We look through the .net.xml file to find valid edges
    with open(self.netFile,'r') as nf:
      for line in nf:
        # we've found a valid edge
        if not atEdge and '<edge id="' in line and 'priority="' in line:
          line = line[line.index('id="')+len('id="'):]
          edgeID = line[:line.index('"')]
          atEdge = True
          
          if self.skipCheck:
            validEdges.append(edgeID)
            atEdge = False
            
          continue
        # We check the to see if a type is dissallowed.
        
        elif atEdge and 'lane id="' in line and 'disallow="' in line:
          # Take the disallowed vClass and put it into a list
          line = line[line.index('disallow="')+len('disallow="'):]
          disallow = line[:line.index('"')]
          disallow = disallow.split(' ')
          
          # Compare the allowed list with disallow
          isValidLane = True
          for vClass in self.vClassAllowed:
            # if one of the allowed is found in disallow this is not an
            # edge we can use
            if vClass[1] and vClass[0] in disallow:
              isValidLane = False
              break
          # if the loop completes and none are found to be disallowed,
          # then this is a good lane.
          if isValidLane:
            validEdges.append(edgeID)
            atEdge = False
          

        # We are no longer at the right edge
        else:
          atEdge = False
          continue
      # end for
    # end open
    return validEdges
          
# end class RetrieveEdges
