#!/bin/bash -l
#
# CP2K on Piz Daint
#SBATCH -A s957
#SBATCH --job-name=df
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=12
#SBATCH --cpus-per-task=1
#SBATCH --partition=normal
#SBATCH --constraint=gpu


#========================================
# load modules and run simulation
module load daint-gpu

export CRAY_CUDA_MPS=1
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
ulimit -s unlimited

srun -n $SLURM_NTASKS  lmp_df < in.df &> lmplog &

wait

for a  in `seq 1 12`; do
 nline=$(echo "($a-1)*32009*8334+1" | bc); echo $nline; 
tail -n +$nline df.lammpstrj | head -n 266763010 > df.lammpstrj-part-$a &
wait
done

wait

sbatch ../analyze.run

sleep 1

