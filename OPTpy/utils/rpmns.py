from os import path, mkdir,curdir
from ..core import Workflow 

__all__ = ['RPMNSflow']

class RPMNSflow(Workflow):
    def __init__(self,**kwargs):
        """ 
        keyword arguments:
        nval : Number of valence bands
        ecut : Kinetic energy cutoff
        nspinor=1 : Number of spinorial components
        nkTetra=5 : Number of k-points for Tetrahedral integration
        """
        super(RPMNSflow, self).__init__(**kwargs)
        self.nval = kwargs['nval']
        self.nkTetra = kwargs['nkTetra']
        self.ecut = kwargs['ecut']
        self.nspinor= kwargs['nspinor']

    def write(self):
        """ Makes RPMNS directory.
    	This runs the RPMNS Tiniba executable"""

#       RPMNS directory:
        dirname=path.realpath(curdir)
        newdir="RPMNS"
        RPMNSdir=path.join(dirname,newdir)
        if not path.exists(RPMNSdir):
            mkdir(RPMNSdir)

#       RPMNS/run.sh file:
        filename=RPMNSdir+"/run.sh"
        f=open(filename,"w")
        f.write("#!/bin/bash\n\n")
        f.write("Nval=%d\n" % (self.nval))
        f.write("echo $Nval >.fnval\n")
        f.write("WFK=WFK\n")
        f.write("ln -nfs ../WFN/out_data/odat_WFK WFK\n")
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
        f.write("cp eigen.d ../eigen_%s_%s %s\n" 
            %(str(self.nkTetra),str(int(self.ecut)),postfix))
        f.write("cp pmnhalf.d ../pmn_%s_%s %s\n" 
            %(str(self.nkTetra),str(int(self.ecut)),postfix))
        f.write("cp pnn.d ../pnn_%s_%s %s\n" 
            %(str(self.nkTetra),str(int(self.ecut)),postfix))
        f.close()
