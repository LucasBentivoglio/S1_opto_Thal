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
            'cores': 12,
            'script': 'init.py',
            'mpiCommand': 'mpiexec', # --use-hwthread-cpus
            'skip': True}

    elif type=='mpi_direct2':
        b.runCfg = {'type': 'mpi_direct',
            'mpiCommand': 'mpirun -n 80 ./x86_64/special -mpi -python init.py', # --use-hwthread-cpus
            'skip': True}

    elif type == 'hpc_slurm_Expanse':
        b.runCfg = {'type': 'hpc_slurm',
                    'allocation': 'TG-MED240050',
                    'partition': 'compute',
                    'walltime': '24:00:00',
                    'nodes': 1,
                    'coresPerNode': 128,
                    'email': 'lucas16edu@gmail.com',
                    'folder': '/home/lbentivoglio/CA1_Model_Teste/',
                    'script': 'init.py',
                    'mpiCommand': 'mpirun',
                    'custom': '#SBATCH --mem=128G\n#SBATCH --export=ALL\n#SBATCH --partition=compute',
                    'skip': False}

    elif type == 'hpc_slurm_jsc':
        b.runCfg = {'type': 'hpc_slurm',
                    'allocation': 'TG-MED240050',
                    'walltime': '24:00:00',
                    'nodes': 1,
                    'coresPerNode': 128,
                    'email': 'lucas16edu@gmail.com',
                    'folder': '/home/lbentivoglio/S1_opto_Thal/',
                    'script': 'init.py',
                    'mpiCommand': 'srun',
                    'custom': '#SBATCH --account=icei-hbp-00000000006',
                    'skip': True}
# ----------------------------------------------------------------------------------------------
# Main code
# ----------------------------------------------------------------------------------------------
if __name__ == '__main__': 
    b = custom() #

    b.batchLabel = 'v3_batch1'  
    b.saveFolder = 'data/'+b.batchLabel
    b.method = 'grid'
    setRunCfg(b, 'hpc_slurm_Expanse')
    b.run() # run batch
    
     
