from os import path, mkdir,curdir
from ..core import Workflow 

__all__ = ['RESPONSEflow']

#       Response name
#       1  chi1----linear response           24 calChi1-layer linear response     
#       3  eta2----bulk injection current    25 calEta2-layer injection current   
#       41 zeta----bulk spin injection       29 calZeta-layer spin injection      
#       21 shg1L---Length gauge-1w&2w faster 22 shg2L---Length gauge-2w           
#       42 shg1V---Velocity gauge-1w&2w      43 shg2V---Velocity gauge-2w         
#       44 shg1C---Layer-Length gauge-1w&2w  45 shg2C---Layer-Length gauge-2w     
#       26 ndotccp-layer carrier injection   27 ndotvv--carrier injection 
response_dict={
    1  : 'chi1'  , 24 : 'calChi1-layer',
    3  : 'eta2'  , 25 : 'calEta2-layer', 
    41 : 'zeta'  , 29 : 'calZeta-layer' , 
    21 : 'shg1L' , 22 : 'shg2L', 
    26 : 'ndotccp-layer' ,  27 : 'ndotvv',
    42 : 'shg1V' , 43 : 'shg2V',
    44 : 'shg1C' , 45 : 'shg2C' 
}
component_dict={ 'x' : 1, 'y' : 2, 'z' : 3 }

