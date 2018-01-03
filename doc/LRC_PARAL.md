# Tutorial

## Contents 
1. [SHG in GaAs](#shg_gaas)

Here, I will show how to run the GaAs example in parallel in Lawrencium clusters (at Lawrence Berkeley National Laboratory).    

<a id='basics'></a>
## Basics   
Please follow the GaAs example in serial first at [Tutorial](https://github.com/trangel/OPTpy/blob/master/doc/TUTORIAL.md)  

<a id='shg_gaas'></a>
## Second Harmonic Generation in GaAs  

This example is the same as in the first Tutorial.

Please create a new directory, and download the following files:   

* [Gaas.cif](https://raw.githubusercontent.com/trangel/OPTpy/master/examples/data/structures/GaAs.cif): Structure file in cif format (from the Materials Project database)   
* [31ga.3.hgh](https://github.com/trangel/OPTpy/tree/master/examples/data/pseudos/31ga.3.hgh):   HGH pseudopotential for Ga   
* [33as.5.hgh](https://github.com/trangel/OPTpy/tree/master/examples/data/pseudos/33as.5.hgh): HGH pseudopotential for As   
* [GaAs-paral-lrc.py](https://raw.githubusercontent.com/trangel/OPTpy/master/examples/flows/GaAs-paral-lrc.py): 
OPTpy input file for SHG in GaAs 

You should have in a single directory:    
```bash
ls   
33as.5.hgh GaAs.py 31ga.3.hgh GaAs-paral-lrc.cif
```

To run OPTpy simply do:   
```bash
python GaAs-paral-lrc.py
```
This should create:     
```bash
taskfile1  taskfile2  job.sh
```   
in addition to (same as in previous tutorial):    
```bash
00-KK	    03-RPMNS	33as.5.hgh  gaas.klist_4x4x4  symmetries
01-Density  04-RESP	GaAs.cif    res
02-WFN	    31ga.3.hgh	GaAs.py     run.sh
```

Let's describe the new files:     
* [taskfile1](#taskfile1)    
* [taskfile2](#taskfile2)   
* [job.sh](#job)    
 
<a id='taskfile1'></a>
###  taskfile1    
This contains series of calculations for the 02-WFN task.    
In fact, the calculation is parallelized on k-points, each subdirectory in 02-WFN will be used to calculate a subset of the total number of k-points.   
Note that in DFT k-points can be run independent of each other.   

#### taskfile2     
These are series of calculations for the 03-RPMNS task.   
The matrix elements are going to be computed in parallel (for k-points).   

#### job.sh   
This is a usual slurm job file, but it will run the series of calculations in taskfile1 and taskfile2 above in parallel, 
the trick is done with the ht\_helper function of LRC clusters as:   
```
# Divide tasks by k-point, run several serial jobs in parallel using ht_helper in LRC:
ht_helper.sh -t taskfile1 -n1 -s1 -vL -o "-x PATH -x LD_LIBRARY_PATH"
ht_helper.sh -t taskfile2 -n1 -s1 -vL -o "-x PATH -x LD_LIBRARY_PATH"
```   
For details, please consult the LRC cluster documentation.    
