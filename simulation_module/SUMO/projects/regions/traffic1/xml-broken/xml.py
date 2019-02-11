# xml.py
# Author: Quentin Goss
# Last Modified: 12/18/18
#
# Handles various XML operations

import warnings

# Try 3
def parse(xml):
    for n in xml:
        n = next(xml[n] == '<',n)
    # end for
# end parse

# Continue condition
#
# @param condition -> Conidtion which must be true to continue
# @param n -> current character
def next(condition,n):
    if condition: return(n+1)
# end def next

# Tag loop xml
#
# @param n -> char index
# @param xml -> xml string
def tag(n,xml):
    
# end def tag

# Try #2!
def parse_old_2(s_xml):
	s_prev_char = ' '
    s_valid_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz:_'
	# Tags start with < and end with /
	for n in len(s_xml):
        char = s_xml[n]
        
        # Tag begin
        if char == '<':
            # next char
            n += 1
            char = s_xml[n]
            
            # Header Begin
            if char == '?':
                # are the next 3 chars 'xml' in order?
                if s_xml[n+1] == 'x' and s_xml[n+2] == 'm' and s_xml[n+3] == 'l':
                    # next char
                    n += 4
                    char = s_xml[n]
                    
                    # close Header if '?>'
                    if char == '?' and s_xml[n+1] == '>':
                        n += 1
                        continue
                    prop_begin = False  
                      
                    # Space
                    if char == ' ':
                        prop_begin = True
                    # \t \n
                    if char == '\\':
                        n += 1
                        char = s_xml[n]
                        if char == 't' or char == 'n':
                            prop_begin = True
                    
                    # Property Begin
                    if prop_begin:
                        # Additional spaces and tabs
                        while char == ' ' or char == '\\':
                            n += 1
                            if char == '\\' and (s_xml[n] == 't' or s_xml[n] == 'n'):
                                n += 1
                            char = s_xml[n]
                        # end while
                        
                        # close Header if '?>'
                        if char == '?' and s_xml[n+1] == '>':
                            n += 1
                            continue
                        
                        # Property Name
                        elif char in s_valid_chars:
                            s_prop_name = char
                            
                            # Loop through properties
                            more_prop = True
                            while more_prop:
                                n += 1
                                char = s_xml[n]
                                 
                                # Property Name continues 
                                while char in s_valid_chars:
                                     n += 1
                                     char = s_xml[n]
                                     s_prop_name += char
                                
                                # Property name ends     
                                if char == '=' and s_xml[n+1] == '"':
                                    n += 2
                                    char = s_xml[n]
                                    
                                    while not char == '"':
                                        break
                    # end if Property Begin
                # end if xml
            # end if Header Begin
        # end if Tag begin
		continue
	return
# end def parse

# Pa
rses XML and returns a parsed XML object
#
# @param s_xml = XML string to be parsed
def parse_old(s_xml):
    ln = 0
    s_valid_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz:_'
    ls_tokens = []
    s_token = ''
    s_header_contents = ''
    is_comment = False
    is_header = False
    for char in s_xml:
        ln += 1
        s_token += char
        ##################
        ### Tag Checks ###
        ##################

        ##########
        # Header #
        ##########
        if s_token == '<?xml':
            is_header = True
            s_token = ''
            continue
        elif is_header and len(s_token) > 1 and s_token[-2:] == '?>':
            is_header = False
            ls_props = parse_props(s_token[1:-2])
            ls_tokens.append(['xml',ls_props])
            print(ls_tokens)
            s_token = ''
            continue

        ###########
        # Comment #
        ###########
        elif '<!--' in s_token:
            is_comment = True
            s_token = ''
            continue
        elif is_comment and len(s_token) > 2 and s_token[-3:] == '-->':
            is_comment = False
            s_token = ''
            continue

        #################################
        ### Intermediate Mode Handles ###
        #################################

        ###################
        # Handle Comments #
        ###################
        if is_comment:
            s_token = ''
            continue

        #################
        # Handle Header #
        #################
        elif is_header:
            continue

        elif (str('<' + char) in s_token):
            print(s_token)
    return
# End def parse

# Parses properties in an XML object
#
# @param s_props = The inside of an XML object with no trailing or ending spaces
def parse_props(s_props):
    s_token = ''
    ls_props = []
    s_name = ''
    is_prop = False
    for char in s_props:
        s_token += char
        # Start of token
        if len(s_token) > 1 and s_token[-2:] == '="':
            s_name = s_token[:-2].strip(' ')
            is_prop = True
            s_token = ''
            continue
        # End of token
        elif char == '"' and len(s_token) > 1 and not s_token[-2:] == '\"':
            ls_props.append([s_name,s_token[:-1]])
            is_prop = False
            s_token = ''
            s_name = ''
            continue
        
        if is_prop:
            continue
    # end for
    return(ls_props)

# Retrieves an XML string from file.
#
# @param s_fname = Name of XML file
# @return s_xml = Contents of the XML file as a string.
def sff(s_fname): # Shortened
    return(string_from_file(s_fname))
def string_from_file(s_fname):
    s_xml = ''
    with open(s_fname, 'r') as file:
        for s_line in file:
            s_xml += s_line
        # end for
    # end with
    return(s_xml)
# end def string_from_file

def test():
    s_xml = sff('../data/regions.poly.xml')
    parse(s_xml)
# end def test

test()
