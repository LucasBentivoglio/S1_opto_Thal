"""
netParams.py

High-level specifications for S1-thalamus network model using NetPyNE

Contributors: salvadordura@gmail.com, fernandodasilvaborges@gmail.com
"""

from netpyne import specs
import pickle, json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

netParams = specs.NetParams()   # object of class NetParams to store the network parameters

try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import cfg

#------------------------------------------------------------------------------
#
# NETWORK PARAMETERS
#
#------------------------------------------------------------------------------
for cellName in cfg.gid_list.keys():
        
        gid = cfg.gid_list[cellName]
        MorphoName = cfg.Morpholist[str(gid)]
        hocName = cfg.hoclist[str(gid)]
        MorphologyPath = 'O1_data_physiology/morphologies/ascii'        
        
        print(cellName,hocName)
            
        cellRule = netParams.importCellParams(label=cellName, somaAtOrigin=True,
            conds={'cellType': cellName, 'cellModel': 'HH_full'},
            fileName='O1_data_physiology/emodels_hoc/' + hocName + '.hoc',
            cellName=hocName,
            cellInstance = False,
            cellArgs=[gid, MorphologyPath, MorphoName])
        

        axon_pt3d_x, axon_pt3d_y, axon_pt3d_z, soma_pt3d_diam =  netParams.cellParams[cellName]['secs']['soma_0']['geom']['pt3d'][-1]

        if cellName in cfg.Ipops:
            netParams.cellParams[cellName]['secs']['axon_0']['geom']['diam'] = 2.0
        else:
            netParams.cellParams[cellName]['secs']['axon_0']['geom']['diam'] = 1.0
        # netParams.cellParams[cellName]['secs']['axon_0']['geom']['L'] = 30.0

        axon_pt3d_diam =  netParams.cellParams[cellName]['secs']['axon_0']['geom']['diam']
        axon_pt3d_L =  netParams.cellParams[cellName]['secs']['axon_0']['geom']['L']

        netParams.cellParams[cellName]['secs']['axon_0']['geom']['pt3d'] = [(axon_pt3d_x, axon_pt3d_y, axon_pt3d_z, axon_pt3d_diam),
                                                                                    (axon_pt3d_x, axon_pt3d_y+axon_pt3d_L/2.0, axon_pt3d_z, axon_pt3d_diam),
                                                                                    (axon_pt3d_x, axon_pt3d_y+axon_pt3d_L, axon_pt3d_z, axon_pt3d_diam)]


        axon1_pt3d_x, axon1_pt3d_y, axon1_pt3d_z, axon_0_pt3d_diam =  netParams.cellParams[cellName]['secs']['axon_0']['geom']['pt3d'][-1]

        # netParams.cellParams[cellName]['secs']['axon_1']['geom']['diam'] = 0.5
        # netParams.cellParams[cellName]['secs']['axon_1']['geom']['L'] = 30.0

        axon1_pt3d_diam =  netParams.cellParams[cellName]['secs']['axon_1']['geom']['diam']
        axon1_pt3d_L =  netParams.cellParams[cellName]['secs']['axon_1']['geom']['L']

        netParams.cellParams[cellName]['secs']['axon_1']['geom']['pt3d'] = [(axon1_pt3d_x, axon1_pt3d_y, axon1_pt3d_z, axon1_pt3d_diam),
                                                                                    (axon1_pt3d_x, axon1_pt3d_y+axon1_pt3d_L/2.0, axon1_pt3d_z, axon1_pt3d_diam),
                                                                                    (axon1_pt3d_x, axon1_pt3d_y+axon1_pt3d_L, axon1_pt3d_z, axon1_pt3d_diam)] 

                    
        myelin_pt3d_x, myelin_pt3d_y, myelin_pt3d_z, axon_1_pt3d_diam =  netParams.cellParams[cellName]['secs']['axon_1']['geom']['pt3d'][-1]

        # netParams.cellParams[cellName]['secs']['myelin_0']['geom']['diam'] = 0.5
        netParams.cellParams[cellName]['secs']['myelin_0']['geom']['L'] = 100.0

        myelin_pt3d_diam =  netParams.cellParams[cellName]['secs']['myelin_0']['geom']['diam']
        myelin_pt3d_L =  netParams.cellParams[cellName]['secs']['myelin_0']['geom']['L']

        netParams.cellParams[cellName]['secs']['myelin_0']['geom']['pt3d'] = [(myelin_pt3d_x, myelin_pt3d_y, myelin_pt3d_z, myelin_pt3d_diam),
                                                                                    (myelin_pt3d_x, myelin_pt3d_y+myelin_pt3d_L/2.0, myelin_pt3d_z, myelin_pt3d_diam),
                                                                                    (myelin_pt3d_x, myelin_pt3d_y+myelin_pt3d_L, myelin_pt3d_z, myelin_pt3d_diam)] 


