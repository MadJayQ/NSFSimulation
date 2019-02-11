# sumo2csv.py
# Author: Quentin Goss
# Last Modified: 10/29/18
#
# Creates two comma seperated value (CSV) files from a .net.xml file.
#  1. edges.csv
#  2. junctions.csv

s_net_xml = 'C:/flpoly/fall18/add/Wyandotte MI/data/Wyandotte.MI.net.xml'
s_edges_csv = 'Wyandotte.MI.edges.csv'
s_junctions_csv = 'Wyandotte.MI.junctions.csv'

with open(s_edges_csv, 'w') as edges_csv:
    edges_csv.write('EDGE_ID,FROM_ID,TO_ID,NAME,PRIORITY,TYPE\n')
# end width edges.csv

with open(s_junctions_csv, 'w') as junctions_csv:
    junctions_csv.write('JUNCT_ID,X,Y,TYPE\n')
# end with junctions.csv

with open(s_net_xml, 'r') as net_xml:
    with open(s_edges_csv, 'a') as edges_csv:
        with open (s_junctions_csv, 'a') as junctions_csv: 
            for s_line in net_xml:

                # Edge parsing
                if '<edge' in s_line and not 'function="internal"' in s_line:
                    s_edge_id = s_from_id = s_to_id = s_name = s_priority = s_type = ''

                    # edge id
                    if 'id="' in s_line:
                        s_edge_id = s_line[s_line.index('id="')+len('id="'):]
                        s_edge_id = s_edge_id[:s_edge_id.index('"')]
                                              
                    # from id
                    if 'from="' in s_line:
                        s_from_id = s_line[s_line.index('from="')+len('from="'):]
                        s_from_id = s_from_id[:s_from_id.index('"')]

                    # to id
                    if 'to="' in s_line:
                        s_to_id = s_line[s_line.index('to="')+len('to="'):]
                        s_to_id = s_to_id[:s_to_id.index('"')]

                    # name
                    if 'name="' in s_line:
                        s_name = s_line[s_line.index('name="')+len('name="'):]
                        s_name = s_name[:s_name.index('"')]

                    # priority
                    if 'priority="' in s_line:
                        s_priority = s_line[s_line.index('priority="')+len('priority="'):]
                        s_priority = s_priority[:s_priority.index('"')]

                    # type
                    if 'type="' in s_line:
                        s_type = s_line[s_line.index('type="')+len('type="'):]
                        s_type = s_type[:s_type.index('"')]

                    # Write to edges.csv
                    s_data = s_edge_id + ',' + s_from_id + ',' + s_to_id + ',' + s_name + ',' + s_priority + ',' + s_type + '\n'
                    edges_csv.write(s_data)

                    del s_data
                    del s_edge_id
                    del s_from_id
                    del s_to_id
                    del s_name
                    del s_priority
                    del s_type
    
                # end Edge parsing
                    
                # Junction parsing
                if '<junction' in s_line and not 'type="internal"' in s_line:
                    s_junct_id = x = y = s_type = ''
                    
                    if 'id="' in s_line:
                        s_junct_id = s_line[s_line.index('id="')+len('id="'):]
                        s_junct_id = s_junct_id[:s_junct_id.index('"')]
                        
                    if 'x="' in s_line:
                        x = s_line[s_line.index('x="')+len('x="'):]
                        x = x[:x.index('"')]
                        
                    if 'y="' in s_line:
                        y = s_line[s_line.index('y="')+len('y="'):]
                        y = y[:y.index('"')]
                        
                    if 'type="' in s_line:
                        s_type = s_line[s_line.index('type="')+len('type="'):]
                        s_type = s_type[:s_type.index('"')]

                    # write to junctions.csv
                    s_data = s_junct_id + ',' + x + ',' + y + ',' + s_type + '\n'
                    junctions_csv.write(s_data)
                    
                    del s_data
                    del s_junct_id
                    del x
                    del y
                    del s_type
                # End junction parsing
                
            # end for line in net.xml
        # end with junctions.csv
    # end with edges.csv
# end with net.xml

