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
Then run ABINIT and Tiniba with:   
```bash
bash run.sh   
```

This should create:
```bash
ls
00-KK	    03-RPMNS	33as.5.hgh  gaas.klist_4x4x4  symmetries
01-Density  04-RESP	GaAs.cif    res
02-WFN	    31ga.3.hgh	GaAs.py     run.sh
```

Let's describe the files and directories:  
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
* **gaas.out**: output text file from ABINIT    
* **out_data**: directory to store ground-state density from ABINIT   
 
<a id='wfn'></a>
### 02-WFN     
Wavefuncitons calculation with ABINIT    
Scripts, exectuable, and input file conventions are the same as in [01-Density](#density).    

#### Output files  
* **gaas.out**: output text file from ABINIT    
* **out_data**: directory to store wavefunctions from ABINIT    

<a id='rpmns'></a> 
### 03-RPMNS   
Matrix elements with TINIBA       

#### Scripts         
* **run.sh**: main bash script to run TINIBA    

#### Executable
* **rpmns**: constructs momentum matrix elements from ABINIT wavefunctions      

#### Input files
* **WFK**: ABINIT wavefunctions file   
 
#### Output files  
* **eigen_4x4x4_15-spin**: eigenvalues    
* **pmn_4x4x4_15-spin**: momentum matrix elements   
* **pnn_4x4x4_15-spin**

<a id='resp'></a>
### 04-RESP   
Responses with TINIBA         

#### Scripts         
* **run.sh**: main bash script to run TINIBA

#### Executables
* **set_input_all**: prepares input files for tetrahedra integration   
* **tetra_method_all**: performs integration with tetrahedra method   
* **rkramer**: Performs Kramers-Kronig transformation to get imaginary part of spectrum from the real part    


#### Input files
This uses most output files obtained in 03 and 00 above    
See first lines of bash.sh    
```bash
ln -nfs ../symmetries/tetrahedra_4x4x4 tetrahedra_4x4x4
ln -nfs ../gaas.klist_4x4x4 gaas.klist_4x4x4
ln -nfs ../symmetries/Symmetries.Cartesian_4x4x4 Symmetries.Cartesian
ln -nfs ../eigen_4x4x4_15-spin eigen_4x4x4_15-spin
ln -nfs ../pmn_4x4x4_15-spin pmn_4x4x4_15-spin
ln -nfs ../pnn_4x4x4_15-spin pnn_4x4x4_15-spin
```

#### Output files   
* **res/shgL.xyz.4x4x4_15-spin.Nv8.Nc8**: SHG along the xyz direction (4x4x4 grid, energy cutoff 15 Hartree, using spinors, transitions over 8 valence and 8 conduction bands)    
Note that the k-point grid is too small (underconvergence).    

To plot the absolute value of the SHG spectra (as measured in experiment) in gnuplot syntax:   
```
plot 'shgL.xyz.4x4x4_15-spin.Nv8.Nc8' u 1:(($2+$4)**2+($3+$5)**2)**0.5 w l
``` 
