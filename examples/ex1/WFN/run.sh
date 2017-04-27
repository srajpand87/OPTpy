#!/bin/bash


MPIRUN='mpirun -n 1 --npernode 1'
ABINIT='abinit'

ln -nfs ../../SCF/out_data/odat_DEN input_data/idat_DEN

$MPIRUN $ABINIT < gaas.files &> gaas.log

