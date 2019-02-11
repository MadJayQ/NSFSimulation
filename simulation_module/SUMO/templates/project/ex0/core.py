# Add imports here
import config # ./config.py


###############################
# Add element(s) to routefiles
#
# @return string = The elements that will be added to the
# routefile.
###############################
def generate_elements():
    
    return ''
# End def generate_elements()


###############################
# Initilize anything that needs to happen at step 0 here.
###############################
def initialize(traci):
    
    return
# end def intialize


###############################
# Anything that happens within the TraCI control loop goes here.
# One pass of the loop == 1 timestep.
###############################
def timestep(traci,n_step):

    return
# end timestep

###############################
# A quick pause
###############################
def pause():
    input("Press return to continue...")
# end def pause()
