from __future__ import print_function
import os
from numpy import dot,round
from .abinittask import AbinitTask

__all__ = ['AbinitWfnTask']

class AbinitWfnTask(AbinitTask):
    """Charge density calculation."""

    _TASK_NAME = 'Wavefunction task'

    _input_fname = 'wfn.in'
    _output_fname = 'wfn.out'

    def __init__(self, dirname, **kwargs):
        """
        Arguments
        ---------

        dirname : str
            Directory in which the files are written and the code is executed.
            Will be created if needed.


        Keyword Arguments
        -----------------

        charge_density_fname : str
            Name of the density file produced by a previous SCF run (_DEN).
        ecut : float
            Kinetic energy cut-off, in Hartree.
        nband : int
            Number of bands to be computed.
        nbdbuf : int
            Number of bands in the buffer, useful for NSCF calculations in lots of bands.
        tolwfr : float (1e-16)
            Tolerance on wavefunctions residual used as a convergence criterion
            for the NSCF cycle.
        prefix : str
            Prefix used as a rootname for abinit calculations.
        structure : pymatgen.Structure
            Structure object containing information on the unit cell.
        input_wavefunction_fname: str, optional
            Name of previously compute wavefunction file, in case you want
            to restart from there.
        input_variables : dict
            Any other input variables for the Abinit input file.
        nspinor : Number of spinorial components, int, optional
            Default 1

        See also:

        """

        kwargs.setdefault('prefix', 'wfn')

        self.prefix=kwargs['prefix']
        self.kgrid_response=kwargs['kgrid_response']
        self.kgrid="{}x{}x{}".format(self.kgrid_response[0],self.kgrid_response[1],self.kgrid_response[2])

#       Extra lines for run script:
        self.runlines="#k-points read from kpt.in file:\n\
echo kptopt 0 > kpt.in\n\
echo nkpt >>kpt.in\n\
cat ../{0}.klist_{1} | wc -l >> kpt.in\n\
echo kpt >>kpt.in\n\
cat ../{0}.klist_{1} >>kpt.in\n".format(self.prefix,self.kgrid)

        super(AbinitWfnTask, self).__init__(dirname, **kwargs)

        self.charge_density_fname = kwargs['charge_density_fname']

        if 'input_wavefunction_fname' in kwargs:
            self.input_wavefunction_fname = kwargs['input_wavefunction_fname']

        self.input.set_variables(self.get_wfn_variables(**kwargs))

        

    def get_wfn_variables(self, **kwargs):
        """Return a dict of variables required for an SCF calculation."""

        nband = kwargs.get('nband')
        if not nband:
            nband = kwargs.get('nbnd')

        ecut = kwargs.get('ecut')
        if not ecut:
            ecut = kwargs.get('ecutwfc')
            if not ecut:
                raise Exception("Please specify 'ecut' for Abinit.")
            else:
                # Maybe warn the user that ecut is in Hartree?
                pass


        variables = dict(
            ecut = ecut,
            nband = nband,
            irdden = 1,
            nbdbuf = kwargs.get('nbdbuf', 0),
            irdwfk = 1 if self.input_wavefunction_fname else 0,
            tolwfr = kwargs.get('tolwfr', 1e-16),
            iscf = kwargs.get('iscf', -3),
            istwfk = kwargs.get('istwfk', '*1'),
            include = "\"kpt.in\"",
            nspinor = kwargs.pop('nspinor', 1),
            )
        return variables

    @property
    def wavefunction_fname(self):
        return self.get_odat('WFK')

    wfn_fname = wavefunction_fname
    wfk_fname = wavefunction_fname

    @property
    def charge_density_fname(self):
        return self.get_odat('DEN')

    @charge_density_fname.setter
    def charge_density_fname(self, value):
        self._charge_density_fname = value
        dest = os.path.relpath(self.get_idat('DEN'), self.dirname)
        self.update_link(value, dest)

    rho_fname = charge_density_fname

    _input_wavefunction_fname = ''
    @property
    def input_wavefunction_fname(self):
        return self._input_wavefunction_fname
    
    @input_wavefunction_fname.setter
    def input_wavefunction_fname(self, value):
        self._input_wavefunction_fname = value
        dest = os.path.relpath(self.get_idat('WFK'), self.dirname)
        self.update_link(value, dest)

    @property
    def exchange_correlation_potential_fname(self):
        return self.get_odat('VXC')

    vxc_fname = exchange_correlation_potential_fname

    def kpts_from_file(self,**kwargs):
        from numpy import reshape as np_reshape
        from numpy import fromfile as np_fromfile
        from numpy import ndarray as ndarray
#       Read k-points from file (obsolete):
        nkTetra = kwargs['nkTetra']
        kpt_filename="symmetries/"+self.prefix+".kcartesian_"+str(nkTetra)
        kcartesian=np_fromfile(kpt_filename,sep= ' ')
#       Get reciprocal lattice vectors:
#       Pymatgen. lattice. reciprocal_lattice(self)
#       Get inverse matrix, to then convert to recp.
#       Note that cartesian coordinates are in angstrom:
        bohr2ang=0.529177249
        reciprocal_lattice=self.structure.lattice.reciprocal_lattice
        invM = reciprocal_lattice.inv_matrix/bohr2ang
#       Check k-points in file are OK
        nk=kcartesian.size/3
        if ( nk != nkTetra ):
            print("%i k-points found in file %s.\nExpecting %i \n" % (nk,nkTetra))
            exit(1)
        kcartesian=np_reshape(kcartesian,(nk,3))
        kpt=ndarray(shape=(nkTetra,3),dtype=float) 
        for ik in range(nkTetra):
             kk=kcartesian[ik][:]
             kred=dot(kk, invM)
             kpt[ik][:]=round(kred,6)

