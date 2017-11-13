# Tutorial

## Contents 
1. [Basics](#basics)
2. [SHG in GaAs](#shg_gaas)

<a id='basics'></a>
## Basics   
To start using OPTpy you need to go first to the basics of ABINIT.   
Please go through the basic lessons (1 to 4) on the [ABINIT web site](http://www.abinit.org) first.   

<a id='shg_gaas'></a>
## Second Harmonic Generation in GaAs  

For this example we will need:   
1. pseudopotential files
2. structure data   

Please create a new directory, and download the following files:   

* [Gaas.cif](https://raw.githubusercontent.com/trangel/OPTpy/master/examples/data/structures/GaAs.cif): Structure file in cif format (from the Materials Project database)   
* [31ga.3.hgh](https://github.com/trangel/OPTpy/tree/master/examples/data/pseudos/31ga.3.hgh):   HGH pseudopotential for Ga   
* [33as.5.hgh](https://github.com/trangel/OPTpy/tree/master/examples/data/pseudos/33as.5.hgh): HGH pseudopotential for As   
* [GaAs.py](https://raw.githubusercontent.com/trangel/OPTpy/master/examples/flows/GaAs.py): 
OPTpy input file for SHG in GaAs 

You should have in a single directory:    
```bash
ls   
33as.5.hgh GaAs.py 31ga.3.hgh GaAs.cif
```

To run OPTpy simply do:   
```bash
python GaAs.py
```

This should create:
```bash
ls
00-KK      02-WFN     04-RESP    33as.5.hgh GaAs.py    run.sh
01-Density 03-RPMNS   31ga.3.hgh GaAs.cif   res        symmetries
```

Let's describe the content of the directories:  
* [00-KK](#kk)    
* [01-Density](#density)   
* [02-WFN](#wfn)    
* [03-RPMNS](#rpmns)    
* [04-RESP](#resp)    
 
<a id='kk'></a>
###  00-KK 
Set up k-point grid for tetrahedra integration   

#### Scripts         
* **run.sh**: script to run **ibz** executable    

#### Executable
* **ibz**: sets up a special k-point list for tetrahedrum integration.    

#### Input files   
* **pvectors**: contains lattice cell parameters    
* **sym.d**: symmetry matrices of the crystal    
Note the two files above are created by OPTpy and linked via run.sh.    

#### Output files   
* **gaas.klist_4x4x4**: list of special k-points for tetrahedrum integration for a 4x4x4 grid in reduced coordinates    
* **symmetries/gaas.kcartesian_4x4x4**: same as above but in Cartesian coordinates   
* **symmetries/tetrahedra_4x4x4**: definition of tetrahedra for integration    
* **symmetries/Symmetries.Cartesian_4x4x4**: symmetries in Cartesian coordinates       

<a id='density'></a>
### 01-Density  
Ground state calculation with ABINIT    

#### Scripts         
* **run.sh**: main bash script to run ABINIT    

#### Executable
ABINIT   

#### Input files
* **gaas.files**: ABINIT *files* file   
* **gaas.in**: ABINIT input file     
* **input_data**: directory for eventual input files for ABINIT (empty in this case)    
* **tmp_data**: directory to store temporary files while executing ABINIT    
 
#### Output files   
* **out_data**: directory to store big output files (wavefunctions, density, etc...) from ABINIT    
