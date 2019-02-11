# <a name="top_of_page"></a>GUI module
[Version 1](#version1) , [Version 2](#version2) , [Version 3](#version3) , [Version 4](#version4)

>Quentin: Here we have notes about a module that visualizes *.net.xml* maps and converts them into simple directional graphs.
>
>[Modules Homes](../Readme.md)

The purpose of the GUI module is to practice the following:
1. Retrieving information from the *.net.xml* file such as *node*, *edge*, or *boundary* information.
2. Creating a directed graph out of *node* + *edge* information.
3. Plotting this information to a window for visualization.

To try out any of the GUI versions, open up the `test.py` within the verision direction and point it to a `.net.xml` file by changing the variable `s_path_of_net_xml`.

## <a name="version1"></a>Version 1
[Top](#top_of_page)<br/>
Within Version 1, we create a very basic graphics window using the graphics.py library.
We retrieve the boundaries from the *.net.xml* file. Most notably, non-zero coordinates such as `bottom_left(-30.5,-3.0) top_right(40.3,15.0)` are adjusted to fit neatly in a window where the window is structured like:
```
(0,0)
+------>
|    +x
|
| +y
v
```
Our example coordinates would be adjusted to fit neatly into a window and become something like:
```
x_adj = 0 - bottom_left.x  + window_padding
x_adj = 0 - -30.5 + 10
x_adj = 40.5

y_adj = 0 - bottom_left.y  + window_padding
y_adj = 0 - -3.0 + 10
y_adj = 13
```
The new coordinates are `bottom_left(10,10) top_right(80.8,28.0)`and fit nicely into a graphical window.

## <a name="version2"></a>Version 2
[Top](#top_of_page)<br/>
Version 2 introduces a new feature to create a directed graph by parsing the *.net.xml* file for junctions (nodes) and edges then plotting them to a graphical window.
a second window with some simple navigation buttons is included to view maps that do not fit within the boundaries of a window.

To enable the directed graphic in the `test.py` file, ensure that `is_minimap_mode=True`.

## <a name="version3"></a>Version 3
[Top](#top_of_page)<br/>
Version 3 contains some performance and graphical tweaks to version 2.
It is currently the most stable version.

## <a name="version4"><a/>Version 4
[Top](#top_of_page)<br/>
Verison 4 attempts to scale with very large maps (where the `.net.xml` is one megabyte or larger).

>Quentin: A very large `.net.xml` is included.
>It is at `./test_map/Davenport.net.xml`

Notably, Junction (node) and edge data, which is used to produce a directed graph is saved in `.json` format.
```
# Sample from junctions.json

"100001531": {
		 "true_center_coords": [16811.38,18175.29],
		 "graphical_center_coords": [4319,9839.12]
},

# Sample from edges.json

"2687588940_to_2687589854": {
		"true_coords": [[25168.0,22545.59],[25572.24,23253.28]],
		"graphical_coords": [[12676,5469.120000000001],[13080,4761.120000000001]]
},
```
