"""
Compute optical responses with OPTpy

"""
from OPTpy import  OPTflow,Structure, lrc_mk_paraljob

nproc = 16


flow = OPTflow(
    dirname = './',

    #
    # Common variables:
    #
    prefix = 'gaas',      # Root name for files required by Tiniba
    # Structure from file:
    structure=Structure.from_file('GaAs.cif'),

    #
    # Pseudopotentials:
    #
    pseudo_dir = './',
    pseudos = ['31ga.3.hgh', '33as.5.hgh'],

    ecut = 15.0,          # Cutoff energy for wavefunctions
    nspinor = 2,          # Number of spinorial components

    #
    # Variables for density:
    #
    ngkpt = [4,4,4],      # k-point grid for density
    kshift = [[.5,.5,.5],[.5,0,0],[0,.5,0],[0,0,.5]],  # k-point shift for density

    #
    # Variables for momentum matrix elements and responses:
    #
    kgrid_response=[4,4,4], # k-point grid for responses
    nband=36,      # Total number of bands
    nbdbuf=2,      # Bands in buffer (see Abinit documentation)
    nval_total=8,  # Total number of valence bands

    #
    # Variables for responses:
    #
    # Bands to include for transitions (can be less than for RPMNS)
    ncond=8,         # Number of conduction bands to include
    nval=8, # (= nval_total) All valence bands must be included, not working yet for nval < nval_total 
    # Response to calculate, see Doc. in responses.py
    response=1,
    components=["xx","yy","zz"],

    #  WFN and RPMS calculation split by k-points
    split_by_proc=True,

    # Default parameters for the MPI runner.
    # Please adapt them to your needs.
    nproc = nproc,
    nproc_per_node = '',
    mpirun = 'mpirun',
    nproc_flag = '',
    nproc_per_node_flag = '',
    mpi_extra_vars='',
    )


# Execution
# This is my local execution task:
flow.write()


#
# Now let's write the job slurm file for LRC clusters:
#
# These are the modules to be load (please modify this as needed:
modules="\
module load intel openmpi mkl\n"

lrc_mk_paraljob(
    jobname = 'job',
    dirname = flow.dirname,
    cluster = 'nokomis',
    modules = modules,
    nproc = nproc
    )
