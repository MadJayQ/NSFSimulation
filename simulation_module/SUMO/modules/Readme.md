# <a name="top_of_page"></a>modules
[GUI](#gui) , [Point of Interest](#poi) , [sumo2json](#sumo2json) , [Vehicle](#vehicle)
>Quentin: This section contains notes about the various python modules we created.
>
>[Sumo + TraCI Home](../Readme.md)

---
<!-- begin GUI -->
## <a name="gui"></a>GUI
[Top](#top_of_page)

Documention for the GUI has it's own readme [gui.md](./gui/gui.md).
<!-- end GUI --> 
---
<!-- begin poi -->
## <a name="poi"></a>Point of Interest
[Top](#top_of_page)

A class created to manage Point of Interest (POI) nodes featuring coordinates, values, increase/decrease and vehicle hit methods.
Useful code:
```
# Importing the POI library
import poi

# Initializing a POI object
# closest_edge = (edge_ID,x,y)
# poi.poi(id,x,y,value,closest_edge)
o_poi = poi.poi("veh0",30.0,25.0,50,("gneE15",15.4,10.3))
```
<!-- end poi -->
---
<!-- begin sumo2json -->
## <a name="sumo2json"></a>sumo2json
[Top](#top_of_page) , [Changelog](#sumo2json_changelog

`sumo2json` is a module that converts data from a `.net.xml` file into two seperate `.json` files:
- `junctions.json` which contains node data.
- `edges.json` which contains edge data.

Combined, these two `.json` files contain the info of a directed graph for any SUMO map.
This module is an independent command line interface program that we can run will the following command as long as we're in the same directory as `sumo2json.py`.

`python3 sumo2json.py --net_xml NET_XML`

We must point to the `.net.xml` file using the `--net_xml` or `-f` flags followed by the file name. Sample usage using the `Davenport.net.xml` test file within the module directory:

```
python3 sumo2json.py --net_xml Davenport.net.xml
                    [ or ]
python3 sumo2json.py -f Davenport.net.xml 
```

Failure to specify a `.net.xml` file or by specifying one without the `.net.xml` extension will result in an exception being raised.

### <a name="sumo2json_changelog"></a>Changelog
[sumo2json](#sumo2json) ,  [Version 2](#sumo2json_changelog_2)

#### <a name="sumo2json_changelog_2"><a/>Version 2
Added the the fields `from` and `to` which contains strings of the junction ids.

<!-- end sumo2json -->
---
<!-- begin vehicle -->
## <a name="vehicle"></a>Vehicle
[Top](#top_of_page)

A class created to manage Vehicles featuring edge/POI memory and capacity.
Useful code:
```
# Importing the Vehicle library
import vehicle

#Initializing a Vehicle object
# vehicle.vehicle(id)
o_veh = vehicle.vehicle("veh0")
```
<!-- end vehicle -->
