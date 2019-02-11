#!/bin/bash
# Edit these
project="flpoly"
begin=0
end=30000

# Do not edit these
net_xml=$project".net.xml"
osm=$project".osm"
typ_xml="osm.typ.xml"
poly_xml=$project".poly.xml"
rou_xml=$project".rou.xml"
sumocfg=$project".sumocfg"
geo_sumocfg=$project"_geo.sumocfg"

# Clean out old files
rm *.net.xml *.sumocfg
echo "Old .net.xml file(s) removed. Creating a new one..."

# Netconvert
netconvert --osm-files $osm -o $net_xml \
--roundabouts.guess --ramps.guess \
 --junctions.join --tls.guess-signals --tls.discard-simple --tls.join
echo "netconvert Complete."

# Polyconvert
polyconvert --net-file $net_xml --osm-files $osm --type-file $typ_xml -o $poly_xml
echo "polyconvert Complete."

# Route File
echo -e "<routes>\n</routes>" > $rou_xml

# Sumocfg File w/ Geometry
echo "<configuration>" > $geo_sumocfg
echo -e "\t<input>" >> $geo_sumocfg
echo -e "\t\t<net-file value=\""$net_xml"\" />" >> $geo_sumocfg
echo -e "\t\t<route-files value=\""$rou_xml"\" />" >> $geo_sumocfg
echo -e "\t\t<additional-files value=\""$poly_xml"\" />" >> $geo_sumocfg
echo -e "\t</input>" >> $geo_sumocfg
echo -e "\t<time>" >> $geo_sumocfg
echo -e "\t\t<begin value=\""$begin"\" />" >> $geo_sumocfg
echo -e "\t\t<end value=\""$end"\" />" >> $geo_sumocfg
echo -e "\t</time>" >> $geo_sumocfg
echo "</configuration>" >> $geo_sumocfg
echo "Geometry config file created."

# Sumocfg File
echo "<configuration>" > $sumocfg
echo -e "\t<input>" >> $sumocfg
echo -e "\t\t<net-file value=\""$net_xml"\" />" >> $sumocfg
echo -e "\t\t<route-files value=\""$rou_xml"\" />" >> $sumocfg
echo -e "\t</input>" >> $sumocfg
echo -e "\t<time>" >> $sumocfg
echo -e "\t\t<begin value=\""$begin"\" />" >> $sumocfg
echo -e "\t\t<end value=\""$end"\" />" >> $sumocfg
echo -e "\t</time>" >> $sumocfg
echo "</configuration>" >> $sumocfg
echo "Config file created."



# Unset variables
unset net_xml
unset osm
unset typ_xml
unset poly_xml
unset sumocfg
unset geo_sumocfg
