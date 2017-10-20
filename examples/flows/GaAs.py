"""
Compute optical responses with OPTpy

"""
from OPTpy import  OPTflow,Structure
from myLRC import mkjob_by_task

flow = OPTflow(
    dirname = './',

#   Common variables:
    prefix = 'gaas',      # Root name for files required by Tiniba
#   Structure from file:
    structure=Structure.from_file('../data/structures/GaAs.json'),

#   Pseudopotentials:
    pseudo_dir = '../data/pseudos',
    pseudos = ['31-Ga.pspnc', '33-As.pspnc'],

    ecut = 15.0,           # Wavefunctions cutoff energy
    nspinor = 2,          # Number of spinorial components

#   Variables for density:
    ngkpt = [4,4,4],      # k-point grid for density
    kshift = [.5,.5,.5],  # k-point shift for density

#   Variables for momentum matrix elements and responses:
    kgrid_response=[4,4,4], # k-point grid for responses
    nband=36,   # Number of bands
    nbdbuf=2,   # Bands in buffer (see Abinit documentation).
    nval_total=8,     #TODO get number of valence bands from pseudopotentials

#   Variables for responses:
#   Bands to include for transitions (can be less than for RPMNS)
    ncond=8,
    nval=8,
#   Response to calculate, see Doc. in responses.py
    response=1,
    components=["xx","yy","zz"],

#   Turn on "split": WFN and RPMS calculation split: each proc is assigned to a task
    split_by_proc=True,

    # These are the default parameters for the MPI runner.
    # Please adapt them to your needs.
    nproc = 16,
    nproc_per_node = '',
    mpirun = 'mpirun',
    nproc_flag = '',
    nproc_per_node_flag = '',
    mpi_extra_vars='',
    )


# Execution
# This is my local execution task:
#flow.write()
#
#modules="\
#module swap gcc intel \n\
#module load openmpi mkl\n\
#module load intel/2013_sp1.4.211 openmpi hdf5/1.8.13-intel-p\n"
#
#mkjob_by_task(jobname='GaAs',
#    cluster='catamount',
#    nproc = flow.nproc,
#    modules = modules
#)

#flow.run()
#flow.report()
