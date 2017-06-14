from ..core import Workflow,Task 

__all__ = ['MERGEflow']

class MERGEflow(Workflow,Task):
    def __init__(self,ntask,**kwargs):
        """ 
        Arguments
        ---------
        ntask : int, total of tasks to merge.

        Keyword arguments
        ---------
        dirname : str, directory where the RPMNS calculation is done.
        ecut : Kinetic energy cutoff
        nspinor=1 : Number of spinorial components
        kgrid_response : k-points for Tetrahedral integration

        """
        super(MERGEflow, self).__init__(**kwargs)
        self.dirname = kwargs['dirname']
        self.ecut = kwargs['ecut']
        self.kgrid_response = kwargs['kgrid_response']
        self.nspinor = kwargs.pop('nspinor',1)

        self.get_filenames()

        #Write run.sh file:
        self.runscript.append("eigenfile={0}".format(self.eigenfile))
        self.runscript.append("pmnfile={0}".format(self.pmnfile))
        self.runscript.append("pnnfile={0}".format(self.pnnfile))
        self.runscript.append("")

        # Merge eigenvalue files:
        self.runscript.append("#Merge eigenvalues")
        self.runscript.append("cat 1/eigen.d > tmp")
        for itask in range(1,ntask):
            self.runscript.append("cat {0}/eigen.d >> tmp".format(itask+1))
        self.runscript.append("awk '{$1=\"\"; print NR $0}' tmp > $eigenfile")
            
        # Merge pmn files:
        self.runscript.append("\n#Merge pmn")
        self.runscript.append("cat 1/pmnhalf.d > $pmnfile")
        for itask in range(1,ntask):
            self.runscript.append("cat {0}/pmnhalf.d >> $pmnfile".format(itask+1))
        # Merge pnn files:
        self.runscript.append("\n#Merge pnn")
        self.runscript.append("cat 1/pnn.d > $pnnfile")
        for itask in range(1,ntask):
            self.runscript.append("cat {0}/pnn.d >> $pnnfile".format(itask+1))

    def get_filenames(self):
        """ Get filenames for files to merge """ 
        from os import path, mkdir,curdir
        from os import getcwd

        #Get filenames: 
        kgrid="{}x{}x{}".format(self.kgrid_response[0],self.kgrid_response[1],self.kgrid_response[2])
        cwd=getcwd()
        if ( self.nspinor > 1):
           spin="-spin"
        else:
           spin=""
        sufix="_{0}_{1}{2}".format(kgrid,int(self.ecut),spin)
        #
        eigenfile="eigen"+sufix
        self.eigenfile=path.join(cwd,eigenfile)
        #
        pmnfile="pmn"+sufix
        self.pmnfile=path.join(cwd,pmnfile)
        #
        pnnfile="pnn"+sufix
        self.pnnfile=path.join(cwd,pnnfile)
