"""
init.py

Starting script to run NetPyNE-basedS1 model.

Usage:
    python init.py # Run simulation, optionally plot a raster

MPI usage:
    mpiexec -n 4 nrniv -python -mpi init.py

Contributors: salvadordura@gmail.com, fernandodasilvaborges@gmail.com
"""

import matplotlib; matplotlib.use('Agg')  # to avoid graphics error in servers
from netpyne import sim
import pickle, json
import numpy as np

# cfg, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')
cfg, netParams = sim.readCmdLineArgs()

sim.initialize(
    simConfig = cfg, 	
    netParams = netParams)  				# create network object and set cfg and net params
sim.net.createPops()               			# instantiate network populations
sim.net.createCells()              			# instantiate network cells based on defined populations
sim.net.connectCells()            			# create connections between cells based on params
sim.net.addStims() 							# add network stimulation
sim.setupRecording()              			# setup variables to record for each cell (spikes, V traces, etc)
sim.runSim()                      			# run parallel Neuron simulation  
sim.gatherData()                  			# gather spiking data and cell info from each node
sim.saveData()                    			# save params, cell info and sim output to file (pickle,mat,txt,etc)#
sim.analysis.plotData()         			# plot spike raster etc

# Epops = cfg.Epops
# Ipops = cfg.Ipops

# spk_times = sim.simData['spkt']  # Tempos de spikes
# spk_ids = sim.simData['spkid']  # IDs dos neurônios

# print(np.array(list(spk_times)[250::50]) - np.array(list(spk_times)[200:-50:50]))

# sim.analysis.plotRaster(timeRange=[300,320], figSize=(18,5), popRates=True, saveFig=True);

# sim.analysis.plotTraces(include=Ipops, timeRange=[299,320], overlay=True, oneFigPer='trace', figSize=(12,4));
# sim.analysis.plotTraces(include=Epops, timeRange=[299,320], overlay=True, oneFigPer='trace', figSize=(12,4));

# sim.analysis.plotTraces(include = cfg.recordCells, timeRange=[223,323], ylim=[-80,20], saveFig=True, axis=False, overlay=True, oneFigPer='trace', figSize=(15,2.1));
# sim.analysis.plotTraces(timeRange=[290,320], overlay=False, oneFigPer='trace', figSize=(18,36));

# sim.analysis.plotTraces(include= [ii for ii in range(9)], timeRange=[300,320], overlay=False, oneFigPer='trace', figSize=(6,36));
# sim.analysis.plotTraces(timeRange=[290,320], overlay=False, oneFigPer='trace', figSize=(6,18));

# for ii in range(0,15,5):
# sim.analysis.plotShape(includePre= [ii for ii in range(0,300,2)], includePost= [ii for ii in range(0,300,2)], 
#         includeAxon=False, showSyns=False, showElectrodes=False,
#         cvar= 'voltage', dist=0.6, elev=90, azim=-90, 
#         axisLabels=True, synStyle='o', 
#         clim= [-75, -60], showFig=False, synSize=2, saveFig=True, figSize=(8,8))

# sim.analysis.plotLFP(electrodes=[ii for ii in range(len(cfg.recordLFP))], timeRange=[296,322], saveFig=True, plots=['timeSeries'], figSize=(24,12.0))

