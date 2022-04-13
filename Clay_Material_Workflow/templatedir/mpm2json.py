#!/usr/bin/env python3

import numpy as np
import argparse
import sys
import json
import pandas as pd


def mpm2json():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Change Dakota mpm.in to mpm.json')
    # Required arguments
    parser.add_argument('--mpm_in', nargs=1,
                    help='mpm.in file from Dakota', required=True)
    

    # Parse command line arguments
    args = parser.parse_args(sys.argv[1:])
    
    # Read mpm.in and skip lines
    with open(args.mpm_in[0]) as data_file:
        json_obj = "\n".join(data_file.readlines()[7:-2])  # Skip extra lines added by dakota 
 
  
    with open("mpm.json", "w") as sfile:
        sfile.write(json_obj)
            
               
        
if __name__ == '__main__':
    mpm2json()