class RESPONSEflow(Workflow):
    def __init__(self,**kwargs):
        """ 
        keyword arguments:
        kgrid_response : k-points for tetrahedra integration
        nval : Number of valence bands to compute the response
        nval_total : Total number of valence bands in the NSCF calculation
        nband : Total number of bands in the NSCF calculation
        ncond : Number of conduction bands to calculate the response
        scissors=0 : Value of scissors shift (eV) (not working yet)
                     Default = 0.0 eV
        tol: Smearning used in Fermi Golden's rule 
             (Delta function of vc energy difference)
             Default = 0.03 eV
        nspinor : Number of spinorial component
        ecut : Kinetic energy cutoff
        acellz : Dimension (in Bohrs) of unit cell along the z direction
                 Used in layer calculations
        dirname : Directory name to run Tiniba
        energy_min : Energy minimimum (in eV) in energy grid for responses
                     Default 0
        energy_max : Energy maximum (in eV) in energy grid for responses
                     Default 10 eV
        energy_steps : Number of points in energy grid for responses
                       Default 2001
        lt : total | layer, default (total)
        components : Tensor components to be calculated, 
             e.g. ["xx","yy","zz"],
        vnlkss=False : Take into accoung Vnl and KSS file (not working yet)
        option: 1 Full #Change name
        prefix : prefix for files in this calculation
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
        super(RESPONSEflow, self).__init__(**kwargs)
        self.dirname = kwargs.pop('dirname','RESP')
        self.nval = kwargs['nval']
        self.nval_total = kwargs['nval_total']
        self.ncond = kwargs['ncond']
        self.nband = kwargs['nband']
        self.kgrid_response = kwargs['kgrid_response']
        self.kgrid="{}x{}x{}".format(self.kgrid_response[0],self.kgrid_response[1],self.kgrid_response[2])
        self.ecut = kwargs['ecut']
        self.nspinor= kwargs['nspinor']
        self.prefix = kwargs['prefix']
        self.components = kwargs['components']
        self.response = kwargs['response']
#       Optional arguments:
        self.lt = kwargs.pop('lt','total')
        self.scissors = kwargs.pop('scissors',0.000)
        self.tol = kwargs.pop('tol',0.03)
        self.acellz = kwargs.pop('acellz',1.000)
        self.energy_min = kwargs.pop('energy_min',0)
        self.energy_max = kwargs.pop('energy_max',10)
        self.energy_steps = kwargs.pop('energy_steps',2001)
        self.vnlkss = kwargs.pop('vnlkss','False')
        self.option = kwargs.pop('option',1)
        self.smearvalue = kwargs.pop('smearvalue',0.15)


    def write_latm_input(self):
        """ Write input files for RESP"""
        from os import path, mkdir,curdir

#       Create RESP dir.:
        if not path.exists(self.dirname):
            mkdir(self.dirname)


#       Get case name:
        self.case=str(self.kgrid)+"_"+str(int(self.ecut))
        if ( self.nspinor > 1 ):
            self.case = self.case+"-spin"

    
#       Get number of k-points from file
        kfile="../{}.klist_{}".format(self.prefix,self.kgrid)
#        kMax=sum(1 for line in open(kfile))

#       Get variables from input variables:
        component_list=' '.join(str(p) for p in self.components)
        ncond_total=self.nband-self.nval_total
        withSO=".False."
        if ( self.nspinor == 2 ):
            withSO=".True."

#       Get file names:
        energy_data_filename= "eigen_"+self.case
        energys_data_filename= "energys.d_"+self.case
        half_energys_data_filename= "halfenergys.d_"+self.case
        pmn_data_filename= "pmn_"+self.case
        rmn_data_filename= "rmn.d_"+self.case
        der_data_filename= "der.d_"+self.case
        tet_list_filename= "tetrahedra_"+str(self.kgrid)
        integrand_filename= "Integrand_"+self.case
        spectrum_filename= "Spectrum_"+self.case
 
#       1. write tmp_$case file:
        filename=self.dirname+"/tmp_"+self.case
        f=open(filename,"w")
#            % (self.lt,case,self.scissors,self.option,self.nval,self.nval_total,self.ncond,ncond_total,self.response,component_list,self.smearvalue,str(self.vnlkss)))
        f.write("&INDATA\n")
        f.write("nVal = %i,\n" % (self.nval))
        f.write("nMax = %i,\n" % (self.nband))
        f.write("nVal_tetra = %i,\n" % (self.nval_total))
        f.write("nMax_tetra = %i,\n" % (self.ncond))
#        f.write("kMax = %i,\n" % (kMax))
        f.write("kMax = XXX,\n")
        f.write("scissor = %f,\n" % (self.scissors))
        f.write("tol = %f,\n" % (self.tol))
        f.write("nSpinor = %i,\n" % (self.nspinor))
        f.write("acellz = %f,\n" % (self.acellz))
        f.write("withSO = %s,\n" % (withSO))
        f.write("energy_data_filename = \"%s\",\n" % (energy_data_filename))
#       TODO correct misspellings in Tiniba:
        f.write("energys_data_filename = \"%s\",\n" % (energys_data_filename))
        f.write("half_energys_data_filename = \"%s\",\n" % (half_energys_data_filename))
        f.write("pmn_data_filename = \"%s\",\n" % (pmn_data_filename))
        f.write("rmn_data_filename = \"%s\",\n" % (rmn_data_filename))
        f.write("der_data_filename = \"%s\",\n" % (der_data_filename))
        f.write("tet_list_filename = \"%s\",\n" % (tet_list_filename))
        f.write("integrand_filename = \"%s\",\n" % (integrand_filename))
        f.write("spectrum_filename = \"%s\",\n" % (spectrum_filename))
        f.write("energy_min = %i,\n" % (self.energy_min))
        f.write("energy_max = %i,\n" % (self.energy_max))
        f.write("energy_steps = %i\n" % (self.energy_steps))
        f.write("/\n")

        f.close()

    def write_run_file(self):
        """ Writes file run.sh """
#       run.sh
        filename=self.dirname+"/run.sh"
        f=open(filename,"w")
        #
        f.write("#Copy files:\n")
        f.write("cp ../symmetries/tetrahedra_{} .\n".format(self.kgrid))
        f.write("cp ../symmetries/Symmetries.Cartesian_{} Symmetries.Cartesian\n".format(self.kgrid))
        f.write("cp ../eigen_{} .\n".format(self.case))
        f.write("cp ../pmn_{} .\n".format(self.case))
        #
        f.write("\n#Find number of k-points and replace kMax value in files:\n")
        f.write("nkpt=`cat ../{0}.klist_{1} | wc  -l`\n".format(self.prefix,self.kgrid))
        f.write("executable=`echo \"sed -i -e 's/XXX/$nkpt/g' tmp_{0}\"`\n".format(self.case))
        f.write("eval $executable\n\n")
        # 
        f.write("#Executable\nset_input_all tmp_{0} spectra.params_{0}\n".format(self.case))
        # Integrate each response at a time:
        resp_name=response_dict[self.response]
        f.write("\n#Integrate each component at a time:\n")
        for component in self.components:
            f.write("#Component %s\n" % (component)) 
            f.write("sed s/Integrand_%s/%s.%s.dat_%s/ tmp_%s >tmp1_%s\n"
            % (self.case,resp_name,component,self.case,self.case,self.case))
            f.write("sed s/Spectrum_%s/%s.%s.spectrum_ab_%s/ tmp1_%s > int_%s_%s\n"
            % (self.case,resp_name,component,self.case,self.case,component,self.case))
            f.write("#Executable\ntetra_method_all int_%s_%s\n\n" 
            % (component,self.case))
 
#        f.write("rm -f tmp*\n")
        f.close()

    def write_opt_file(self):
        """ Writes file opt.dat required by Tiniba
           option=1 from all valence bands Nv to 1...Nc conduction bands
           option=2 from a given valence band  to a given conduction band"""

        filename=self.dirname+"/opt.dat"
        f = open(filename,"w")
        f.write("%s %s %s\n" % (self.option,self.nval,self.ncond))
        f.close()

    def write_spectra_params(self):
        """ Writes spectra_params file (input for latm executable) """
        from numpy import empty as np_empty
        from numpy import int as np_int

#       Get variables from input variables:
        n_component=len(self.components)
        resp_name=response_dict[self.response]
#       spectra.params file:
        filename=self.dirname+"/spectra.params_"+self.case
        f=open(filename,"w")
        f.write("%i\n" % (n_component))
        for ii in range(n_component):
#           Map component 'xyz' to digits '123'
            cc=list(self.components[ii])
            cci=np_empty(shape=(len(cc)),dtype=np_int)
            for jj in range(len(cc)):
                cci[jj]=component_dict[cc[jj]]
#
            resp_filename=resp_name+"."+self.components[ii]+".dat_"+self.case
            file_num=501+ii
            f.write("%i %s %i T\n" % (self.response, resp_filename, file_num))
            for jj in range(len(cc)):
                f.write("%i " % (cci[jj]))
            f.write("\n") 
        f.close()       



    def write(self):
        """ Compute optical responses using Tiniba executables"""
        self.write_latm_input()
        self.write_run_file()
        self.write_spectra_params()
        self.write_opt_file()


