
"""
cfg.py

High-level specifications for S1-thalamus network model using NetPyNE

Contributors: salvadordura@gmail.com, fernandodasilvaborges@gmail.com

# edges files not inclued in https://github.com/FernandoSBorges/
"""

from netpyne import specs
import json
import os
import numpy as np

cfg = specs.SimConfig()  

#------------------------------------------------------------------------------
#
# SIMULATION CONFIGURATION
#
#------------------------------------------------------------------------------

cfg.coreneuron = False

#------------------------------------------------------------------------------
# Select nodes to simulate
#------------------------------------------------------------------------------

f = open('cells_info_data.json') 

Lista = json.load(f) 

print(Lista)

cfg.hoclist = Lista["hoclist"]
cfg.Morpholist = Lista["Morpholist"]
cfg.gid_list = Lista["gid_list"]
# cfg.cellName_list = Lista["cellName_list"]
# cfg.cellsList = Lista["cellsList"]

cfg.Epops = []
cfg.Ipops = []
     
cfg.cellNumber = {}
cfg.popLabel = {}
cfg.popNumber = {}
  
for cellName in sorted(cfg.gid_list.keys()):

    if 'cADpyr' in cellName:
        cfg.Epops.append(cellName)
    else:
        cfg.Ipops.append(cellName)  

    cfg.cellNumber[cellName] = 50
    cfg.popLabel[cellName] = cellName # No cell diversity
    cfg.popNumber[cellName] = 50

#------------------------------------------------------------------------------
# Run parameters
#------------------------------------------------------------------------------
cfg.duration = 0.40*1e3 ## Duration of the sim, in ms  
cfg.dt = 0.025
cfg.seeds = {'cell': 4321, 'conn': 4321, 'stim': 1000, 'loc': 4321} 
cfg.hParams = {'celsius': 34, 'v_init': -84.0}  
cfg.verbose = False
cfg.createNEURONObj = True
cfg.createPyStruct = True  
cfg.cvode_active = False
cfg.cvode_atol = 1e-6
cfg.cache_efficient = True
cfg.printRunTime = 0.1

cfg.includeParamsLabel = False
cfg.printPopAvgRates = True
cfg.checkErrors = False

#--------------------------------------------------------------------------
# Recording 
#--------------------------------------------------------------------------
cfg.allpops = cfg.Epops + cfg.Ipops

cfg.cellsrec = 2
if cfg.cellsrec == 0:  cfg.recordCells = cfg.allpops # record all cells
elif cfg.cellsrec == 1: cfg.recordCells = [(pop,0) for pop in cfg.allpops] # record one cell of each pop
elif cfg.cellsrec == 2: # record one cell of each cellMEtype # need more test!!!
    cfg.recordCells = []
    for popName in cfg.allpops:
        cellNumber = 50
        if cellNumber < 5: 
            for numberME in range(cellNumber):
                cfg.recordCells.append((popName,numberME))
        else:
            numberME = 0
            diference = cellNumber - 5.0*int(cellNumber/5.0)
            
            for number in range(5):            
                cfg.recordCells.append((popName,numberME))
                
                if number < diference:              
                    numberME+=int(np.ceil(cellNumber/5.0))  
                else:
                    numberME+=int(cellNumber/5.0)

cfg.recordTraces = {'V_soma': {'sec':'soma_0', 'loc':0.5, 'var':'v'},
                    # 'V_axon_0': {'sec':'axon_0', 'loc':0.5, 'var':'v'},
                    # 'V_apic_0': {'sec':'apic_0', 'loc':0.5, 'var':'v'},      
                    # 'V_dend_0': {'sec':'dend_0', 'loc':0.5, 'var':'v'},      
                    }
cfg.recordStim = False			
cfg.recordTime = False  		
cfg.recordStep = 0.025       

# cfg.saveLFPPops =  cfg.recordCells 

cfg.recordLFP = [[x, y, 50] for y in [200, 400, 600] for x in [0, 50, 100]] # 

#------------------------------------------------------------------------------
# Saving
#------------------------------------------------------------------------------
cfg.simLabel = 'v1_batch2'       #   + str(cfg.cynradNumber)
cfg.saveFolder = 'data/'+cfg.simLabel
# cfg.filename =                	## Set file output name
cfg.savePickle = True	        	## Save pkl file
cfg.saveJson = False           	## Save json file
cfg.saveDataInclude = ['simData', 'simConfig', 'net', 'netParams'] ## ['simData'] ##  ['simData'] ##, , 'simConfig', 'netParams'
cfg.backupCfgFile = None 		##  
cfg.gatherOnlySimData = False	##  
cfg.saveCellSecs = True			
cfg.saveCellConns = True	

#------------------------------------------------------------------------------
# Analysis and plotting 
# ------------------------------------------------------------------------------
cfg.analysis['plotRaster'] = {'saveFig': True, 'showFig': False, 'orderInverse': True, 'timeRange': [290,320], 'figSize': (18,5), 'popRates': True, 
                              'fontSize':12, 'markerSize':4, 'marker': 'o', 'dpi': 100} 

cfg.analysis['plot2Dnet']   = {'include': cfg.allpops, 'saveFig': True, 'showConns': False, 'figSize': (12,12), 'view': 'xz', 'fontSize':12}   # Plot 2D cells xy

cfg.analysis['plotTraces'] = {'include': cfg.recordCells, 'oneFigPer': 'trace', 'overlay': True, 'timeRange': [290,320], 'ylim': [-100,50], 'saveFig': True, 'showFig': False, 'figSize':(12,12)}

cfg.analysis['plotLFP'] = {'separation': 1.0, 'plots': ['timeSeries', 'spectrogram','PSD'], 'timeRange': [290,320], 'maxFreq': 500, 'saveFig': True, 'showFig': False}

#------------------------------------------------------------------------------  
# Thalamic Cells

cfg.thalamicpops = ['VPM_sTC']
cfg.cellNumber['VPM_sTC'] = 200 # 839

for mtype in cfg.thalamicpops: # No diversity
	metype = mtype
	cfg.popLabel[metype] = mtype
	cfg.popNumber[mtype] = cfg.cellNumber[metype]

## Th->S1
cfg.connect_ThVecStim_S1 = True
cfg.TC_S1 = {}
cfg.TC_S1['VPM_sTC'] = True
cfg.TC_S1_weightE = 0.00015
cfg.TC_S1_weightI = 0.00025

# homogeneous_poisson at 3Hz cos wave and FR~30Hz
cfg.tmin = 300
cfg.tdur = 40
cfg.max_rate = 100.00
cfg.f_osc = 0.01
cfg.bin_size = 0.05
