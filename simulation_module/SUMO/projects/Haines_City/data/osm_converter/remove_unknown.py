# remove_unknown.py
# Author: Quentin Goss
# Last Modified: 9/20/18
#
# Cleans type="unknown" polygons from a .typ.xml file
#
# Usage (debian): 
#   python3 remove_unknown.py --poly_xml=POLY_XML
def main():
  options = get_options()
  s_poly_xml = options.poly_xml
  s_temp = "./temp.poly.xml"

  # First write over each line that isn't an unknown to the temp file.
  n_lines = 0
  with open(s_poly_xml,'r') as poly_xml:
    with open(s_temp,'w') as temp:
      for s_line in poly_xml:
        n_lines += 1
        print('Reading line [%d] in %s' % (n_lines,s_poly_xml),end='\r')
        if 'type="unknown"' in s_line:
          continue
        else:
          temp.write(s_line)

  # Then write it back to the original.
  print()
  n = 0
  with open(s_temp,'r') as temp:
    with open(s_poly_xml,'w') as poly_xml:
      for s_line in temp:
        n += 1
        print('Copying over line [%d].' % (n),end='\r')
        poly_xml.write(s_line)
        
  # ending stats
  f_pruned = 100.0 - (float(n) / float(n_lines))*100
  n_pruned = n_lines - n
  print('\npruned %5.2f%% and %d type="unknown"s.' % (f_pruned,   n_pruned),end='\n')
# end def main

def get_options():
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--poly_xml', help='Path of the POLY_XML file', action='store', type='string', dest='poly_xml', default='None')
  (options, args) = parser.parse_args()
  
  if options.poly_xml == 'None':
    raise Exception('.poly.xml not declared. Please point to the .poly.xml using --poly_xml=POLY_XML.')
  elif options.poly_xml[0-len('.poly.xml'):] != '.poly.xml':
    print('<!> WARNING <!> Unconventional file extension %s.' % (options.poly_xml))
  
  return options
# end def get_options


main()



