"""
Compute wavefunction files.

"""
from OPTpy import  AbinitWfnTask,Structure

task = AbinitWfnTask(
    dirname = 'WFN',
    charge_density_fname = 'SCF/out_data/odat_DEN',
    structure=Structure.from_file('../data/structures/GaAs.json'),
    prefix = 'gaas',
    pseudo_dir = '../data/pseudos',
    pseudos = ['31-Ga.pspnc', '33-As.pspnc'],

#    ngkpt = [2,2,2],      # k-points grid
#    kshift = [0,0,0],  # k-points shift
#   Give k-points by hand, this are to be read from KK:
    kpt = [[0,0,0],[0.5,0.5,0.5]],
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
