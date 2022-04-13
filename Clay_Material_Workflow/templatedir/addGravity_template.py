#!/usr/bin/env python3

import numpy as np
import argparse
import sys
import json
import pandas as pd


# Input slope angle - output mpm.json with gravity adjusted 
inputFile = {slope_angle}
outputFile = sys.argv[1]

def gravity(inputFile):
	x_gravity = 9.81*np.sin(np.deg2rad(int(inputFile))) # For some reason is calculating in radians
	y_gravity = -9.81*np.cos(np.deg2rad(int(inputFile)))
	return x_gravity, y_gravity



def write_output(x_gravity, y_gravity):  # Update gravity in mpm.json
    with open(outputFile, "r") as f:
        filedata = f.read()
        filedata = filedata.replace('x_gravity', str(x_gravity))
        filedata = filedata.replace('y_gravity', str(y_gravity))
        with open(outputFile, "w") as g:
        	g.writelines(filedata)
        	

def main():
    x_gravity, y_gravity = gravity(inputFile)
    write_output(x_gravity, y_gravity)


if __name__ == "__main__":
    main()

