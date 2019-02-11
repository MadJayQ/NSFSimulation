#!/bin/bash

# Batch converts all current maps

version=2
sumo2json_py='/home/veins/src/sumo-traci-python3/modules/sumo2json/version'$version'/sumo2json.py'

projects=('3choices' 'Davenport' 'grid2' 'Haines_City' 'intersection_1' 'leopard')

for project in ${projects[@]}; do
  net_xml='/home/veins/src/sumo-traci-python3/projects/'$project'/data/'$project'.net.xml'
  rm -r $project
  mkdir $project
  python3 $sumo2json_py --net_xml=$net_xml
  mv *.json -t $project
done

# FlPoly is a special case and doesn't follow the standard folder structure
project='flpoly'
net_xml='/home/veins/src/sumo-traci-python3/projects/'$project'/data/Version2/'$project'.net.xml'
rm -r $project
mkdir $project
python3 $sumo2json_py --net_xml=$net_xml
mv *.json -t $project
