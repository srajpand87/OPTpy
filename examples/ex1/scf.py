"""
Compute ground state charge density.

"""
from OPTpy import  AbinitScfTask,Structure

task = AbinitScfTask(
    dirname = 'SCF',

    structure=Structure.from_file('../data/structures/GaAs.json'),
    prefix = 'gaas',
    pseudo_dir = '../data/pseudos',
    pseudos = ['31-Ga.pspnc', '33-As.pspnc'],

    ngkpt = [2,2,2],      # k-points grid
    kshift = [.5,.5,.5],  # k-points shift
    ecut = 5.0,           # Wavefunctions cutoff energy

    # These are the default parameters for the MPI runner.
    # Please adapt them to your needs.
    nproc = 1,
    nproc_per_node = 1,
    mpirun = 'mpirun',
    nproc_flag = '-n',
    nproc_per_node_flag = '--npernode',
    )


# Execution
task.write()
#task.run()
#task.report()
