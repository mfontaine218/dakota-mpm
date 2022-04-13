# MPM Post Process

# Command Line
# python3 mpm_postProcess.py particles09.h5 mpmpostProcess.txt

import sys
import os
import numpy as np
import pandas as pd


# Input one of the MPM results files (ie Stresses from time step 10)
inputFile = sys.argv[1]
outputFile = sys.argv[2]


def hd5_2_df():  # Read hd5 file data
    df = pd.read_hdf(inputFile)   # Read file
    velocity = df[['velocity_x', 'velocity_y']]  # Pull out velocities
    return velocity


def v_nonzero(velocity):   # count number of particles that moved (magnitude)
    v_nonzero = 0
    for x, y in zip(velocity.velocity_x, velocity.velocity_y):
        if (x**2 + y**2)**(1/2) > 0.5:  # Set threshold velocity
            v_nonzero = v_nonzero + 1

    vol_fraction = ((v_nonzero/len(velocity.velocity_x))*100)
    return vol_fraction


def avg_velocity(velocity):
    avg_x = (velocity['velocity_x'].loc[velocity['velocity_x'] != 0]).mean()
    avg_y = (velocity['velocity_y'].loc[velocity['velocity_y'] != 0]).mean()
    return avg_x, avg_y


def generate_output(vol_fraction, avg_x, avg_y):
    values = np.array([vol_fraction, avg_x, avg_y])
    s = str(values)[1:-1]
    return s


def write_output(s):  # Write results to file results.out should be sys.argv[2]
    with open(outputFile, "w") as f:
        f.write(s)


def main():
    velocity = hd5_2_df()
    vol_fraction = v_nonzero(velocity)
    avg_x, avg_y = avg_velocity(velocity)
    s = generate_output(vol_fraction, avg_x, avg_y)
    write_output(s)


if __name__ == "__main__":
    main()
