from os import path, mkdir,curdir
from ..core import Workflow,Task 

__all__ = ['RPMNSflow']

class RPMNSflow(Workflow,Task):
    def __init__(self,ntask=1,task=1,**kwargs):
        """ 
        Arguments
        ---------
        task, ntask : used to split calculation in tasks (optional)
            task is the task index and ntask is the total of tasks.

        keyword arguments:
        nval_total : Number of valence bands
        ecut : Kinetic energy cutoff
        nspinor=1 : Number of spinorial components
        kgrid_response : k-points for Tetrahedral integration
        wfn_fname : Name of wavefunction file (Abinit WFK file)
        """
        super(RPMNSflow, self).__init__(**kwargs)
        self.nval_total = kwargs['nval_total']
        self.ecut = kwargs['ecut']
        self.kgrid_response = kwargs['kgrid_response']
        self.kgrid="{}x{}x{}".format(self.kgrid_response[0],self.kgrid_response[1],self.kgrid_response[2])
        self.nspinor = kwargs['nspinor']
        self.dirname = kwargs.pop('dirname','RPMNS')
        self.wfn_fname=kwargs['wfn_fname'][task-1]
        print(self.wfn_fname)

        dest = 'WFK'
        self.update_link(self.wfn_fname, dest)

#        f.write("ln -nfs %s WFK\n\n" % (self.wfn_fname))
        self.runscript.append("Nval=%d" % (self.nval_total))
        self.runscript.append("echo $Nval >.fnval")
        self.runscript.append("WFK=WFK")
        self.runscript.append("rho='.false.'")
        self.runscript.append("em='.true.'")
        self.runscript.append("pmn='.true.'")
        self.runscript.append("rhomm='.false.'")
        self.runscript.append("lpmn='.false.'")
        self.runscript.append("lpmm='.false.'")
        self.runscript.append("sccp='.false.'")
        self.runscript.append("lsccp='.false.'\n")
        self.runscript.append("#Executable")
        self.runscript.append("rpmns $WFK $rho $em $pmn $rhomm $lpmn $lpmm $sccp $lsccp\n")
#
#        # Rename output files:
#        postfix=""
#        if ( self.nspinor == 2 ):
#            postfix="-spin"
#        f.write("cp eigen.d ../eigen_{}_{}{}\n"\
#            .format(self.kgrid,int(self.ecut),postfix))
#        f.write("cp pmnhalf.d ../pmn_{}_{}{}\n"\
#            .format(self.kgrid,int(self.ecut),postfix))
#        f.write("cp pnn.d ../pnn_{}_{}{}\n"\
#            .format(self.kgrid,int(self.ecut),postfix))
#        f.close()
