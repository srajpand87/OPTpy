"""Workflow to run an optical-response calculation."""
from __future__ import print_function

#from os.path import join as pjoin
#from os.path import dirname
#from os import getcwd
import os
from ..external import Structure
from ..core import Workflow
from ..Abinit import AbinitScfTask, AbinitWfnTask

__all__ = ['OPTflow']

class OPTflow(Workflow):
    """
    Optical response flow made of the following tasks:
        - Set parameters for tetrahedrum integration
        - DFT charge density, wavefunctions and eigenvalues
        - Momentum matrix elements
        - Calculate responses
    """

    def __init__(self, **kwargs):
        """
        Keyword arguments
        -----------------
        (All mandatory unless specified otherwise)

        dirname : str
            Directory in which the files are written and the code is executed.
            Will be created if needed.
        kgrid_response : list(3), int
            Grid of k-points used for the response
        kshift : list(3), float, optional
            Relative shift of the k-points grid along each direction,
            as a fraction of the smallest division along that direction.
        ngkpt : list(3), float
            K-points grid. Number of k-points along each primitive vector
            of the reciprocal lattice.
        nband : int
            Number of bands to be computed.
        ecut : float
            Energy cutoff for the wavefunctions
        prefix : str
            Prefix required by Tiniba as a rootname.
        pseudo_dir : str
            Directory in which pseudopotential files are found.
        pseudos : list, str
            Pseudopotential files.
        split_by_proc : logic, optional
            Default = False
            Split WFN/RPMS tasks by number of processors.
        structure : pymatgen.Structure
            Structure object containing information on the unit cell.

        """

#       Initialize variables:
        super(OPTflow, self).__init__(**kwargs)

