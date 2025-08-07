
"""
cells_info.py

High-level specifications for S1-thalamus network model using NetPyNE

Contributors: salvadordura@gmail.com, fernandodasilvaborges@gmail.com

# edges files not inclued in https://github.com/FernandoSBorges/
"""

import numpy as np
import json


def cellsINFO(sample = "6cells", layer = 4, distance2Dmin = 0, distance2Dmax = 150):
    
    print('\n\n',sample, layer, distance2Dmin, distance2Dmax,'\n\n')

    from bluepysnap import Circuit
    from bluepysnap.bbp import Cell

    CircuitPath = 'O1_data_physiology/'
    circuit_path = CircuitPath + 'circuit_config.json'
    circuit = Circuit(circuit_path)
    cells = circuit.nodes["S1nonbarrel_neurons"]
    nodesinfo = cells.get()

    def distance3D(gidpre,gidpost):
        return np.sqrt(np.power(nodesinfo['x'][gidpre]-nodesinfo['x'][gidpost],2)+np.power(nodesinfo['y'][gidpre]-nodesinfo['y'][gidpost],2)+np.power(nodesinfo['z'][gidpre]-nodesinfo['z'][gidpost],2))

    def distance2D(gidpre,gidpost):
        return np.sqrt(np.power(nodesinfo['x'][gidpre]-nodesinfo['x'][gidpost],2)+np.power(nodesinfo['y'][gidpre]-nodesinfo['y'][gidpost],2))

    def distance2Dmean(gidpre, mean_x, mean_y): # edited positions -> y depth
        return np.sqrt(np.power(nodesinfo['x_new'][gidpre]-mean_x,2)+np.power(nodesinfo['y_new'][gidpre]-mean_y,2))


    mtypes = sorted(cells.property_values(Cell.MTYPE))

    i = 0
    mntypes = {}
    for mn in sorted(mtypes):
        mntypes[mn] = i
        i+=1

    print(mntypes)

    #------------------------------------------------------------------------------
    # Select nodes to simulate
    #------------------------------------------------------------------------------
    node_gid = []
    hoclist = {}
    Morpholist = {}
    mean_x, mean_y = np.mean(nodesinfo['x_new']), np.mean(nodesinfo['y_new'])

    if sample == "6cells":    
        for gid in [108767, 141766, 138433, 140868, 125451, 118551]: 
            if str(layer) == nodesinfo['mtype'][gid][1] and distance2Dmean(gid, mean_x, mean_y) > distance2Dmin and distance2Dmean(gid, mean_x, mean_y) <distance2Dmax:  

                print(len(node_gid),gid,nodesinfo['synapse_class'][gid],nodesinfo['mtype'][gid],nodesinfo['model_template'][gid],nodesinfo['morphology'][gid],hex,distance2Dmean(gid, mean_x, mean_y))

                node_gid.append(gid)
                hoclist[gid] = nodesinfo['model_template'][gid][4:]
                Morpholist[gid] = nodesinfo['morphology'][gid] + '.asc'

    else:    

        f = open('node_sets.json') 
        node_sets = json.load(f) 

        for gid in node_sets['hex0']['node_id']: 
            if str(layer) == nodesinfo['mtype'][gid][1] and distance2Dmean(gid, mean_x, mean_y) > distance2Dmin and distance2Dmean(gid, mean_x, mean_y) <distance2Dmax:  

                print(len(node_gid),gid,nodesinfo['synapse_class'][gid],nodesinfo['mtype'][gid],nodesinfo['model_template'][gid],nodesinfo['morphology'][gid],hex,distance2Dmean(gid, mean_x, mean_y))

                node_gid.append(gid)
                hoclist[gid] = nodesinfo['model_template'][gid][4:]
                Morpholist[gid] = nodesinfo['morphology'][gid] + '.asc'

    #------------------------------------------------------------------------------
    # Save pop infos
    #------------------------------------------------------------------------------
    gid_list = {}
    cellName_list = {}
    cellsList = {}

    if sample == "6cells":    

        for ii,gid in enumerate(node_gid):

            cellName = nodesinfo['mtype'][gid] + '_' + nodesinfo['etype'][gid]        
            cellName_new = cellName + '_' + str(ii)
            
            cellName_list[gid] = cellName_new
            gid_list[cellName_new] = gid
            
            print('%s %s %s 1 1 %d' % (cellName_new,nodesinfo['mtype'][gid],nodesinfo['etype'][gid],gid))

            cellsList[cellName] = [{'x': nodesinfo['x_new'][gid], 'y': nodesinfo['y_new'][gid], 'z': nodesinfo['z_new'][gid]}]
            
    else:    
        for gid in node_gid:

            cellName = nodesinfo['mtype'][gid]                             
            cellName_list[gid] = cellName

            if cellName not in gid_list.keys():
                gid_list[cellName] = []

            gid_list[cellName].append(gid)
            
            print('%d %s %d' % (gid,cellName, len(gid_list[cellName])))

        for popName in sorted(gid_list.keys()):
            cellsList[popName] = []
            for gid in gid_list[popName]:                
                    cellsList[popName].append({'x': nodesinfo['x'][gid], 'y': nodesinfo['y'][gid], 'z': nodesinfo['z'][gid]})


    # return node_gid, hoclist, Morpholist, gid_list, cellName_list, cellsList
    Lista = {}
    Lista['hoclist'] = hoclist
    Lista['Morpholist'] = Morpholist
    Lista['gid_list'] = gid_list
    Lista['cellName_list'] = cellName_list
    Lista['cellsList'] = cellsList
    
    return Lista


# Get the Lista data
Lista = cellsINFO(sample="6cells", layer=4, distance2Dmin=0, distance2Dmax=300)

# Save Lista to a JSON file
output_filename = "cells_info_data.json"
with open(output_filename, "w") as f:
    json.dump(Lista, f, indent=4)

print(f"Data saved to {output_filename}")