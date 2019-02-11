#!/bin/bash
name="university.net.xml"
rm *.net.xml
echo "Old .net.xml file(s) removed. Creating a new one..."
netconvert --osm-files university.osm -o $name \
--geometry.remove --roundabouts.guess --ramps.guess \
 --junctions.join --tls.guess-signals --tls.discard-simple --tls.join
echo "Convert Complete. Opening in netedit!"
netedit $name
