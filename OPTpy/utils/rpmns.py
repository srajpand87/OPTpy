from os import path, mkdir,curdir
from ..core import Workflow 

__all__ = ['RPMNSflow']

class RPMNSflow(Workflow):
    def __init__(self,**kwargs):
        """ 
        keyword arguments:
        structure : pymatgen.Structure
            Structure object containing information on the unit cell.
        """
        super(RPMNSflow, self).__init__(**kwargs)
        self.nval = kwargs['nval']

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
        f.close()
