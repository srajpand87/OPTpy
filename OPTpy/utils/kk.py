from os import path, mkdir,curdir
from ..external import Structure 
from ..core import Workflow 
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer 
from numpy import int as np_int
from numpy import array as np_array
from numpy import linalg as np_linalg
from numpy import ones as np_ones

__all__ = ['KKflow']

class KKflow(Workflow):
    def __init__(self,**kwargs):
        """ 
        keyword arguments:
        structure : pymatgen.Structure
            Structure object containing information on the unit cell.
        """
        super(KKflow, self).__init__(**kwargs)
        self.structure = kwargs['structure']
        self.case = kwargs['case']
        self.grid_response = kwargs['grid_response']

    def write(self):
        """ Makes KK directory.
    	This contains symmetries and lattice parameters"""

#       Gets symmetries with pymatgen:
        symprec=0.1 # symmetry tolerance for the Spacegroup Analyzer
                    #used to generate the symmetry operations
        sga = SpacegroupAnalyzer(self.structure, symprec)
#       ([SymmOp]): List of symmetry operations.
        SymmOp=sga.get_symmetry_operations()
        nsym=len(SymmOp)

#       Symmetries directory:
#        dirname=path.dirname(path.abspath(__file__))
        dirname=path.realpath(curdir)
        newdir="symmetries"
        SYMdir=path.join(dirname,newdir)
        if not path.exists(SYMdir):
            mkdir(SYMdir)

#       symmetries/sym.d file:
        filename=SYMdir+"/sym.d"
        f=open(filename,"w")
        f.write("%i\n" % (nsym))
        for isym in range(0,nsym):
            symrel=np_array(SymmOp[isym].rotation_matrix) #rotations
#           Transpose all symmetry matrices
            symrel = np_linalg.inv(symrel.transpose())
            symrel = np_array(symrel,np_int)
            #translation=SymmOp[isym].translation_vector
	    f.write(" ".join(map(str, symrel[0][:]))+" ")
	    f.write(" ".join(map(str, symrel[1][:]))+" ")
            f.write(" ".join(map(str, symrel[2][:]))+"\n")
        f.close()
#       Get lattice parameters
        lattice=self.structure.lattice
        rprim=lattice
        ang2bohr=1.88972613
        acell=np_ones(3)*ang2bohr
#       Write pvectors file
#       symmetries/pvectors file:
        filename=SYMdir+"/pvectors"
        f=open(filename,"w")
        f.write(str(lattice)+"\n")
        f.write(" ".join(map(str, acell[:]))+"\n")
        f.close()
#       KK directory:
        #dirname=path.dirname(path.abspath(__file__))
        dirname=path.realpath(curdir)
        newdir="KK"
        KKdir=path.join(dirname,newdir)
        if not path.exists(KKdir):
            mkdir(KKdir)
#       Write KK/run.sh file
        filename=KKdir+"/run.sh"
        f=open(filename,"w")
        f.write("#!/bin/bash\n\n")
        f.write("IBZ=ibz\n")
        f.write("CASE="+self.case+"\n\n")
        f.write("#Copy files\n")
	f.write("cp ../symmetries/pvectors .\n")
	f.write("cp ../symmetries/sym.d .\n\n")
        f.write("#Executable\n")
        f.write("$IBZ -abinit -tetrahedra -cartesian -symmetries -reduced -mesh\n\n")
        f.write("#Rename output files:\n")
	f.write("NKPT=`wc kpoints.reciprocal | awk '{print $1}'`\n\n")
	f.write("mv kpoints.reciprocal ../$CASE.klist_$NKPT\n")
   	f.write("mv kpoints.cartesian ../symmetries/$CASE.kcartesian_$NKPT\n")
   	f.write("mv tetrahedra ../symmetries/tetrahedra_$NKPT\n")
   	f.write("mv Symmetries.Cartesian ../symmetries/Symmetries.Cartesian_$NKPT\n")
   	f.write("cd ..\n")
   	f.write("rm -rf TMP/")
        f.close()
#       Write KK/grid file
        filename=KKdir+"/grid"
        f=open(filename,"w")
        f.write(" ".join(map(str, self.grid_response[:]))+"\n")
        f.close()
#       PENDING: need to get rid of this file:
#       Write KK/fort.83
#       0 if 'odd_rank'
#       1 if system was rendered non-centrosymmetric via odd_rank.sh
#       2 normal case
        filename=KKdir+"/fort.83"
        f=open(filename,"w")
        f.write("2 \n") 
        f.close()
        

        
