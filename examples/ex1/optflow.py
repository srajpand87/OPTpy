"""
Compute optical responses with OPTpy

"""
from OPTpy import  OPTflow,Structure

flow = OPTflow(
    dirname = './',

#   Common variables:
    prefix = 'gaas',      # Root name for files required by Tiniba
#   Structure from file:
    structure=Structure.from_file('../data/structures/GaAs.json'),

#   Pseudopotentials:
    pseudo_dir = '../data/pseudos',
    pseudos = ['31-Ga.pspnc', '33-As.pspnc'],

    ecut = 5.0,           # Wavefunctions cutoff energy
    nspinor = 2,          # Number of spinorial components

#   Variables for density:
    ngkpt = [2,2,2],      # k-point grid for density
    kshift = [.5,.5,.5],  # k-point shift for density

#   Variables for momentum matrix elements and responses:
    kgrid_response=[4,4,4], # k-point grid for responses
    nkTetra=5,  #This should be read from output of KK?
                #TODO make kk.f90 part of OPTpy
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

    # These are the default parameters for the MPI runner.
    # Please adapt them to your needs.
    nproc = 1,
    nproc_per_node = 1,
    mpirun = 'mpirun',
    nproc_flag = '',
    nproc_per_node_flag = '',
    )


# Execution
flow.write()
#flow.run()
#flow.report()
