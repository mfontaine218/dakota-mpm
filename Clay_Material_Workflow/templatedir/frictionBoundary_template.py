#!/usr/bin/env python3

import numpy as np
import argparse
import sys
import json
import pandas as pd


# Input friction angle - output mpm.json with friction at boundary adjusted 
inputFile = {friction}
outputFile = sys.argv[1]

def friction_calc(inputFile):
	friction_boundary = np.tan(np.deg2rad(int(inputFile))) # np.trig functions default is calculating in radians
	return friction_boundary



def write_output(friction_boundary):  # Update friction_boundary in mpm.json
    with open(outputFile, "r") as f:
        filedata = f.read()
        filedata = filedata.replace('friction_boundary', str(friction_boundary))
        with open(outputFile, "w") as g:
        	g.writelines(filedata)
        	

def main():
    friction_boundary = friction_calc(inputFile)
    write_output(friction_boundary)


if __name__ == "__main__":
    main()

