"""Workflow to run an optical-response calculation."""
from __future__ import print_function

from os.path import join as pjoin
from os.path import dirname
from os import getcwd

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
        structure : pymatgen.Structure
            Structure object containing information on the unit cell.

        """
        super(OPTflow, self).__init__(**kwargs)

        kwargs.pop('dirname', None)

        self.ngkpt = kwargs.pop('ngkpt',[1,1,1])
        self.kshift = kwargs.pop('kshift', [.0,.0,.0])


#       Get current path:
        self.cwd=dirname(getcwd())
        print(self.cwd)
        # ==== KK task ==== #
        self.make_kk_task(**kwargs)

        # ==== DFT calculations ==== #
        fnames = self.make_dft_tasks_abinit(**kwargs)
        kwargs.update(fnames)

        # === RPMNS calculation === #
        self.make_rpmns_task(**kwargs)  

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
            dirname = pjoin(self.dirname, '00-KK'),
            **kwargs)

        self.add_task(self.kktask)
            
    def make_rpmns_task(self,**kwargs):
        """ Run RPMNS task.
        Compute momentum matrix elements. """
        from ..utils import RPMNSflow

        self.rpmnstask = RPMNSflow(
            dirname = pjoin(self.dirname, '03-RPMNS'),
            **kwargs)

        self.add_task(self.rpmnstask)

    def make_response_task(self,**kwargs):
        """ Run response task.
        Compute responses with Tiniba. """
        from ..utils import RESPONSEflow

        self.responsetask = RESPONSEflow(
            dirname = pjoin(self.dirname,'04-RESP'),
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
            raise Exception("Error, when providing charge_density_fname is required")

        else:
            self.scftask = AbinitScfTask(
                dirname = pjoin(self.dirname, '01-Density'),
                ngkpt = self.ngkpt,
                kshift = self.kshift,
                **kwargs)

            self.add_task(self.scftask)
            
            kwargs.update(
                charge_density_fname = self.scftask.charge_density_fname)

#       WFN calculation
        self.wfntask = AbinitWfnTask(
            dirname = pjoin(self.dirname, '02-WFN'),
            **kwargs)

        self.add_task(self.wfntask)

        kwargs.update(
            wfn_fname = pjoin(self.cwd,self.wfntask.wfn_fname)) 

        fnames = dict(wfn_fname = pjoin(self.cwd,self.wfntask.wfn_fname))
        return fnames
