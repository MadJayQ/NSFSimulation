#!/bin/bash
name="university.net.xml"
osm_file="university.osm"
type_file="osm.typ.xml"
poly_file="university.poly.xml"
rm *.net.xml
echo "Old .net.xml file(s) removed. Creating a new one..."
netconvert --osm-files $osm_file -o $name \
--roundabouts.guess --ramps.guess \
 --junctions.join --tls.guess-signals --tls.discard-simple --tls.join
echo "netconvert Complete."
polyconvert --net-file $name --osm-files $osm_file --type-file $type_file -o $poly_file
echo "polyconvert Complete."
unset name
unset osm_file
unset type_file
unset poly_file
