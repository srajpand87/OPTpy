#!/bin/bash


MPIRUN='mpirun -n 1 --npernode 1'
ABINIT='abinit'

$MPIRUN $ABINIT < gaas.files &> gaas.log

