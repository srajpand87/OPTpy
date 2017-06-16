from os import path, mkdir,curdir
from ..core import Workflow,MPITask 

__all__ = ['RPMNSflow']

class RPMNSflow(Workflow,MPITask):
    def __init__(self,ntask=1,task=1,rename=True,**kwargs):
        """ 
        Arguments
        ---------
        task, ntask : used to split calculation in tasks (optional)
            task is the task index and ntask is the total of tasks.
        rename : logical, optional, flag to rename files at output.
            Default: True

        keyword arguments:
        nval_total : Number of valence bands
        ecut : Kinetic energy cutoff
        nspinor=1 : Number of spinorial components
        kgrid_response : k-points for Tetrahedral integration
        wfn_fname : Name of wavefunction file (Abinit WFK file)
        """
        super(RPMNSflow, self).__init__(**kwargs)

        # Get input variables:
        self.nval_total = kwargs['nval_total']
        self.ecut = kwargs['ecut']
        self.kgrid_response = kwargs['kgrid_response']
        self.kgrid="{}x{}x{}".format(self.kgrid_response[0],self.kgrid_response[1],self.kgrid_response[2])
        self.nspinor = kwargs['nspinor']
        self.dirname = kwargs.pop('dirname','RPMNS')
        self.wfn_fname=kwargs['wfn_fname'][task-1]


        # --- Write run.sh file ---
        # Define variables
        self.runscript.variables={
            'MPIRUN' : self.mpirun_variable,
            'WFK':'WFK',
            'RHO':'.false.',
            'EM':'.true.',
            'PMN':'.true.',
            'RHOMM':'.false.',
            'LPMN':'.false.',
            'LPMM':'.false.',
            'SCCP':'.false.',
            'lSCCP':'.false.',
            'NVAL':"{}".format(self.nval_total)
        }
        # Symbolic links:
        dest = 'WFK'
        self.update_link(self.wfn_fname, dest)
        # Add other lines:
        self.runscript.append("echo $NVAL >.fnval\n")
        # Executable
        self.runscript.append("#Executable")
        self.runscript.append("$MPIRUN rpmns $WFK $RHO $EM $PMN $RHOMM $LPMN $LPMM $SCCP $lSCCP")
        # Rename output files:
        if ( rename ):
            self.runscript.append("cp eigen.d {0}\n".format(self.eigen_fname))
            self.runscript.append("cp pmnhalf.d {0}\n".format(self.pmn_fname))
            self.runscript.append("cp pnn.d {0}\n".format(self.pnn_fname))

    @property
    def eigen_fname(self):
        original = path.realpath(curdir)
        eigen_fname='eigen{0}'.format(self.suffix)
        return path.join(original, eigen_fname) 

    @property
    def pmn_fname(self):
        original = path.realpath(curdir)
        pmn_fname='pmn{0}'.format(self.suffix)
        return path.join(original, pmn_fname) 

    @property
    def pnn_fname(self):
        original = path.realpath(curdir)
        pnn_fname='pnn{0}'.format(self.suffix)
        return path.join(original, pnn_fname) 

    @property
    def suffix(self):
        if ( self.nspinor > 1):
           spin="-spin"
        else:
           spin=""
        suffix="_{0}_{1}{2}".format(self.kgrid,int(self.ecut),spin)
        return suffix
