#from OPTpy import abinittask
from os import path, mkdir,chdir
from OPTpy import Structure #..external 
from OPTpy import Workflow #..core
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer 
from numpy import int as np_int
from numpy import array as np_array
from numpy import linalg as np_linalg
from numpy import ones as np_ones

__all__ = ['KKFlow']

class KKflow(Workflow):
    def __init__(self,**kwargs):
        """ 
        keyword arguments:
        structure : pymatgen.Structure
            Structure object containing information on the unit cell.
        """
        super(KKflow, self).__init__(**kwargs)
        self.structure = kwargs['structure']

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
        dirname=path.dirname(path.abspath(__file__))
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
        print lattice
        print acell
#       Write pvectors file

#       KK directory:
        dirname=path.dirname(path.abspath(__file__))
        newdir="KK"
        KKdir=path.join(dirname,newdir)
        if not path.exists(KKdir):
            mkdir(KKdir)

flow = KKflow(
   structure=Structure.from_file('../data/structures/GaAs.json')
)
flow.write()

