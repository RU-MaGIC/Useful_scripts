#!/bin/bash

#SBATCH --partition=p_lemenzad            # Partition (job queue)
#SBATCH --job-name=cool-name          # Assign an short name to your job
#SBATCH --nodes=1                    # Number of nodes you require
#SBATCH --ntasks=1                   # Total # of tasks across all nodes
#SBATCH --cpus-per-task=40            # Cores per task (>1 if multithread tasks)
#SBATCH --mem=192000                   # Real memory (RAM) required (MB)
#SBATCH --time=48:00:00              # Total run time limit (HH:MM:SS)
#SBATCH --output=slurm.%N.%j.out     # STDOUT output file
#SBATCH --error=slurm.%N.%j.err      # STDERR output file (optional)

## Loading modules to use
module load java/11.0.5
module load singularity/3.5.2

## The details for running the actual job
## This example has a nextflow run example- my nextflow executable is in my home directory. 
/home/lemenzad/nextflow run main.nf

## Capture job accounting info (OPTIONAL- but awesome, big thanks to Gallen Collier)
sleep 10
echo ""
sacct --units=G --format=MaxRSS,MaxDiskRead,MaxDiskWrite,Elapsed,NodeList -j $SLURM_JOBID | sed -n -e 1,2p -e 5p
echo ""
echo -n "Fair-share score: ";sshare | grep $USER | grep general | awk '{print $NF}'
echo ""
sleep 2
