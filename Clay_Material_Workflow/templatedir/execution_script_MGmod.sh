#!/bin/bash
# Execution Script to setup and run MPM for Dakota

#-----------------------
# Stress Initialization
#-----------------------

python3 initParticleStress.py --particlesFile /$(pwd)/results/gauss_points/particles0.h5 --stressConfig stressConfig.in 

#----------------
# MPM Simulation 
#----------------
 # Script to change mpm.in to mpm.json and get ride of dakota lines
python3 mpm2json.py --mpm_in  mpm.in


# Run MPM
~/Research/mpm/build/./mpm -i mpm.json -f $(pwd)/



