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

cells_info = json.load(f) 

# print(Lista)

cfg.hoclist = cells_info["hoclist"]
cfg.Morpholist = cells_info["Morpholist"]
cfg.gid_list = cells_info["gid_list"]

# assign variables (use empty dicts as fallback)
cfg.sections_dend = cells_info.get("sections_dend", {})
cfg.sections_soma = cells_info.get("sections_soma", {})

print(f"Loaded sections_dend: {len(cfg.sections_dend)} entries, sections_soma: {len(cfg.sections_soma)} entries")

cfg.Epops = []
cfg.Ipops = []
     
cfg.cellNumber = {}
cfg.popLabel = {}
cfg.popNumber = {}

cfg.cellNumber['L4_BP_cNAC_0'] = 5
cfg.cellNumber['L4_BTC_cNAC_1'] = 5
cfg.cellNumber['L4_NBC_cNAC_2'] = 5
cfg.cellNumber['L4_SSC_cADpyr_3'] = 25
cfg.cellNumber['L4_SSC_cADpyr_4'] = 50
cfg.cellNumber['L4_UPC_cADpyr_5'] = 50
cfg.cellNumber['L4_UPC_cADpyr_6'] = 25

for cellName in sorted(cfg.gid_list.keys()):

    if 'cADpyr' in cellName:
        cfg.Epops.append(cellName)
    else:
        cfg.Ipops.append(cellName)  

    cfg.popLabel[cellName] = cellName # No cell diversity in NetPyNE
    cfg.popNumber[cellName] = cfg.cellNumber[cellName] 


print(cfg.cellNumber)
print(cfg.popNumber)

#------------------------------------------------------------------------------
# Run parameters
#------------------------------------------------------------------------------
cfg.duration = 0.60*1e3 ## Duration of the sim, in ms  
cfg.dt = 0.025
cfg.seeds = {'cell': 1234, 'conn': 1234, 'stim': 1234, 'loc': 1234} 
cfg.hParams = {'celsius': 34, 'v_init': -74.0}  
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
cfg.allpops = cfg.Ipops + cfg.Epops  # all pops

cfg.cellsrec = 0
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
cfg.recordTime = True  		
cfg.recordStep = 0.025 

# cfg.saveLFPPops =  cfg.recordCells 

# cfg.recordLFP = [[x, y, 500] for y in [750] for x in [150]] # 
cfg.recordLFP = [[x, y, 500] for y in [700, 750, 800] for x in [100, 150, 200]] # 

#------------------------------------------------------------------------------
# Saving
#------------------------------------------------------------------------------
cfg.simLabel = 'v1_batch0'       #   + str(cfg.cynradNumber)
cfg.saveFolder = 'data/'+cfg.simLabel
# cfg.filename =                	## Set file output name
cfg.savePickle = False	        	## Save pkl file
cfg.saveJson = False           	## Save json file
cfg.saveDataInclude = ['simData', 'simConfig', 'net', 'netParams'] ## ['simData'] ##  ['simData'] ##, , 'simConfig', 'netParams'
cfg.backupCfgFile = None 		##  
cfg.gatherOnlySimData = False	##  
cfg.saveCellSecs = True			
cfg.saveCellConns = True	

#------------------------------------------------------------------------------
# Analysis and plotting 
# ------------------------------------------------------------------------------
cfg.analysis['plotRaster'] = {'include': cfg.allpops, 'saveFig': True, 'showFig': False, 'orderInverse': True, 'timeRange': [500,515], 'figSize': (18,5), 'popRates': True, 
                              'fontSize':12, 'markerSize':4, 'marker': 'o', 'dpi': 100} 

cfg.analysis['plot2Dnet']   = {'include': cfg.allpops, 'saveFig': True, 'showConns': False, 'figSize': (12,12), 'view': 'xy', 'fontSize':12}   # Plot 2D cells xy

cfg.analysis['plotTraces'] = {'include': cfg.recordCells, 'oneFigPer': 'trace', 'overlay': True, 'timeRange': [500,515], 'ylim': [-100,50], 'saveFig': True, 'showFig': False, 'figSize':(18,5)}

cfg.analysis['plotLFP'] = {'separation': 1.0, 'plots': ['timeSeries', 'locations','spectrogram'], 'timeRange': [500,515], 'maxFreq': 500, 'saveFig': True, 'showFig': False}

#------------------------------------------------------------------------------  
# Thalamic Cells
cfg.thalamicpops = ['VPM_sTC']
cfg.cellNumber['VPM_sTC'] = 800

for mtype in cfg.thalamicpops: # No diversity
	metype = mtype
	cfg.popLabel[metype] = mtype
	cfg.popNumber[mtype] = cfg.cellNumber[metype]

## Th->S1
cfg.connect_ThVecStim_S1 = True
cfg.TC_S1 = {}
cfg.TC_S1['VPM_sTC'] = True
cfg.TC_S1_weight = {}
cfg.TC_S1_weight['L4_BP_cNAC_0'] = 0.0002
cfg.TC_S1_weight['L4_BTC_cNAC_1'] = 0.0002
cfg.TC_S1_weight['L4_NBC_cNAC_2'] = 0.0002
cfg.TC_S1_weight['L4_SSC_cADpyr_3'] = 0.00001
cfg.TC_S1_weight['L4_SSC_cADpyr_4'] = 0.00005
cfg.TC_S1_weight['L4_UPC_cADpyr_5'] = 0.0003
cfg.TC_S1_weight['L4_UPC_cADpyr_6'] = 0.00001

# light onset at 500 ms
cfg.Th_stimStart = 500.0