# https://github.com/suny-downstate-medical-center/S1_mouse
# Layer	     height	  from	  to
# L1         0.089      0.000	0.089
# L2         0.070      0.089	0.159
# L3         0.128      0.159	0.286
# L4         0.134      0.286	0.421
# L5         0.263      0.421	0.684
# L6         0.316      0.684	1.000			 
# L23        0.198      0.089	0.286
# All     1378.8 um

layer = {'1':[0.0, 0.089], '2': [0.089,0.159], '3': [0.159,0.309], '23': [0.089,0.309], '4':[0.309,0.418], '5': [0.418,0.684], '6': [0.684,1.0], 
'longS1': [2.2,2.3], 'longS2': [2.3,2.4]}  # normalized layer boundaries

#Th pop
ymin={'ss_RTN_o': 1688, 'ss_RTN_m': 1766, 'ss_RTN_i': 1844, 'VPL_sTC': 2000, 'VPM_sTC': 2156, 'POm_sTC_s1': 2312}
ymax={'ss_RTN_o': 1766, 'ss_RTN_m': 1844, 'ss_RTN_i': 2000, 'VPL_sTC': 2156, 'VPM_sTC': 2312, 'POm_sTC_s1': 2624}

#------------------------------------------------------------------------------
# General network parameters
#------------------------------------------------------------------------------
netParams.scale = 1.0 # Scale factor for number of cells
netParams.sizeX = 300.0 # x-dimension (horizontal length) size in um
netParams.sizeY = 2080.0 # y-dimension (vertical height or cortical depth) size in um
netParams.sizeZ = 300.0 # z-dimension (horizontal depth) size in um
netParams.shape = 'cylinder' # cylindrical (column-like) volume
netParams.rotateCellsRandomly = True
   
netParams.defaultThreshold = -20.0 # spike threshold, 10 mV is NetCon default, lower it for all cells
# netParams.defaultDelay = 0.1 # default conn delay (ms)
netParams.propVelocity = 300.0 #  300 μm/ms (Stuart et al., 1997)
netParams.scaleConnWeightNetStims = 0.001  # weight conversion factor (from nS to uS)
    
#------------------------------------------------------------------------------
# S1 pop
#------------------------------------------------------------------------------
for cellName in netParams.cellParams.keys():        
    layernumber = cellName[1:2]
    if layernumber == '2':
        netParams.popParams[cellName] = {'cellType': cellName, 'cellModel': 'HH_full', 'ynormRange': layer['23'],  'numCells':cfg.cellNumber[cellName]}
    else:
        netParams.popParams[cellName] = {'cellType': cellName, 'cellModel': 'HH_full', 'ynormRange': layer[layernumber], 'numCells': cfg.cellNumber[cellName]}

#------------------------------------------------------------------------------
# Syn
#------------------------------------------------------------------------------

