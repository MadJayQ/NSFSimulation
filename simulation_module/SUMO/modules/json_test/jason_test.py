import json

dict_junction = { "junction":
  {
    "id": "gneJ33",
    "true_center_coords": [-40.30,20.45],
    "graphics_center_coords": [13,52],
    "neighbors":[["gneJ5",4],["gneJ77",76],["gneJ52",51]]
  }
}


json_file = "file.json"
with open(json_file,'w+') as f:
  json.dump(dict_junction,f)
  
with open(json_file,'r') as f:
  data = json.load(f)
  
print(type(data["junction"]["true_center_coords"]))
