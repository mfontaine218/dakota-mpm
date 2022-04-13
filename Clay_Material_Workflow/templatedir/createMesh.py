import numpy as np
import argparse
import sys
import json
from itertools import chain

def createMesh():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Create 2-D mesh for MPM')
    # Required arguments
    parser.add_argument('--xMin', type=float, nargs=1,
                        help='Min x value', required=True)
    parser.add_argument('--xMax', type=float, nargs=1,
                        help='Max x value', required=True)
    parser.add_argument('--yMin', type=float, nargs=1,
                        help='Min y value', required=True)
    parser.add_argument('--yMax', type=float, nargs=1,
                        help='Max y value', required=True)
    parser.add_argument('--xCells', type=int, nargs=1,
                        help='Number of cells in x direction', required=True)    
    parser.add_argument('--yCells', type=int, nargs=1,
                        help='Number of cells in y direction', required=True)
    # Arguments for creating entity sets
    parser.add_argument('--entitySets', nargs=1,
                         help='JSON file containing information for creating node entity sets')

    args = parser.parse_args(sys.argv[1:])

    # Calculate node locations
    xLocations = np.empty([args.xCells[0] + 1])
    yLocations = np.empty([args.yCells[0] + 1])    
    deltaX = (args.xMax[0] - args.xMin[0]) / float(args.xCells[0])
    deltaY = (args.yMax[0] - args.yMin[0]) / float(args.yCells[0])    
    
    for i in range(args.xCells[0] + 1):
        xLocations[i] = i * deltaX

    for i in range(args.yCells[0] + 1):
        yLocations[i] = i * deltaY

    idArray = np.empty([args.yCells[0] + 1, args.xCells[0] + 1])
    for i in range(args.xCells[0] + 1):
        for j in range(args.yCells[0] + 1):
            idArray[j, i] = int(i + j * (args.xCells[0] + 1))

    cellArray = np.empty([args.xCells[0] * args.yCells[0]], dtype=object)
    
    with open('mesh.txt', 'w') as f:
        f.write("! elementShape quadrilateral\n")
        f.write("! elementNumPoints 4\n")
        f.write("%s %s\n" % ((len(xLocations) * len(yLocations)), (args.xCells[0] * args.yCells[0])))

        # Write node locations to file
        for y in yLocations:        
            for x in xLocations:
                f.write("%s %s\n" % (x, y))

        # Write cells to file
        counter = 0
        for i in range(args.yCells[0]):
            for j in range(args.xCells[0]):
                cell = [int(idArray[i, j]), int(idArray[i, j + 1]), int(idArray[i + 1, j + 1]), int(idArray[i + 1, j])]
                cellArray[counter] = cell
                f.write("%s %s %s %s\n" % (cell[0], cell[1], cell[2], cell[3]))
                counter = counter + 1

    # Create entity sets
    if args.entitySets is not None:
        with open(args.entitySets[0]) as data_file:
            entityData = json.load(data_file)        
            nodeSets = { "node_sets" : [] }
            cellSets = { "cell_sets" : [] }
            
            for val in entityData["node_sets"]:
                if "axis" in val: 
                    setId = int(val["id"])                
                    # Axis along which to add nodes to set
                    axis = int(val["axis"])
                    # Location of axis for node set, specified as integer indicating row or column of nodes
                    location = int(val["location"])

                    if axis == 0:
                        nodeSet = idArray[location, :].astype('int')
                    elif axis == 1:
                        nodeSet = idArray[:, location].astype('int')

                    currentSet = { "id" : setId, "set" : nodeSet.tolist() }
                    nodeSets["node_sets"].append(currentSet)

                if "box" in val:
                    box = val["box"]
                    setId = int(val["id"])                                    
                    nodeSet = idArray[box[2]:(box[3] + 1), box[0]:(box[1] + 1)].astype('int')
                    currentSet = { "id" : setId, "set" : list(chain.from_iterable(nodeSet.tolist())) }
                    nodeSets["node_sets"].append(currentSet)
                    
            for val in entityData["cell_sets"]:
                if "axis" in val:
                    setId = int(val["id"])                
                    # Axis along which to add cells to set
                    axis = int(val["axis"])
                    # Location of axis for cell set, specified as integer indicating row or column of nodes
                    location = int(val["location"])

                    cellSet = []
                    counter = 0
                    nodeSet = np.empty(0)

                    if axis == 0:
                        nodeSet = idArray[location, :].astype('int')
                    elif axis == 1:
                        nodeSet = idArray[:, location].astype('int')

                    for cell in cellArray:
                        if len(list(set(nodeSet.tolist()) & set(cell))) != 0:
                            cellSet.append(counter)
                                
                        counter = counter + 1

                    currentSet = { "id" : setId, "set" : cellSet }
                    cellSets["cell_sets"].append(currentSet)

                if "box" in val:
                    box = val["box"]
                    setId = int(val["id"])                                    
                    nodeSet = idArray[box[2]:(box[3] + 1), box[0]:(box[1] + 1)].astype('int')
                    
                    cellSet = []
                    counter = 0

                    for cell in cellArray:
                        if len(list(set(list(chain.from_iterable(nodeSet.tolist()))) & set(cell))) == 4:
                            cellSet.append(counter)
                                
                        counter = counter + 1

                    currentSet = { "id" : setId, "set" : cellSet }
                    cellSets["cell_sets"].append(currentSet)                   
                    
            nodeAndCellSets = { "node_sets" : nodeSets["node_sets"], "cell_sets" : cellSets["cell_sets"]}
            jsonData = json.dumps(nodeAndCellSets, indent = 2)

            with open("entity_sets.json", "w") as outfile:
                outfile.write(jsonData)                

if __name__ == '__main__':
    createMesh()