netParams.synMechParams['E->E'] = {'mod': 'DetAMPANMDA','Dep': 700.568,'Fac': 17.989,'Use': 0.327,'tau_d_AMPA': 1.74,'NMDA_ratio':0.8}      
netParams.synMechParams['E->I'] = {'mod': 'DetAMPANMDA','Dep': 700.568,'Fac': 17.989,'Use': 0.327,'tau_d_AMPA': 1.74,'NMDA_ratio':0.8}            
netParams.synMechParams['I->I'] = {'mod': 'DetGABAAB','Dep': 775.316,'Fac': 9.435,'Use': 0.109,'tau_d_GABAA': 7.487,'GABAB_ratio':0.0}
netParams.synMechParams['I->E'] = {'mod': 'DetGABAAB','Dep': 606.433,'Fac': 24.743,'Use': 0.0913,'tau_d_GABAA': 7.192,'GABAB_ratio':0.0}


netParams.connParams['I->E'] = { 
                        'preConds': {'pop': cfg.Ipops},
                        'postConds': {'pop': [ 'L4_SSC_cADpyr_4']},
                        'convergence': 600,
                        'synsPerConn': 20,     
                        'sec': 'basal',                  # target postsyn section
                        'synMech': 'I->E',              # target synaptic mechanism
                        'weight': 2.5,                 # synaptic weight 
                        'delay': 1.0,                 # synaptic delay 
                        }    

netParams.connParams['I->E_B'] = { 
                        'preConds': {'pop': cfg.Ipops},
                        'postConds': {'pop': ['L4_SSC_cADpyr_3', 'L4_UPC_cADpyr_5', 'L4_UPC_cADpyr_6']},
                        'convergence': 600,
                        'synsPerConn': 20,     
                        'sec': 'basal',                  # target postsyn section
                        'synMech': 'I->E',              # target synaptic mechanism
                        'weight': 2.5,                 # synaptic weight 
                        'delay': 1.0,                 # synaptic delay 
                        }    

netParams.connParams['E->E'] = { 
                        'preConds': {'pop': ['L4_UPC_cADpyr_5']},
                        'postConds': {'pop': ['L4_SSC_cADpyr_4']},
                        'convergence': 300,
                        'synsPerConn': 10,     
                        'sec': 'basal',                  # target postsyn section
                        'synMech': 'E->E',              # target synaptic mechanism
                        'weight': 1.75,                 # synaptic weight 
                        'delay': 1.0,                 # synaptic delay 
                        } 

netParams.connParams['E->E_B'] = { 
                        'preConds': {'pop': ['L4_SSC_cADpyr_4']},
                        'postConds': {'pop': ['L4_SSC_cADpyr_3', 'L4_UPC_cADpyr_6']},
                        'convergence': 300,
                        'synsPerConn': 10,     
                        'sec': 'basal',                  # target postsyn section
                        'synMech': 'E->E',              # target synaptic mechanism
                        'weight': 1.0,                 # synaptic weight 
                        'delay': 1.0,                 # synaptic delay 
                        } 

netParams.connParams['E->E_C'] = { 
                        'preConds': {'pop': ['L4_SSC_cADpyr_3', 'L4_UPC_cADpyr_6']},
                        'postConds': {'pop': ['L4_UPC_cADpyr_5']},
                        'convergence': 300,
                        'synsPerConn': 10,     
                        'sec': 'basal',                  # target postsyn section
                        'synMech': 'E->E',              # target synaptic mechanism
                        'weight': 1.5,                 # synaptic weight 
                        'delay': 1.0,                 # synaptic delay 
                        } 

netParams.connParams['E->I'] = { 
                        'preConds': {'pop': ['L4_UPC_cADpyr_5']},
                        'postConds': {'pop': cfg.Ipops},
                        'convergence': 500,
                        'synsPerConn': 10,
                        'sec': 'somatic',                  # target postsyn section
                        'synMech': 'E->I',              # target synaptic mechanism
                        'weight': 1.0,                 # synaptic weight 
                        'delay': 1.0,                 # synaptic delay 
                        }    

