# Test file for vehicle class.
import vehicle
print("Vehicle class imported.")
veh = vehicle.vehicle("veh0")
print("Vehicle has initialized.")

print()
print(veh.get_id())
veh.set_id("veh55")
print(veh.get_id())

print()
print(veh.get_next_dest_edge_id())
veh.set_next_dest_edge_id("-gneE77")
print(veh.get_next_dest_edge_id())

print()
print(veh.get_final_dest_edge_id())
veh.set_final_dest_edge_id("-gneE100")
print(veh.get_final_dest_edge_id())

print()
print(str(veh.get_capacity()))
veh.set_capacity(30)
print(str(veh.get_capacity()))
veh.increase_capacity(5)
print(str(veh.get_capacity()))

print()
print(veh.get_visited_pois())
veh.set_visited_pois(["poi0","poi1","poi2"])
print(veh.get_visited_pois())
veh.add_visited_pois("poi73")
print(veh.get_visited_pois())
veh.discard_visited_pois("poi1")
print(veh.get_visited_pois())

del veh
try:
  veh.get_id()
except:
  print()
  print("veh deleted sucessfully.")


print("Vehicle class test sucessfully completed.")
