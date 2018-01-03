import os 

def lrc_mk_paraljob(**kwargs):
    """
    Writes a submission script for lawrencium clusters
    --------------------------------------------------

    Optional arguments:
    jobname : str, default "job"
    dirname : str, default './'
    cluster : str, default 'nokomis'
    nproc   : int, default 16
    modules : str, default ''
    """
    jobname = kwargs.pop('jobname','job')
    dirname = kwargs.pop('dirname','./')
    cluster = kwargs.pop('cluster','nokomis')
    nproc   = kwargs.pop('nproc',16)
    modules = kwargs.pop('modules','')
    #
    # Check input parameters
    #
    known_clusters=['catamount','nokomis','minnehaha']
    if cluster not in known_clusters:
        print('Unknown cluster {}'.format(cluster))
        print('Known clusters {}'.format(' '.join(known_clusters)))
        exit(1)

    # Write taskfile1:
    newfile = os.path.join(dirname,"taskfile1")
    f = open (newfile,"w")
    for iproc in range(1,nproc+1):
        f.write("cd 02-WFN/{}; bash run.sh\n".format(iproc))
    f.close()

    # Write taskfile2:
    newfile = os.path.join(dirname,"taskfile2")
    f = open (newfile,"w")
    for iproc in range(1,nproc+1):
        f.write("cd 03-RPMNS/{}; bash run.sh\n".format(iproc))
    f.close()

    # Write run files
    newfile = os.path.join(dirname,"run1.sh")
    f = open(newfile,"w")
    f.write("#!/bin/bash\n\n")
    f.write("cd 00-KK\n")
    f.write("bash run.sh\n")
    f.write("cd ..\n")
    f.write("cd 01-Density\n")
    f.write("bash run.sh\n")
    f.write("cd ..\n")
    f.close()

    newfile = os.path.join(dirname,"run2.sh")
    f = open(newfile,"w")
    f.write("#!/bin/bash\n\n")
    f.write("cd 03-RPMNS\n")
    f.write("bash run.sh\n")
    f.write("cd ..\n")
    f.write("cd 04-RESP\n")
    f.write("bash run.sh\n")
    f.write("cd ..\n")
    f.close()

    # job.sh file
    newfile = os.path.join(dirname,"job.sh")
    f = open(newfile,"w")
    f.write("#!/bin/bash -l\n")
    f.write("#SBATCH  --job-name={}\n".format(jobname))
    if cluster == 'minnehaha' :
        f.write("#SBATCH  --qos=condo_minnehaha\n")
        f.write("#SBATCH  --account=lr_minnehaha\n")
        f.write("#SBATCH  --partition=lr4\n")
    elif cluster == 'nokomis' :
        f.write("#SBATCH  --qos=condo_nokomis\n")
        f.write("#SBATCH  --account=lr_nokomis\n")
        f.write("#SBATCH  --partition=lr3\n")
    elif cluster == 'catamount' :
        f.write("#SBATCH  --qos=cm_medium\n")
        f.write("#SBATCH  --account=catamount\n")
        f.write("#SBATCH  --partition=catamount\n")

    f.write("#SBATCH  --ntasks={}\n".format(nproc))
    f.write("#SBATCH  -t 120:00:00\n")
    f.write("#SBATCH --mail-type=all\n")
    f.write("#SBATCH --mail-user=trangel@lbl.gov\n\n")
    f.write("bash /global/home/users/trangel/.optpy\n\n")
    f.write(modules)
    f.write("\n\n")
    f.write("# Execution (ABINIT parallelized with MPI)\n")
    f.write("bash run1.sh\n\n")
    f.write("# Divide tasks by k-point, run several serial jobs in parallel using ht_helper in LRC:\n")
    f.write("ht_helper.sh -t taskfile1 -n1 -s1 -vL -o \"-x PATH -x LD_LIBRARY_PATH\"\n")
    f.write("ht_helper.sh -t taskfile2 -n1 -s1 -vL -o \"-x PATH -x LD_LIBRARY_PATH\"\n\n")
    f.write("# Execute merge and respones:\n")
    f.write("# Not parallelized:\n")
    f.write("bash run2.sh\n")
    f.close() 
