from os import path, mkdir,curdir
from ..core import Workflow 

__all__ = ['RESPONSESflow']

class RESPONSESflow(Workflow):
    def __init__(self,**kwargs):
        """ 
        keyword arguments:
        nval : Number of valence bands
        nband : Number of bands
        ecut : Kinetic energy cutoff
        lt : total | layer
        nspinor=1 : Number of spinorial components
        nkTetra=5 : Number of k-points for Tetrahedral integration
        scissors=0 : Value of scissors shift (eV) (not working yet)
        components : Tensor components to be calculated, 
             e.g. ["xx","yy","zz"],
        vnlkss=False : Take into accoung Vnl and KSS file (not working yet)
        option: 1 Full #Change name
        smearvalue : Smearing value in eV 
        response : Response to calculate:
        ---------  choose a response ---------
        1  chi1----linear response           24 calChi1-layer linear response     
        3  eta2----bulk injection current    25 calEta2-layer injection current   
        41 zeta----bulk spin injection       29 calZeta-layer spin injection      
        21 shg1L---Length gauge-1w&2w faster 22 shg2L---Length gauge-2w           
        42 shg1V---Velocity gauge-1w&2w      43 shg2V---Velocity gauge-2w         
        44 shg1C---Layer-Length gauge-1w&2w  45 shg2C---Layer-Length gauge-2w     
        26 ndotccp-layer carrier injection   27 ndotvv--carrier injection   
        """
        super(RESPONSESflow, self).__init__(**kwargs)
        self.lt = kwargs['lt']
        self.nval = kwargs['nval']
        self.nband = kwargs['nband']
        self.nkTetra = kwargs['nkTetra']
        self.ecut = kwargs['ecut']
        self.nspinor= kwargs['nspinor']
        self.scissors = kwargs['scissors']
        self.components = kwargs['components']
        self.vnlkss = kwargs['vnlkss']
        self.option = kwargs['option']
        self.smearvalue = kwargs['smearvalue']
        self.response = kwargs['response']

    def write(self):
        """ Run the responses.sh Tiniba executable"""
        case=str(self.nkTetra)+"_"+str(int(self.ecut))
        if ( self.nspinor > 1 ):
            case = case+"-spin"
        components_list=' '.join(str(p) for p in self.components)
        ncond=self.nband-self.nval 
        filename="run-responses.sh"
        f=open(filename,"w")
        f.write("#!/bin/bash\n\n")
        f.write("responses-local.sh -w %s -m %s -s %s -o %s -v %i -c %i -r %s -t \"%s\" -b %f -n .%s.\n" 
            % (self.lt,case,self.scissors,self.option,self.nval,ncond,self.response,components_list,self.smearvalue,str(self.vnlkss)))

        f.close()