#       Current directory
#        self.cwd=os.getcwd()
#        self.cwd=os.path.dirname(os.getcwd())

        kwargs.pop('dirname', None)
        self.ngkpt = kwargs.pop('ngkpt',[1,1,1])
        self.kshift = kwargs.pop('kshift', [.0,.0,.0])
        self.split_by_proc = kwargs.pop('split_by_proc',False)
        self.nproc = kwargs.pop('nproc',1)

        # ==== KK task ==== #
        tetrahedra_fname,symmetries_fname,kreciprocal_fname=self.make_kk_task(**kwargs)
        kwargs.update(tetrahedra_fname=tetrahedra_fname,
                      symmetries_fname=symmetries_fname,
                      kreciprocal_fname=kreciprocal_fname)

        # ==== DFT calculations ==== #
        wfn_fnames=self.make_dft_tasks_abinit(**kwargs)
        kwargs.update(wfn_fname=wfn_fnames)

        # === RPMNS calculation === #
        (eigen_fname,pmn_fname,pnn_fname)=self.make_rpmns_task(**kwargs)  
        kwargs.update(
		eigen_fname=eigen_fname,
		pmn_fname=pmn_fname,
		pnn_fname=pnn_fname)

        # === MERGE files === #
        self.make_merge_task(**kwargs)  

        # === Optical response === #
        self.make_response_task(**kwargs) 

    @property
    def has_kshift(self):
        return any([i!=0 for i in self.kshift])


    def make_kk_task(self,**kwargs):
        """ Run KK flow.
        Initialize parameters for tetrahedrum integration."""
        from ..utils import KKflow 

        self.kktask = KKflow(
            dirname = os.path.join(self.dirname, '00-KK'),
            **kwargs)

        self.add_task(self.kktask)
        kwargs.update(
            tetrahedra_fname = self.kktask.tetrahedra_fname,
            symmetries_fname = self.kktask.symmetries_fname,
            kreciprocal_fname = self.kktask.kreciprocal_fname)
        tetrahedra_fname = self.kktask.tetrahedra_fname
        symmetries_fname = self.kktask.symmetries_fname
        kreciprocal_fname = self.kktask.kreciprocal_fname
       
        return tetrahedra_fname,symmetries_fname, kreciprocal_fname
           
    def make_merge_task(self,**kwargs):
        """ Run merge task: 
        when calculation is split, it merges the output files """
        from ..utils import MERGEflow

        if ( self.split_by_proc == True ):
            dirname='03-RPMNS/'
            self.mergetask = MERGEflow(
                dirname = os.path.join(self.dirname, dirname),
                ntask=self.ntask,
                **kwargs)
            self.add_task(self.mergetask)

 
    def make_rpmns_task(self,**kwargs):
        """ Run RPMNS task.
        Compute momentum matrix elements. """
        from ..utils import RPMNSflow

        if ( self.split_by_proc == False ):
            self.rpmnstask = RPMNSflow(
                dirname = os.path.join(self.dirname, '03-RPMNS'),
                **kwargs)
            self.add_task(self.rpmnstask)
        else:
            # Divide calculation by nproc:
            kwargs.update(mpirun='')
            for self.task in range(self.ntask):
                dirname='03-RPMNS/'+str(self.task+1)
                self.rpmnstask = RPMNSflow(
                    dirname = os.path.join(self.dirname, dirname),
                    task=self.task+1,
                    ntask=self.ntask,
                    rename=False,
                    **kwargs)
                self.add_task(self.rpmnstask,background=True)
            self.runscript.append("wait\n")

        eigen_fname=self.rpmnstask.eigen_fname
        pmn_fname=self.rpmnstask.pmn_fname
        pnn_fname=self.rpmnstask.pnn_fname
        kwargs.update(
            eigen_fname=eigen_fname,
            pmn_fname=pmn_fname,
            pnn_fname=pnn_fname) 
        return eigen_fname,pmn_fname,pnn_fname 

    def make_response_task(self,**kwargs):
        """ Run response task.
        Compute responses with Tiniba. """
        from ..utils import RESPONSEflow

        self.responsetask = RESPONSEflow(
            dirname = os.path.join(self.dirname,'04-RESP'),
            **kwargs)

        self.add_task(self.responsetask)


    def make_dft_tasks_abinit(self, **kwargs):
        """
        Initialize all DFT tasks using Abinit.
        Return a dictionary of file names.
        """
        from ..Abinit import AbinitScfTask

        # Either charge density is provided or an SCF task is initialized.
        if 'charge_density_fname' in kwargs:
            print("Skiping SCF calculation\n")
        else:
            self.scftask = AbinitScfTask(
                dirname = os.path.join(self.dirname, '01-Density'),
                ngkpt = self.ngkpt,
                kshift = self.kshift,
                **kwargs)

            self.add_task(self.scftask)
            
            kwargs.update(
                charge_density_fname = self.scftask.charge_density_fname)

        # WFN calculation

        # Here we remove the variables related to k-points, 
        #these are read from an external file.
        if ( 'ngkpt' in kwargs ):
            del kwargs['ngkpt']
        wfn_fnames = [] 
        if ( self.split_by_proc == False ):
            self.wfntask = AbinitWfnTask(
                dirname = os.path.join(self.dirname, '02-WFN'),
                **kwargs)

            self.add_task(self.wfntask)
            #wfn_fname=os.path.join('../',self.wfntask.wfn_fname)
            wfn_fname=self.wfntask.wfn_fname
            wfn_fnames.append(wfn_fname)

            #fnames = dict(wfn_fname = os.path.join('../',self.wfntask.wfn_fname))
            return wfn_fnames
        else : 
            # Divide calculation by nproc:
            self.ntask=self.nproc
            # split tasks: 
            for self.task in range(self.ntask):
                kwargs.update(mpirun='')
                dirname='02-WFN/'+str(self.task+1)
                self.wfntask = AbinitWfnTask(
                    dirname = os.path.join(self.dirname, dirname),
                    task=self.task+1,
                    ntask=self.ntask,
                    **kwargs)

                self.add_task(self.wfntask,background=True)
                wfn_fname=self.wfntask.wfn_fname
                wfn_fnames.append(wfn_fname)
            self.runscript.append("wait\n")

        kwargs.update(
            wfn_fname=wfn_fnames ) 
        return wfn_fnames        
