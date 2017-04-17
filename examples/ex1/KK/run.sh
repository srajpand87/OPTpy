#!/bin/bash

IBZ=ibz
CASE=gaas

#Copy files
cp ../symmetries/pvectors .
cp ../symmetries/sym.d .

#Executable
$IBZ -abinit -tetrahedra -cartesian -symmetries -reduced -mesh

#Rename output files:
NKPT=`wc kpoints.reciprocal | awk '{print $1}'`

mv kpoints.reciprocal ../$CASE.klist_$NKPT
mv kpoints.cartesian ../symmetries/$CASE.kcartesian_$NKPT
mv tetrahedra ../symmetries/tetrahedra_$NKPT
mv Symmetries.Cartesian ../symmetries/Symmetries.Cartesian_$NKPT
cd ..
rm -rf TMP/