netParams.connParams['E->I_B'] = { 
                        'preConds': {'pop': ['L4_SSC_cADpyr_3', 'L4_SSC_cADpyr_4', 'L4_UPC_cADpyr_6']},
                        'postConds': {'pop': cfg.Ipops},
                        'convergence': 500,
                        'synsPerConn': 10,
                        'sec': 'somatic',                  # target postsyn section
                        'synMech': 'E->I',              # target synaptic mechanism
                        'weight': 0.75,                 # synaptic weight 
                        'delay': 1.0,                 # synaptic delay 
                        }   

netParams.connParams['I->I'] = { 
                        'preConds': {'pop': cfg.Ipops},
                        'postConds': {'pop': cfg.Ipops},
                        'convergence': 30,
                        'synsPerConn': 5,
                        'sec': 'basal',                  # target postsyn section
                        'synMech': 'I->I',              # target synaptic mechanism
                        'weight': 0.25,                 # synaptic weight 
                        'delay': 1.0,                 # synaptic delay 
                        }  
#------------------------------------------------------------------------------
# ThVecStim->S1 connectivity parameters
#------------------------------------------------------------------------------
# Th
# # J. Neurosci., June 29, 2016 • 36(26):6906 – 6916
# thalamocortical uEPSPs had several-fold larger amplitudes and faster kinetics in FS interneurons compared with excitatory neurons
# amplitude, 1.8 –13.8 vs 0.4 – 0.9 mV; 
# rise time, 0.4 – 0.8 vs 1.3–2.8 ms; 
# decay time constant, 6 –12 vs 17–36 ms
netParams.synMechParams['NMDA_Th']             = {'mod': 'MyExp2SynNMDABB',    'tau1NMDA': 15, 'tau2NMDA': 150,                'e': 0}
netParams.synMechParams['AMPA_Th']             = {'mod': 'MyExp2SynBB',        'tau1': 0.05,   'tau2': 5.3, 'e': 0}
ESynMech_Th = ['AMPA_Th', 'NMDA_Th']


# create 1 vectstim pop per cell gid
for metype in cfg.thalamicpops: # metype
    np.random.seed(1)
    gaussian = np.random.normal(2.3, 0.07, cfg.cellNumber[metype])
    cellsList = []            
    for cellLabel in range(cfg.cellNumber[metype]): # all cells in metype

        spike_times = (np.array(gaussian[cellLabel:cellLabel+1]) + 10.0, np.array(gaussian[cellLabel:cellLabel+1]) + cfg.Th_stimStart) 
        # spike_times = np.array(gaussian[cellLabel:cellLabel+1]) + cfg.Th_stimStart # light onset at 500 ms
        cellsList.append({'cellLabel': cellLabel, 'spkTimes': list(spike_times[1:2])})
        # print(cellLabel, spike_times[:2])
        
    if np.size(cellsList) > 0:
        netParams.popParams[metype] = {'cellModel': 'VecStim', 'cellsList': cellsList}        

# print(cellsList)

if cfg.connect_ThVecStim_S1:

    ## Connectivity rules
    synapsesperconnection_Th_S1 = 9.0
    for pre in ['VPM_sTC']:  #  
        if cfg.TC_S1[pre]:

            for post in cfg.Ipops: 
                
                conn_convergence = np.ceil(350/synapsesperconnection_Th_S1)

                netParams.connParams['thal_'+pre+'_'+post] = { 
                    'preConds': {'pop': pre},  ####################################################
                    'postConds': {'pop': post},
                    'weight': cfg.TC_S1_weight[post],   # synaptic weight 
                    'sec': list(cfg.sections_soma[post]), # target postsyn section
                    'delay': 0.4,
                    'synsPerConn': int(synapsesperconnection_Th_S1),                     
                    'synMech': ESynMech_Th}  

                netParams.connParams['thal_'+pre+'_'+post]['convergence'] = conn_convergence 
                # netParams.connParams['thal_'+pre+'_'+post]['convergence'] = 1 

            for post in cfg.Epops: 
                
                if 'L4_SS' in post:
                    conn_convergence = np.ceil(500/synapsesperconnection_Th_S1)
                else:
                    conn_convergence = np.ceil(450/synapsesperconnection_Th_S1)

                netParams.connParams['thal_'+pre+'_'+post] = { 
                    'preConds': {'pop': pre},  ####################################################
                    'postConds': {'pop': post},
                    'weight': cfg.TC_S1_weight[post],   # synaptic weight 
                    'sec': list(cfg.sections_dend[post]), #['basal', 'apical'], # target postsyn section
                    'delay': 0.6,
                    'synsPerConn': int(synapsesperconnection_Th_S1),                     
                    'synMech': ESynMech_Th}  

                netParams.connParams['thal_'+pre+'_'+post]['convergence'] = conn_convergence 
                # netParams.connParams['thal_'+pre+'_'+post]['convergence'] = 1

