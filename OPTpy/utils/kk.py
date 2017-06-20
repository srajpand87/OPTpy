from os import path, mkdir,curdir
from ..external import Structure 
from ..core import Workflow,IOTask 
from numpy import int as np_int
from numpy import array as np_array
from numpy import linalg as np_linalg
from numpy import ones as np_ones

__all__ = ['KKflow']

class KKflow(Workflow,IOTask):
    def __init__(self,**kwargs):
        """ 
        keyword arguments:
        structure : pymatgen.Structure
            Structure object containing information on the unit cell.
        IBZ : executable
        prefix : str, prefix for calculation
        dirname : str, directory name
        kgrid_response : int, array(3), k-point grid for response 
        """
        super(KKflow, self).__init__(**kwargs)
        self.structure = kwargs['structure']
        self.prefix = kwargs['prefix']
        self.dirname = kwargs.pop('dirname','KK')
        self.kgrid_response = kwargs['kgrid_response']
        self.kgrid="{}x{}x{}".format(self.kgrid_response[0],self.kgrid_response[1],self.kgrid_response[2])
        self.ibz=kwargs.pop('IBZ','ibz')

        # --- Write run.sh file ---

        # Define variables:
        self.runscript.variables={
            'IBZ' : self.ibz}
        #
        # Copy files:
        #
        self.update_link(self.pvectors_fname,'pvectors')
        self.update_link(self.symd_fname,'sym.d')

        # Load modules in run script:
        if ( 'modules' in kwargs):
            self.runscript.append(kwargs['modules'])
        #
        # Extra lines:
        #
        self.runscript.append("#Executable")
        self.runscript.append("$IBZ -abinit -tetrahedra -cartesian -symmetries -reduced -mesh\n")
        self.runscript.append("#Rename output files:")

	self.runscript.append("mv kpoints.reciprocal {0}".format(self.kreciprocal_fname))
   	self.runscript.append("mv kpoints.cartesian {0}".format(self.kcartesian_fname))
   	self.runscript.append("mv tetrahedra {0}".format(self.tetrahedra_fname))
   	self.runscript.append("mv Symmetries.Cartesian {0}".format(self.symmetries_fname))
#   	self.runscript.append("cd ..")
#   	self.runscript.append("rm -rf TMP/")



    def write(self):
        """ Makes KK directory.
    	This contains symmetries and lattice parameters"""
        
        super(IOTask, self).write()

        self.get_syms()
        self.write_grid()
          
        
    @property
    def tetrahedra_fname(self):
        original = path.realpath(curdir)
        tetrahedra_fname='symmetries/tetrahedra_{0}'.format(self.kgrid)
        return path.join(original, tetrahedra_fname) 

    @property
    def symmetries_fname(self):
        original = path.realpath(curdir)
        symmetries_fname='symmetries/Symmetries.Cartesian_{0}'.format(self.kgrid)
        return path.join(original, symmetries_fname) 

    @property
    def pvectors_fname(self):
        original = path.realpath(curdir)
        pvectors_fname='symmetries/pvectors'
        return path.join(original, pvectors_fname)
 
    @property
    def symd_fname(self):
        original = path.realpath(curdir)
        symd_fname='symmetries/symd'
        return path.join(original, symd_fname)

    @property
    def kreciprocal_fname(self):
        original = path.realpath(curdir)
        kreciprocal_fname='{0}.klist_{1}'.format(self.prefix,self.kgrid)
        return path.join(original, kreciprocal_fname)

    @property
    def kcartesian_fname(self):
        original = path.realpath(curdir)
        kcartesian_fname='symmetries/{0}.kcartesian_{1}'.format(self.prefix,self.kgrid)
        return path.join(original, kcartesian_fname)
 
    def get_syms(self):
        """ Gets symmetries with Pymatgen""" 
        from pymatgen.symmetry.analyzer import SpacegroupAnalyzer 
        # Gets symmetries with pymatgen:
        symprec=0.1 # symmetry tolerance for the Spacegroup Analyzer
                    #used to generate the symmetry operations
        sga = SpacegroupAnalyzer(self.structure, symprec)
        # ([SymmOp]): List of symmetry operations.
        SymmOp=sga.get_symmetry_operations()
        nsym=len(SymmOp)

        # Symmetries directory:
        # dirname=path.dirname(path.abspath(__file__))
        dirname=path.realpath(curdir)
        newdir="symmetries"
        SYMdir=path.join(dirname,newdir)
        if not path.exists(SYMdir):
            mkdir(SYMdir)

        # symmetries/sym.d file:
        #self.symd_fname=SYMdir+"/sym.d"
        f=open(self.symd_fname,"w")
        f.write("%i\n" % (nsym))
        for isym in range(0,nsym):
            symrel=np_array(SymmOp[isym].rotation_matrix) #rotations
            # Transpose all symmetry matrices
            symrel = np_linalg.inv(symrel.transpose())
            symrel = np_array(symrel,np_int)
            #translation=SymmOp[isym].translation_vector
	    f.write(" ".join(map(str, symrel[0][:]))+" ")
	    f.write(" ".join(map(str, symrel[1][:]))+" ")
            f.write(" ".join(map(str, symrel[2][:]))+"\n")
        f.close()
        # Get lattice parameters
        lattice=self.structure.lattice
        rprim=lattice
        ang2bohr=1.88972613
        acell=np_ones(3)*ang2bohr
        # Write pvectors file
        # symmetries/pvectors file:
#        self.pvectors_fname=SYMdir+"/pvectors"
        f=open(self.pvectors_fname,"w")
        f.write(str(lattice)+"\n")
        f.write(" ".join(map(str, acell[:]))+"\n")
        f.close()

    def write_grid(self):
        """ Writes KK/grid file to define the Tetrahedra k-point grid """
    
        #Write KK/grid file
        filename=self.dirname+"/grid"
        f=open(filename,"w")
        f.write(" ".join(map(str, self.kgrid_response[:]))+"\n")
        f.close()
        #PENDING: need to get rid of this file:
        #Write KK/fort.83
        #0 if 'odd_rank'
        #1 if system was rendered non-centrosymmetric via odd_rank.sh
        #2 normal case
        filename=self.dirname+"/fort.83"
        f=open(filename,"w")
        f.write("2 \n") 
        f.close()
