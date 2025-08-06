#!/bin/bash
#SBATCH --job-name=v2_batch4_0
#SBATCH -A TG-IBN140002
#SBATCH -t 24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128
#SBATCH -o /expanse/lustre/projects/csd403/fborges/v2_batch4/v2_batch4_0.run
#SBATCH -e /expanse/lustre/projects/csd403/fborges/v2_batch4/v2_batch4_0.err
#SBATCH --mail-user=fernandodasilvaborges@gmail.com
#SBATCH --mail-type=end

#SBATCH --constraint="lustre"
#SBATCH --mem=128G
#SBATCH --export=ALL
#SBATCH --partition=compute
source ~/.bashrc
cd /home/fborges/S1_opto_Thal/
mpirun -n 128 nrniv -python -mpi init.py simConfig=/expanse/lustre/projects/csd403/fborges/v2_batch4/v2_batch4_0_cfg.json netParams=/expanse/lustre/projects/csd403/fborges/v2_batch4/v2_batch4_netParams.py
wait
    