#------------------------------------------------------------------------------
# NetStim inputs to simulate Spontaneous synapses + background in S1 neurons - data from Rat
#------------------------------------------------------------------------------
# Spont and BG
netParams.synMechParams['AMPA'] = {'mod':'MyExp2SynBB', 'tau1': 0.2, 'tau2': 1.74, 'e': 0}
netParams.synMechParams['NMDA'] = {'mod': 'MyExp2SynNMDABB', 'tau1NMDA': 0.29, 'tau2NMDA': 43, 'e': 0}
netParams.synMechParams['GABAA'] = {'mod':'MyExp2SynBB', 'tau1': 0.2, 'tau2': 8.3, 'e': -80}
netParams.synMechParams['GABAB'] = {'mod':'MyExp2SynBB', 'tau1': 3.5, 'tau2': 260.9, 'e': -93} 
ESynMech = ['AMPA', 'NMDA']
ISynMech = ['GABAA', 'GABAB']

cfg.addStimSynS1 = True
cfg.rateStimI = 5.0 # Hz
cfg.rateStimE = 2.0
SourcesNumber = 10 # for each post Mtype - sec distribution

if cfg.addStimSynS1:      
    for post in cfg.Ipops + cfg.Epops:

        synperNeuron = 100
        ratespontaneous = cfg.rateStimI
        for qSnum in range(SourcesNumber):
            ratesdifferentiation = (0.8 + 0.4*qSnum/(SourcesNumber-1)) * (synperNeuron*ratespontaneous)/SourcesNumber
            netParams.stimSourceParams['StimSynS1_S_all_INH->' + post + '_' + str(qSnum)] = {'type': 'NetStim', 'rate': ratesdifferentiation, 'noise': 1.0}

        synperNeuron = 100
        ratespontaneous = cfg.rateStimE
        for qSnum in range(SourcesNumber):
            ratesdifferentiation = (0.8 + 0.4*qSnum/(SourcesNumber-1)) * (synperNeuron*ratespontaneous)/SourcesNumber
            netParams.stimSourceParams['StimSynS1_S_all_EXC->' + post + '_' + str(qSnum)] = {'type': 'NetStim', 'rate': ratesdifferentiation, 'noise': 1.0}
            
    #------------------------------------------------------------------------------
    for post in cfg.Epops+cfg.Ipops:
        for qSnum in range(SourcesNumber):
            netParams.stimTargetParams['StimSynS1_T_all_EXC->' + post + '_' + str(qSnum)] = {
                'source': 'StimSynS1_S_all_EXC->' + post + '_' + str(qSnum), 
                'synMech': 'AMPA', 
                'conds': {'cellType': post}, 
                'sec': 'all', 
                'weight': 0.5,
                'delay': 0.5}

    for post in cfg.Epops+cfg.Ipops:
        for qSnum in range(SourcesNumber):
            netParams.stimTargetParams['StimSynS1_T_all_INH->' + post + '_' + str(qSnum)] = {
                'source': 'StimSynS1_S_all_INH->' + post + '_' + str(qSnum), 
                'conds': {'cellType': post}, 
                'synMech': 'GABAA', 
                'sec': 'all', 
                'weight': 0.5,
                'delay': 0.5}


print(netParams.connParams.keys())

# #------------------------------------------------------------------------------
# # Description
# #------------------------------------------------------------------------------