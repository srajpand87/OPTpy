from os import path, mkdir,curdir
from ..core import Workflow 

__all__ = ['RPMNSflow']

class RPMNSflow(Workflow):
    def __init__(self,**kwargs):
        """ 
        keyword arguments:
        nval_total : Number of valence bands
        ecut : Kinetic energy cutoff
        nspinor=1 : Number of spinorial components
        nkTetra=5 : Number of k-points for Tetrahedral integration
        wfn_fname : Name of wavefunction file (Abinit WFK file)
        """
        super(RPMNSflow, self).__init__(**kwargs)
        self.nval_total = kwargs['nval_total']
        self.nkTetra = kwargs['nkTetra']
        self.ecut = kwargs['ecut']
        self.nspinor = kwargs['nspinor']
        self.dirname = kwargs.pop('dirname','RPMNS')
        self.wfn_fname = kwargs.pop('wfn_fname','../WFN/out_data/odat_WFK')

    def write(self):
        """ Makes RPMNS directory.
    	This runs the RPMNS Tiniba executable"""

#       RPMNS directory:
        main_dir=path.realpath(curdir)
        RPMNSdir=path.join(main_dir,self.dirname)
        if not path.exists(RPMNSdir):
            mkdir(RPMNSdir)

#       RPMNS/run.sh file:
        filename=RPMNSdir+"/run.sh"
        f=open(filename,"w")
        f.write("#!/bin/bash\n\n")
        f.write("Nval=%d\n" % (self.nval_total))
        f.write("echo $Nval >.fnval\n")
        f.write("WFK=WFK\n")
        f.write("ln -nfs %s WFK\n" % (self.wfn_fname))
        f.write("rho='.false.'\n")
        f.write("em='.true.'\n")
        f.write("pmn='.true.'\n")
        f.write("rhomm='.false.'\n")
        f.write("lpmn='.false.'\n")
        f.write("lpmm='.false.'\n")
        f.write("sccp='.false.'\n")
        f.write("lsccp='.false.'\n\n")
        f.write("rpmns $WFK $rho $em $pmn $rhomm $lpmn $lpmm $sccp $lsccp\n")
#       Rename files:
        postfix=""
        if ( self.nspinor == 2 ):
            postfix="-spin"
        f.write("cp eigen.d ../eigen_%s_%s%s\n" 
            %(str(self.nkTetra),str(int(self.ecut)),postfix))
        f.write("cp pmnhalf.d ../pmn_%s_%s%s\n" 
            %(str(self.nkTetra),str(int(self.ecut)),postfix))
        f.write("cp pnn.d ../pnn_%s_%s%s\n" 
            %(str(self.nkTetra),str(int(self.ecut)),postfix))
        f.close()
