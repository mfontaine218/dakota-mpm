#!/usr/bin/env python3

import numpy as np
import argparse
import sys
import json
import pandas as pd


def initParticleStress():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Create input text files MPM particles and their initial stresses')
    # Required arguments
    parser.add_argument('--particlesFile', nargs=1,
                        help='HDF5 file containing particle info', required=True)
    parser.add_argument('--stressConfig', nargs=1,
                        help='JSON file containing info for initializing stress', required=False)

    # Parse command line arguments
    args = parser.parse_args(sys.argv[1:])

    # Read particle info
    df = pd.read_hdf(args.particlesFile[0], 'table')
    k0 = 0.0
    density = 0.0
    slopeAngle = 0.0
    groundSurface = 0.0
    gravity = 0.0

    # Write particle locations to file
    with open("particles.txt", "w") as pfile:
        pfile.write("%s\n" % len(df['coord_y']))
        np.savetxt(pfile, df[['coord_x', 'coord_y']].values)

    # Calculate TOTAL stresses on each particle
    # transAngle = np.deg2rad(360.0 - slopeAngle)
    # c = np.cos(transAngle)
    # c2 = c**2
    # s = np.sin(transAngle)
    # s2 = s**2
    # sc = s * c
    # transMatrix = np.array([[c2, s2, 2.0 * sc], [s2, c2, -2.0 * sc], [-sc, sc, c2 - s2]])
    # R = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 2]])
    # invR = np.linalg.inv(R)
    # reuterTrans = R.dot(transMatrix.dot(invR))

    print(np.max(df[['coord_y']].values))

    if args.stressConfig is not None:
        with open(args.stressConfig[0]) as data_file:
            json_obj = "\n".join(data_file.readlines()[7:14])  # Skip extra lines added by dakota 
            stressData = json.loads(json_obj)
            k0 = float(stressData["K0"])
            density = float(stressData["density"])
            slopeAngle = float(stressData["slopeAngle"])
            groundSurface = float(stressData["groundSurface"])
            gravity = float(stressData["gravity"])

        with open("particles-stresses.txt", "w") as sfile:
            sfile.write("%s\n" % len(df['coord_y']))
            for particle in df[['coord_x', 'coord_y']].values:
                # vstress = -density * gravity * (groundSurface - particle[1])
                vstress = -density * gravity * \
                    (groundSurface - particle[1]) / \
                    np.cos(np.deg2rad(slopeAngle))
                hstress = k0 * vstress
                shear = 0.0
                princStresses = np.array([hstress, vstress, shear])
                # transStesses = reuterTrans.dot(princStresses)
                transStesses = princStresses
                sfile.write("%s %s %s %s %s %s\n" % (transStesses[0], transStesses[1], transStesses[0],
                                                     transStesses[2], 0.0, 0.0))


if __name__ == '__main__':
    initParticleStress()
