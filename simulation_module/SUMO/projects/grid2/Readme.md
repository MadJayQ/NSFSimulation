# <a name="top_of_page"></a>grid2
[poi1](#poi1) , [poi2](#poi2) , [poi3](#poi3) , [reroute1](#reroute1)
>Quentin: Here we have notes about the project grid2
>
>[Projects Home](../Readme.md)

![grid2.gif](../../assets/screenshots/projects/grid2.gif)

A more ergonomic adaptation of [grid](../grid/Readme.md) that fits neatly on a 1366x768 resolution monitor. The map features a rectangular city with rectangular blocks. There is a four-lane high that goes through the center with the highest priority. The outer roads have the second highest priority and the inside streets have the lowest.

---
<!-- begin poi1 -->
## <a name="poi1"></a>poi1
[Top](#top_of_page) , [Step #1](#poi1.step1) , [Step #2](#poi1.step2) , [Step #3](#poi1.step3) , [Step #4](#poi1.step4) , [Bug Fixes](#poi1.bug_fixes)
<br/>
![grid2.poi1.gif](../../assets/screenshots/projects/grid2.poi1.gif)
<br/> The project *poi1* is the second example created on the *grid2* project.
We build off of the previous example [reroute1](#reroute1) and we utilize the *poi* class from the [poi module](../../modules/Readme.md). We have the following goals:
1. Add any number of point of interests (POIs).
2. Route vehicles to the POIs at random.
3. Increase POI value over time.
4. Decrease POI value when a vehicle arrives to the closest point near the POI.

### <a name="poi1.step1"></a>Step #1: Adding point of interests (POIs).
[poi1](#poi1)<br/>
The first step is to add the POIs to the map.
TraCI has has a module for POIs and we'll use this as a baseline for the handling or POIs.

We want to choose where our POIs will be so we'll define the x and y coordinates of any poi we want to add in *config.py*.
From left to right, each pair of coordinates represent one POI and have the IDs *poi0, poi1... poin* for up to *n* amount of POIs -- we use a list so we may define any amount of POIs from 0 to *n* POIs.
```
# File: config.py

#[x,y] coordinates of all POI.
llf_poi_coords = [[23.0,-25.0],[24.0,34.0],[95.0,33.0],[104.0,-15.0],[142.0,-45.0],[187.0,32.0]] 
```

Before we start looping through our list off coordinates to create our POIs with, we'll bring in a global variable *L_POIS* which we'll use to keep track of and manipulate POIs within the python script.
At each step of our POI creation loop, we'll add POIs to the simulation with the *traci.poi.add()* method and find the nearest edge with the *traci.simulation.convertRoad()* method.
Then we'll create a [poi object](../../modules/Readme.md) and add it to *L_POIS*.
```
global L_POIS
for lf_poi in config.llf_poi_coords:
	s_poi_id = "poi" + str(n_pois)
    
	# traci.poi.add( ID, x, y, Color, arbitrary desc., layer) 
	traci.poi.add(s_poi_id, lf_poi[0], lf_poi[1], (100,100,100,0), poiType="taco_cart",layer=0)
    
	# Finds the closest edge to an xy coordinate.
	# (edgeID, closest_edge_x, closest_edge_y)
	s_sff_road = traci.simulation.convertRoad(lf_poi[0],lf_poi[1],isGeo=False)

	# Create a POI object
	o_poi = poi.poi(s_poi_id,lf_poi[0],lf_poi[1], config.f_initial_poi_value, s_sff_road)

	# Set Decrement Amount
	# This is will be the amount the Value will decrease every POI Update
	o_poi.setDecreaseValue(config.f_poi_value_dec_amt) 

	# Add the object to the list of POIs.
	L_POIS.append(o_poi)

	n_pois += 1
# end for lf_poi in config.llf_poi_coords:
```

### <a name="poi1.step2"></a>Step #2: Route vehicles to POIs at random.
[poi1](#poi1)<br/>
The next step is to route some vehicles to the POIs at random.
To do this we add a few lines of code in the *go_downtown(n_step)* method that sends the vehicle to the edge closest to a random POI.

```
# Send it to a poi node downtown at random
global L_POIS
n_random_int = random.randint(0,len(L_POIS)-1)
s_dest_edge = L_POIS[n_random_int].getClosestEdge()[0]
traci.vehicle.changeTarget(s_veh_id,s_dest_edge)
```

### <a name="poi1.step3"></a>Step #3: Update POIs every tick.
[poi1](#poi1)<br/>
We update the POIs at a configurable tick rate (**config.n_poi_value_update_rate**).
Within the update loop, we increase each POIs value and update the color to represent the next value.
All POIs start out as grey on timestep 0 and range between red (lowest value) and green (highest value) for the remainder of the simulation.

```
if (n_step % config.n_poi_value_update_rate == 0):
	global L_POIS
	for poi in L_POIS:
		# Value increases over time
		poi.increaseValueBy(config.f_poi_value_inc_amt)
		
		# Make sure that the value can't increase over max
		if (poi.getValue() > config.f_poi_value_max):
			poi.setValue(config.f_poi_value_max)
	  
		# Update color to reflect value
		# We want low values to be blue and high values to be green
		# Colors are (red, green, blue, alpha)
		n_color_intensity = int((poi.getValue() / config.f_poi_value_max) * 255)
		if (poi.getValue() < 0):
			traci.poi.setColor(poi.getID(),(255,0,0,0))
		elif (poi.getValue() > 255):
			traci.poi.setColor(poi.getID(),(0,255,0,0))
		else:
		traci.poi.setColor(poi.getID(),(255-n_color_intensity,0+n_color_intensity,0,0))
```

### <a name="poi1.step4"></a>Step #4: Decrease POI value on hit.
[poi1](#poi1)<br/>
Finally, when a vehicle gets to it's destination POI, we call it a "hit".
Since POIs may be placed outside of the boundaries of an edge, we accept a vehicle arriving on the edge closest to the POI to be equivalent to arriving at the POI.
We add a few lines to the *handle_lls_veh_data()* method to locate and properly call a hit to the corresponding POI.

```
# Locate the POI that we arrived at. Find the POI that is 
# nearest to the edge we're on.
for poi in L_POIS:
	if (s_dest_edge == poi.getClosestEdge()[0]):    
		poi.vehicleHit(n_step,s_veh_id)
		break
```

### <a name="poi1.bug_fixes"></a>Bug Fixes
[poi1](#poi1)<br/>
In this example we fixed a bug in the *go_downtown(n_step)* method that caused vehicles to disappear after reaching their POI destination when they are flagged for rerouting twice or more.

First, we change the way that a vehicles route "memory" is stored into the *LLS_VEH_DATA* data structure.
Before we add a new item **[** vehicle id **,** destination edge ID **,** exit ID **]** we clean any deprecated routes.
```
# Add it to LLS_VEH_DATA to be tracked.
# If a record already exists remove it so we can update   
for ls_row in LLS_VEH_DATA:
	if (s_veh_id == ls_row[0]):
		LLS_VEH_DATA.remove(ls_row)
		
# Add to history.
LLS_VEH_DATA.append([s_veh_id,s_exit_edge,s_dest_edge])
```

We also added some checks when defining our exit edges. 
If a vehicle has been rerouted, there is no reason to redefine it's exit destination.
```
# Store the exit destination edge before we change it's route.
# In case the same vehicle gets rerouted, we'll make sure that
# it doesn't set it's exit edge to a non-exit
global LLS_VEH_DATA 
ls_exit_edges = ["gneE52","-gneE52","gneE50","-gneE50"]
s_edge = traci.vehicle.getRoute(s_veh_id)[-1]

# It's being rerouted for the 1st time.
if (s_edge in ls_exit_edges):
	s_exit_edge = s_edge
	
# It's being rerouted for the 2nd or more time.
else:
	for ls_row in LLS_VEH_DATA:
		if (s_veh_id == ls_row[0]):
s_exit_edge = ls_row[1]
```

<!-- end poi1 -->
---
<!-- begin poi2 -->
## <a name="poi2"></a>poi2
[Top](#top_of_page) , [Step #1](#poi2.step1) , [Step #2](#poi2.step2) , [Step #3](#poi2.step3)
<br/>
![grid2.poi2.gif](../../assets/screenshots/projects/grid2.poi2.gif)
<br/>
The project *poi2* is the third example created on the *grid2* project. 
We build off of the previous example [poi1](#poi1) and we implment the *vehicle* class from the [vehicle module](../../modules/Readme.md).
We have the following goals:
1. Replace the vehicle management structure from [poi1](#poi1) **LLS_VEH_DATA** with a list of vehicle objects known as **L_VEHICLES**.
2. Add a capacity to the vehicles. The capacity should vary with each vehicle.
3. Reduce vehicle capacity when a vehicle "hits" a poi.
4. Implement some rules for the vehicle:
	* Vehicle cannot visit the same POI twice.
	* Vehicle "goes home" when capacity is zero (0).
	* Vehicle "goes home" if it's visited every POI.
	
### <a name="poi2.step1"></a>Step #1: Choose a vehicle to reroute.
[poi2](#poi2) <br/>
Since we are utilizing vehicle objects now instead of a list with three (3) strings to track our vehicles, we have made the rerouting functions more modular by splitting the old *go_downtown()* method from [poi1](#poi1) into three seperate methods:
```
# Chooses which vehicle will be picked to go downtown. 
# It chooses from any of the (yellow) vehicles traveling
# along the four (4) lane highway.
def choose_vehicle_to_reroute(n_step):

# Interface with the list of currently tracked vehicles to
# grab an existing vehicle object or create a new vehicle
# if it doesn't already exist.
def retrieve_vehicle(s_veh_id):
return veh

# Decides which POI to send the vehicle to and also sends
# it on it's way.
def go_to_poi(veh):
```
When choosing the vehicle, we utilize the first of the method *choose_vehicle_to_reroute(n_step)*.
We only pick a vehicle here, the rerouting checks happen in *go_to_poi(veh)*.
```
###############################
# Picks a vehicle at random to reroute.
###############################
def choose_vehicle_to_reroute(n_step):
  # Every x timesteps we're going to reroute a vehicle at random to
  # some point in town.
  if (n_step % config.n_go_downtown_rate == 0 and n_step != 0):
    # Pick a vehicle at random to reroute.
    ls_veh_ids = traci.vehicle.getIDList()
    n_random_int = random.randint(0,len(ls_veh_ids)-1)
    s_veh_id = ls_veh_ids[n_random_int]
    
    # Change color to orange.
    traci.vehicle.setColor(s_veh_id,(255,0,0,0))
    
    # Create a new vehicle object
    veh = retrieve_vehicle(s_veh_id)
    
    # Route the vehicle to the first poi
    go_to_poi(veh)
# end def choose_vehicle_to_reroute:
```

### <a name="poi2.step2"></a>Step #2: Send the vehicle to a POI.
[poi2](#poi2) <br/>
Once a vehicle is chosen we can send it to a POI -- we do this using hte *go_to_poi(veh)* method.
Here we perform a quick check is a do-while loop, in each pass we pick a random POI to visit and then check if the if the vehicle has been to the POI otherwise we continue until a point is randomly chosen that hasn't been visited yet.
> Quentin: Each vehicle object tracks the POIs they've visited in a list.
> We can retrieve this list by calling *veh.get_visited_pois()*.

This method is ambiguous and works with both newly created vehicles that are being rerouted for the first time and also vehicles currently being rerouted to POIs.
```
###############################
# Go to POI
# Sends a vehicle to a POI
###############################
def go_to_poi(veh):       
  # Send it to a poi node downtown at random
  # Python has no Do While. To emulate we do:
  # while True:
  #   if fail_condition:
  #     break
  global L_POIS
  while True:
    n_random_int = random.randint(0,len(L_POIS)-1)
    s_dest_edge = L_POIS[n_random_int].getClosestEdge()[0]
    traci.vehicle.changeTarget(veh.get_id(),s_dest_edge)
    if s_dest_edge not in veh.get_visited_pois():
      break
    
  # Store the current destination edge
  veh.set_next_dest_edge_id(s_dest_edge)
  
  # Add it to L_VEHICLES to be tracked.
  global L_VEHICLES
  L_VEHICLES.append(veh)
# end deg go_to_poi()
```

### <a name="poi2.step3"></a>Step #3: Handling vehicles that have just arrived a POI.
[poi2](#poi2) <br/>
Just like we looped through **LLS_VEH_DATA** in the *handle_lls_veh_data()* method in [poi1](#poi1), we will loop through our list of vehicles **L_VEHICLES** in a method adapted from the old *handle_lls_veh_data()* method named *handle_vehicles()*.
First, we handle a "hit".
We reduce the value of the POI that was "hit" and we reduce the capacity of the vehicle.
```
# If the vehicle has arrived at it's destination
if traci.vehicle.getRoadID(veh.get_id()) == veh.get_next_dest_edge_id():     

	# Locate the POI that we arrived at. Find the POI that is 
	# nearest to the edge we're on.
	for poi in L_POIS:
		if (veh.get_next_dest_edge_id() == poi.getClosestEdge()[0]):    
		  # "Hit" the POI
		  poi.vehicleHit(n_step,veh.get_id())
		  
		  # Add the POI to list of visited POIs.
		  veh.add_visited_pois(poi.getID())
		  
		  # Reduce Capacity
		  n_amt = int(poi.getValue() * 100.0)
		  veh.increase_capacity(0-n_amt)
		  
		  # Update vehicle Color
		  update_vehicle_color(veh)
		  break
	# End for
```
Next, we check if any "go home" conditions are met.
If a "go home" condition is met, we'll send the vehicle to whichever exit edge they were traveling to before being sent to a POI.
> Quentin: Here we use a naive approach to check if a vehicle has visited every POI by comparing the length of it's visited poi history to the total amount of POIs in the map.
> This will become very inefficient with a large number of POIs.
```
	# Is the vehicle full (capacity = 0) or has it visted all the POIs?
	if (veh.get_capacity() == 0) or len(veh.get_visited_pois()) == len(L_POIS) :
		# Go home
		traci.vehicle.changeTarget( veh.get_id(), veh.get_final_dest_edge_id())

		# Change the color to blue so we can recognize accomplished cars
		traci.vehicle.setColor(veh.get_id(),(0,255,255,0))

		# remove the vehicle from the list since we no longer need to
		# track it.
		L_VEHICLES.remove(veh)
```
If no "go home" conditions are met, we reroute the vehicle.
```
	# Otherwise send it to another poi
	else:
		# Reroute vehicles to another POI
		go_to_poi(veh)	
```

<!-- end poi2 -->
---
<!-- begin poi3 -->
## <a name="poi3"></a>poi3
[Top](#top_of_page) , [Decision #1](#poi3.decision1) , [Decision #2](#poi3.decision2) , [Decision #3](#poi3.decision3) , [Minor Tweaks](#poi3.minor_tweaks)
<br/>![gri2.poi3.gif](../../assets/screenshots/projects/grid2.poi3.gif)
<br/>The project *poi3* is the fourth example created on the *grid2* project.
We build off the previous example [poi2](#poi2) and modify the POI selection during the *go_to_poi(veh)* to be more intelligent and we also make some minor tweaks.
We will decide on where to send our vehicles by the following checks in order:
1. To the POI with the most Value at the time of check.
2. To the closest POI in terms of road distance at the time of check.
3. Randomly choose to resolve any remaining conflicts.

### <a name="poi3.decision1"></a>Decision #1: Which POI has the most value?
First, we want to go to the POI with the highest value at the time of checking.
We'll add a copy of the POI object to a list of candidates called **l_poi_max** that we'll use to narrow down with the next decision.
To do this, we compare the **f_value** of our **poi** objects.
```
l_poi_max = []
# Find the POI with the most value
elif poi.getValue() >= n_max_val:
	l_poi_max.append(poi)
	
	# Compare vs the record list if there's more than one item in it.
	if len(l_poi_max) > 1:
	
		# If the recorded pois are less than the current, remove it 
		# from the tracking list.
		for poi_max in l_poi_max:
			if poi_max.getValue() < poi.getValue():
				l_poi_max.remove(poi_max)
# End elif
```
### <a name="poi3.decision2"></a>Decision #2: Which POI is the closest?
If we still have a conflict, which is very likely since our POI values can reach a cap, we will pick the closest POI in terms of driving distance.
We know that we have a conflict when **l_poi_max** has more than one POI in it.
We can check the driving distance to POIs by setting a route to it then using the TraCI method *traci.vehicle.getDrivingDistance()*.
We store potential candidates in the list **l_poi_closest**.
```
# If there are more than one candidates, meaning that at least two
# POIs have the same value, we'll compare distances.
if len(l_poi_max) > 1:
	f_distance = -1.0
	f_closest_dist = -1.0
	l_poi_closest = []

	for poi_max in l_poi_max:
		# We can determine the distance by assigning a route to each poi
		# and then calling getDrivingDistance to find the distance retured
		# as a double
		s_dest_edge = poi_max.getClosestEdge()[0]
		traci.vehicle.changeTarget(veh.get_id(),s_dest_edge)
		f_distance = traci.vehicle.getDrivingDistance(veh.get_id(),s_dest_edge,1.0)

		# Compare distances
		# We automatically consider the first one
		if f_closest_dist == -1.0:
			f_closest_dist = f_distance
			l_poi_closest.append([poi_max,f_distance])

		# We check the other ones in the list
		else:
			# Add possible contendors to list.
			if f_distance <= f_closest_dist:
				f_closest_dist = f_distance
				l_poi_closest.append([poi_max,f_distance])

			# Remove non-contendors from the list
			for poi_closest in l_poi_closest:
				if poi_closest[1] > f_distance:
					l_poi_closest.remove(poi_closest)

			# end for poi_closest in l_poi_closest:
		# end else
	# end for poi_max in l_poi_max:
```
### <a name="poi3.decision3"></a>Decision #3: Randomly choose a POI.
If we still have a conflict, in which the chances are almost zero (0), we will choose between the remaining candidates at random.
We know that there is a conflict when there is greater than one POI in **l_poi_closest**.
```
	# If the two values are the same, one of POIs will be picked at random.
	if len(l_poi_closest) > 1:
		n_random_int = random.randint(0,len(l_poi_closest))
		s_dest_edge = l_poi_closest[n_random_int][0]
```
### <a name="poi3.minor_tweaks"></a>Minor Tweaks
Since there are two "go home" conditions, we vary the colors of an "exiting" vehicle.
```
# Change color so we can see when cars go home. The colors will
# vary by reason for going home.

# REASON: No more capacity. Cars will turn CYAN.
if is_full:
	traci.vehicle.setColor(veh.get_id(),(0,255,255,0))

# REASON: Visited every unique POI. Cars will turn GREEN  
elif is_bored:
	traci.vehicle.setColor(veh.get_id(),(0,255,0,0))
	
# REASON: Unknown. Cars will turn DARK GREY
# If cars are grey, there's a logic problem!
else:
	traci.vehicle.setColor(veh.get_id(),(30,30,30,0))
```
<!-- end poi3 -->
---
<!-- begin reroute1 -->
## <a name="reroute1"></a>reroute1
[Top](#top_of_page) , [Step #1](#reroute1.step1) , [Step #2](#reroute1.step2) , [Step #3](#reroute1.step3) , [Step #4](#reroute1.step4)
<br/>
![grid2.reroute1.gif](../../assets/screenshots/projects/grid2.reroute1.gif)
<br/>The project *reroute1* is the first example created on the *grid2* project. Here we have two goals:
1. Add lots of traffic that flows **east -> west** and **west -> east** along the four-lane highway through town.
2. Send some vehicles downtown and then once they arrive, send them back to their original destination.

### <a name="reroute1.step1"></a>Step #1: Create some traffic.
[reroute1](#reroute1)<br/>
The first step is to create a natural flow of traffic moving through our city. To create this flow we use a uniform distribution between 0.0 and 1.0 so that half of the vehicles created are routed eastbound and the other half of vehicles are routed westbound.

```
# We want half of the vehicles to travel eastbound and half
# To travel westbound.
if (random.uniform(0.0,1.0) > 0.5):
	traci.vehicle.add(s_vehicle_id, "eastbound", depart=n_step+1, pos=-4, speed=-3, lane=-6, typeID="chevy_s10")
	s_dest_edge = "gneE50"
else:
	traci.vehicle.add(s_vehicle_id, "westbound", depart=n_step+1, pos=-4, speed=-3, lane=-6, typeID="chevy_s10")
	s_dest_edge = "-gneE52"
```

### <a name="reroute1.step2"></a>Step #2: Select some vehicles to be sent downtown.
[reroute1](#reroute1)<br/>
The next step is to start to the rerouting process by selecting a vehicle currently traveling *eastbound* or *westbound*.
During this step we also need to save the original destination (which is the edge leading out of the city) so that when the reroute is complete, it can procede onto it's original destination.

We let Python decide which vehicles are to be rerouted with the *random* library.

```
# Pick a vehicle at random to reroute.
ls_veh_ids = traci.vehicle.getIDList()
n_random_int = random.randint(0,len(ls_veh_ids)-1)
s_veh_id = ls_veh_ids[n_random_int]
```
### <a name="reroute1.step3"></a>Step #3: Store destinations into memory.
[reroute1](#reroute1)<br/>
Before we send the vehicles downtown we need to save a few things into memory. 
We store three pieces of data into the global variable **LLS_VEH_DATA**, the vehicle ID, the destination edge ID of the route downtown, and the edge where it will exit the city.
First we retrieve it's original destination by retrieiving the last edge in the current route set.

```
# Store the exit destination edge before we change it's route.
s_exit_edge = traci.vehicle.getRoute(s_veh_id)[-1]
```
The edge that the vehicle will be going to downtown is hardcoded so we'll save that to a variable.

```
# Send it someplace downtown.
s_dest_edge = "-gneE35"
traci.vehicle.changeTarget(s_veh_id,s_dest_edge)
```
Then, we'll add our vehicle to **LLS_VEH_DATA** if we don't find that it's already been added to the list.
>Quentin: This part is buggy and doesn't let vehicles be rerouted a second time.
>If a vehicle is rerouted after it's already reached it's downtown destination, it may become unsubscribed from TraCI and throw an error.
>It has been corrected in example [poi1](../poi1/Readme.md).

```
# Add it to LLS_VEH_DATA to be tracked.
global LLS_VEH_DATA
is_found = False
for ls_row in LLS_VEH_DATA:
	if (s_veh_id == ls_row[0]):
		is_found = True
if (not is_found):
LLS_VEH_DATA.append([s_veh_id,s_exit_edge,s_dest_edge])
```
### <a name="reroute1.step4"></a>Step #4: Handle vehicles that arrive downtown.
[reroute1](#reroute1)<br/>
The last step is to handle vehicles that have arrived at their destination. We do this inside the *timestep(n_step)* method.

```
# If the vehicles that went downtown have reached their destination.
# they will head towards their original exit.
for ls_row in LLS_VEH_DATA:
# 0 is the vehicle ID and 2 is the next destination
	try:
		if (traci.vehicle.getRoadID(ls_row[0]) == ls_row[2]):
			# The vehicle has arived, send it on it's way. The exit destination
			# 1 is the exit edge
			traci.vehicle.changeTarget(ls_row[0],ls_row[1])
			
			# Change the color to blue so we can recognize accomplished cars
			traci.vehicle.setColor(ls_row[0],(0,0,255,0))
			
			# remove the vehicle from the list since we no longer have a
			LLS_VEH_DATA.remove(ls_row)
	  # end if
	  
	# This exception is called when a vehicle teleports beyond the ending
	#  destination and doesn't get properly removed from this list. I need
	#  to find some way to recognize when something teleports and remove
	#  it, or find handle it some other way.
	except:
		LLS_VEH_DATA.remove(ls_row)
``` 

<!-- end reroute1 -->
---
