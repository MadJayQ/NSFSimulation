#!/bin/bash
# Edit these
project="Haines_City"
prj_dir="../"
begin=0
end=30000

# Do not edit these
project=$project
net_xml=$project".net.xml"
osm=$project".osm"
typ_xml="osm.typ.xml"
poly_xml=$project".poly.xml"
rou_xml=$project".rou.xml"
sumocfg=$project".sumocfg"
geo_sumocfg=$project"_geo.sumocfg"

# Clean out old files
rm $prj_dir$net_xml *.sumocfg
echo "Old .net.xml file(s) removed. Creating a new one..."

# Set SUMO_HOME var
export SUMO_HOME="/home/veins/src/sumo-0.30.0"

# Netconvert
netconvert --osm-files $prj_dir$osm -o $prj_dir$net_xml \
--roundabouts.guess --ramps.guess \
 --junctions.join --tls.guess-signals --tls.discard-simple --tls.join
echo "netconvert Complete."

# Polyconvert
polyconvert --net-file $prj_dir$net_xml --osm-files $prj_dir$osm --type-file $typ_xml -o $prj_dir$poly_xml
echo "polyconvert Complete."

# Route File
echo -e "<routes>\n</routes>" > $prj_dir$rou_xml

# Sumocfg File w/ Geometry
echo "<configuration>" > $prj_dir$geo_sumocfg
echo -e "\t<input>" >> $prj_dir$geo_sumocfg
echo -e "\t\t<net-file value=\""$net_xml"\" />" >> $prj_dir$geo_sumocfg
echo -e "\t\t<route-files value=\""$rou_xml"\" />" >> $prj_dir$geo_sumocfg
echo -e "\t\t<additional-files value=\""$poly_xml"\" />" >> $prj_dir$geo_sumocfg
echo -e "\t</input>" >> $prj_dir$geo_sumocfg
echo -e "\t<time>" >> $prj_dir$geo_sumocfg
echo -e "\t\t<begin value=\""$begin"\" />" >> $prj_dir$geo_sumocfg
echo -e "\t\t<end value=\""$end"\" />" >> $prj_dir$geo_sumocfg
echo -e "\t</time>" >> $prj_dir$geo_sumocfg
echo "</configuration>" >> $prj_dir$geo_sumocfg
echo "Geometry config file created."

# Sumocfg File
echo "<configuration>" > $prj_dir$sumocfg
echo -e "\t<input>" >> $prj_dir$sumocfg
echo -e "\t\t<net-file value=\""$net_xml"\" />" >> $prj_dir$sumocfg
echo -e "\t\t<route-files value=\""$rou_xml"\" />" >> $prj_dir$sumocfg
echo -e "\t</input>" >> $prj_dir$sumocfg
echo -e "\t<time>" >> $prj_dir$sumocfg
echo -e "\t\t<begin value=\""$begin"\" />" >> $prj_dir$sumocfg
echo -e "\t\t<end value=\""$end"\" />" >> $prj_dir$sumocfg
echo -e "\t</time>" >> $prj_dir$sumocfg
echo "</configuration>" >> $prj_dir$sumocfg
echo "Config file created."

# Clean Unknowns from the .poly.xml
python3 remove_unknown.py --poly_xml=$prj_dir$poly_xml
rm temp.poly.xml
echo 'type="unknown"s removed from .poly.xml'

# Unset variables
unset project
unset prj_dir
unset begin
unset end
unset net_xml
unset osm
unset typ_xml
unset poly_xml
unset sumocfg
unset geo_sumocfg
echo 'Variables successfully unset.'
