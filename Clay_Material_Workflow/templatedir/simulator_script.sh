#!/bin/sh
# Sample simulator to Dakota system call script

# The first and second command line arguments to the script are the
# names of the Dakota parameters and results files.
params=$1
results=$2

# --------------
# PRE-PROCESSING
# --------------

# Incorporate the paramters from Dakota into the templates for geometry

## enity sets  --> createmesh
dprepro3 $params entityInfo_template.json  entityInfo.json

#Create Geometry
create_geometry_script.sh


# Incorporate the parameters from Dakota into the template for mpm.json

dprepro3 $params mpm_template.json  mpm.in

# Calculate and add in gravity
dprepro3 $params addGravity_template.py  addGravity.py

python3 addGravity.py  mpm.in

# Incorporate the parameters from Dakota into the template for stressConfig.json

dprepro3 $params stressConfig_template.json  stressConfig.in

# Calculate and add in friction boundary
dprepro3 $params frictionBoundary_template.py  frictionBoundary.py

python3 frictionBoundary.py  mpm.in

# ---------
# EXECUTION # Write another shell script for execuation
# ---------

# Shell script here to run 1. Stress initilization 2. MPM simulation

execution_script_MGmod.sh

# ---------------
# POST-PROCESSING
# ---------------

# Print file name to see if correct particle is used
ls /$(pwd)/results/Dakota_MPM_LondonClay/particles*.h5 | tail -1

# Python process script
python3 mpm_postProcess.py `ls /$(pwd)/results/Dakota_MPM_LondonClay/particles*.h5 | tail -1`   $results
