#!/bin/bash
# Execution Script run MPM Gauss

#-----------------------                                                                     
# Create  Mesh and Entity Sets                                       
#-----------------------
 
python3 createMesh.py --xMin 0 --xMax 100 --yMin 0 --yMax 50 --xCells 100 --yCells 50 --entitySets entityInfo.json 


#-----------------------
# Create Gauss Points
#-----------------------
# Run MPM
~/Research/mpm/build/./mpm -i mpm_gauss.json -f $(pwd)/



