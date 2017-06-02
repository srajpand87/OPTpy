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
            if ( self.nspinor > 1 ):
                postfix="_{0}_{1}-spin".format(self.kgrid,self.ecut)
            else:
                postfix="_{0}_{1}".format(self.kgrid,self.ecut)

            f.write("cp eigen.d ../eigen{0}\n".format(postfix))
            f.write("cp pmnhalf.d ../pmn{0}\n".format(postfix))
            f.write("cp pnn.d ../pnn{0}\n".format(postfix))
            f.close()
