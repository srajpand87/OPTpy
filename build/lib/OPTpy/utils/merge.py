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

        self.get_filenames(**kwargs)

        #Write run.sh file:
        self.runscript.append("eigen_fname={0}".format(self.eigen_fname))
        self.runscript.append("pmn_fname={0}".format(self.pmn_fname))
        self.runscript.append("pnn_fname={0}".format(self.pnn_fname))
        self.runscript.append("")

        # Merge eigenvalue files:
        self.runscript.append("#Merge eigenvalues")
        self.runscript.append("cat 1/eigen.d > tmp")
        for itask in range(1,ntask):
            self.runscript.append("cat {0}/eigen.d >> tmp".format(itask+1))
        self.runscript.append("awk '{$1=\"\"; print NR $0}' tmp > $eigen_fname")
            
        # Merge pmn files:
        self.runscript.append("\n#Merge pmn")
        self.runscript.append("cat 1/pmnhalf.d > $pmn_fname")
        for itask in range(1,ntask):
            self.runscript.append("cat {0}/pmnhalf.d >> $pmn_fname".format(itask+1))
        # Merge pnn files:
        self.runscript.append("\n#Merge pnn")
        self.runscript.append("cat 1/pnn.d > $pnn_fname")
        for itask in range(1,ntask):
            self.runscript.append("cat {0}/pnn.d >> $pnn_fname".format(itask+1))

    def get_filenames(self,**kwargs):
        """ Get filenames for files to merge """ 
        from os import path, mkdir,curdir
        from os import getcwd

        #Get filenames: 
        self.eigen_fname=kwargs['eigen_fname']
        self.pmn_fname=kwargs['pmn_fname']
        self.pnn_fname=kwargs['pnn_fname']
