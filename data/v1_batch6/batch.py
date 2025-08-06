"""
batch.py 

Batch simulation for S1 model using NetPyNE

Contributors: salvadordura@gmail.com, fernandodasilvaborges@gmail.com
"""
from netpyne.batch import Batch
from netpyne import specs
import numpy as np

# ----------------------------------------------------------------------------------------------
# Custom
# ----------------------------------------------------------------------------------------------
def custom():
    params = specs.ODict()
    
    params[('seeds', 'stim')] =  [1000]

    b = Batch(params=params, netParamsFile='netParams.py', cfgFile='cfg.py')

    return b

# ----------------------------------------------------------------------------------------------
# Run configurations
# ----------------------------------------------------------------------------------------------
def setRunCfg(b, type='mpi_bulletin'):
    if type=='mpi_bulletin' or type=='mpi':
        b.runCfg = {'type': 'mpi_bulletin', 
            'script': 'init.py', 
            'skip': True}

    elif type=='mpi_direct':
        b.runCfg = {'type': 'mpi_direct',
            'cores': 6,
            'script': 'init.py',
            'mpiCommand': 'mpiexec', # --use-hwthread-cpus
            'skip': True}

    elif type=='mpi_direct2':
        b.runCfg = {'type': 'mpi_direct',
            'mpiCommand': 'mpirun -n 80 ./x86_64/special -mpi -python init.py', # --use-hwthread-cpus
            'skip': True}

    elif type == 'hpc_slurm_Expanse':
        b.runCfg = {'type': 'hpc_slurm',
                    'allocation': 'TG-IBN140002',
                    'partition': 'large-shared',
                    'walltime': '24:00:00',
                    'nodes': 1,
                    'coresPerNode': 128,
                    'email': 'fernandodasilvaborges@gmail.com',
                    'folder': '/home/fborges/S1_opto_Thal/',
                    'script': 'init.py',
                    'mpiCommand': 'mpirun',
                    'custom': '#SBATCH --constraint="lustre"\n#SBATCH --mem=1024G\n#SBATCH --export=ALL\n#SBATCH --partition=large-shared',
                    'skip': True}

    elif type == 'hpc_slurm_jsc':
        b.runCfg = {'type': 'hpc_slurm',
                    'allocation': 'icei-hbp-00000000006',
                    'walltime': '24:00:00',
                    'nodes': 2,
                    'coresPerNode': 128,
                    'email': 'fernandodasilvaborges@gmail.com',
                    'folder': '/p/home/jusers/borges1/jusuf/S1_opto_Thal/',
                    'script': 'init.py',
                    'mpiCommand': 'srun',
                    'custom': '#SBATCH --account=icei-hbp-00000000006',
                    'skip': True}

# ----------------------------------------------------------------------------------------------
# Main code
# ----------------------------------------------------------------------------------------------
if __name__ == '__main__': 
    b = custom() #

    b.batchLabel = 'v1_batch6'  
    # b.saveFolder = '/expanse/lustre/projects/csd403/fborges/'+b.batchLabel
    # b.saveFolder = '/p/project/icei-hbp-00000000006/borges1/'+b.batchLabel
    b.saveFolder = 'data/'+b.batchLabel
    b.method = 'grid'
    setRunCfg(b, 'mpi_direct')
    # setRunCfg(b, 'hpc_slurm_Expanse')
    b.run() # run batch
    
     
