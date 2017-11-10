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
 
###  00-KK       
* **run.sh** script to run **ibz** executable    
**ibz** sets up special k-point list for tetrahedrum integration.    
It needs as input:    
**pvectors** contains lattice cell parameters    
**sym.d** symmetry matrices of the crystal    


