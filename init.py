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

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.interpolate import interp1d

excel_file_path = "Spike_trains_steps_L4_elife_Aric.xlsx"

df_rs = pd.read_excel(excel_file_path, sheet_name="RS")
df_fs = pd.read_excel(excel_file_path, sheet_name="FS")
df_rip = pd.read_excel(excel_file_path, sheet_name="Ripplets")
df_rip2 = pd.read_excel(excel_file_path, sheet_name="Ripplets2")

# print("DataFrame for sheet 'RS':")
# print(df_rs.head())
# print("\nDataFrame for sheet 'FS':")
# print(df_fs.head())
# print("\nDataFrame for sheet 'Ripplets':")
# print(df_rip.head())
# print("\nDataFrame for sheet 'Ripplets2':")
# print(df_rip2.head())

# -------------------------------------------------------------------------------- #
# Original time and voltage
t_orig = df_rip2['042021'].values
v_orig = df_rip2['FS 2 ms stim IC'].values

# Create new time array with double the number of points (higher resolution)
t_highres = np.linspace(t_orig[0], t_orig[-1], 4 * len(t_orig) - 1)

# Interpolate using cubic interpolation
interp_func = interp1d(t_orig, v_orig, kind='cubic')
v_highres = interp_func(t_highres)

# -------------------------------------------------------------------------------- #
t_orig2 = df_rip['031820_DFI_P41'].values
v_orig2 = df_rip['FS 5 ms stim'].values

# Create new time array with double the number of points (higher resolution)
t_highres2 = np.linspace(t_orig2[0], t_orig2[-1], 4 * len(t_orig2) - 1)
# Interpolate using cubic interpolation
interp_func2 = interp1d(t_orig2, v_orig2, kind='cubic')
v_highres2 = interp_func2(t_highres2)   

# -------------------------------------------------------------------------------- #
# Original time and voltage
t_orig3 = df_rip2['042021'].values
v_orig3 = df_rip2['RS 2 ms stim IC'].values

# Create new time array with double the number of points (higher resolution)
t_highres3 = np.linspace(t_orig3[0], t_orig3[-1], 4 * len(t_orig3) - 1)
# Interpolate using cubic interpolation
interp_func3 = interp1d(t_orig3, v_orig3, kind='cubic')
v_highres3 = interp_func3(t_highres3)   

# -------------------------------------------------------------------------------- #

t_orig4 = df_rip['102920_DFI_P36'].values
v_orig4 = df_rip['RS 2 ms stim'].values

# Create new time array with double the number of points (higher resolution)
t_highres4 = np.linspace(t_orig4[0], t_orig4[-1], 4 * len(t_orig4) - 1)
# Interpolate using cubic interpolation
interp_func4 = interp1d(t_orig4, v_orig4, kind='cubic')
v_highres4 = interp_func4(t_highres4)       
# -------------------------------------------------------------------------------- #

plt.figure(figsize=(20, 9))

plt.subplot(2, 1, 1)
plt.vlines(x=[2.3, 3.1, 4.0, 5.5, 6.4, 7.7, 8.6, 10.3],ymin=-80, ymax=40, colors='k', linestyles='dotted', linewidth=3,  alpha=0.3)
for cell in sim.simData['V_soma'].keys():
    if 'cell' in cell:   
        try:
            plt.plot(sim.simData['t']-500., sim.simData['V_soma'][cell]-sim.simData['V_soma'][cell][20000]-66.4, linewidth=4, alpha=0.25, label=cell)
        except:
            print(cell) 
            pass
plt.plot(t_highres2-1.2, v_highres2+4-3.7, color='red', linewidth=3, linestyle='--')
plt.plot(t_highres4-0.5, v_highres4+3-3.7, color='blue', linewidth=3, linestyle='--')
plt.plot(t_highres3-1.01, v_highres3+10, color='blue', linewidth=3)
plt.plot(t_highres-1.01, v_highres+3, color='red', linewidth=3)
plt.ylabel('Data Vbar (mV)', size=18)
plt.xlim(0.0, 12)
plt.ylim(-75.0, 40)
plt.xticks([0, 2.3, 3.1, 4.0, 5.5, 6.4, 7.7, 8.6, 10.3, 12], size=18);
plt.xlabel('Latency from light onset (ms)', size=18);
plt.yticks([-20,20], [0,40], size=18);
# plt.ylim(-67., -65.5);
plt.subplot(2, 1, 2)
plt.vlines(x=[2.05, 2.55, 2.75, 3.1, 4.0, 5.5, 6.4, 7.7, 8.6, 10.3],ymin=-80, ymax=40, colors='k', linestyles='dotted', linewidth=3,  alpha=0.3)
for cell in sim.simData['V_soma'].keys():
    if 'cell' in cell:   
        try:
            plt.plot(sim.simData['t']-500., sim.simData['V_soma'][cell]-sim.simData['V_soma'][cell][20000]-66.4, linewidth=4, alpha=0.25, label=cell)
        except:
            print(cell) 
            pass
plt.plot(t_highres2-1.2, v_highres2+4-3.7, color='red', linewidth=3, linestyle='--')
plt.plot(t_highres4-0.5, v_highres4+3-3.7, color='blue', linewidth=3, linestyle='--')
plt.plot(t_highres3-1.01, v_highres3+10, color='blue', linewidth=4)
plt.plot(t_highres-1.01, v_highres+3, color='red', linewidth=4)
plt.ylabel('Data Vbar (mV)', size=18)
plt.xlim(0.0, 4.2)
plt.xticks([0,2.05, 2.55, 2.75, 3.1], size=18);
plt.ylim(-66.75, -61.5);
plt.yticks([-66.4, -65.4],[0,1.0], size=18);
plt.xlabel('Latency from light onset (ms)', size=18);
# plt.legend(fontsize=12)

plt.savefig('Fig_FS_RS_vopt_2ms_stim.png', dpi=300)