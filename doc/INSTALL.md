# Install OPTpy

1. [Requirements](#requirements)   
2. [Quick install](#quick-install)   
3. [Install at Lawrencium](#lawrencium)   
4. [Install at Cori, NERSC](#cori)   

<a id='requirements'></a>
## Requirements

The following software and modules are required to use OPTpy.

  * abinit 7.10.5- (http://www.abinit.org)
  * python 2.7 (version 3 is not yet supported) 
  * numpy 1.6+      (http://www.scipy.org/)
  * pymatgen 3.0+   (http://pymatgen.org/)
  * Tiniba-v3+ (https://github.com/bemese/tiniba)

Note that the binary executables of Tiniba must be found
in your PATH environment variable.

<a id='quick-install'></a>
## Quick install

Once you have satisfied the requirements, install the package with

  python setup.py install

Here are some specific examples on how to install in Lawrencium and NERSC clusters.
Last update (July 2017)

<a id='lawrencium'></a>
## Lawrencium cluster (LBNL)

1. Load python modules  
```bash
module load python/2.7   
```

2. Make a virtual environment   
```bash
mkdir venv   
virtualenv venv  
``` 
This folder contains bin, include, lib   
```bash
source venv/bin/activate  
```
To deactivate type:  
```bash 
deactivate    
```

3. Upgrade packages, otherwise you get errors:   
```bash
pip install --upgrade pip
pip install --upgrade setuptools    
```

4. Install numpy numpy pymatgen  
```bash
pip install numpy   
pip install pymatgen 
```

5. Install OPTpy, under the OPTpy directory:  
```bash
svn checkout https://github.com/trangel/OPTpy.git   
cd OPTpy.git/trunk    
python setup.py install --force     
```

<a id='cori'></a>
## Cori cluster (NERSC)
(Benjamin M. Fregoso)
NERSC is no longer using pip, so better use conda.  

1. Create a virtual envirnment in $HOME/.conda  
```bash
module load python/2.7-anaconda 
conda create -n myenv python=2.7  
source activate myenv        
```

2. Install numpy and pymatgen
```bash
conda install numpy            
conda install --channel matsci pymatgen
pip install pyyaml   
pip install pyspglib   
```

3. Install OPTpy  
```bash
git clone  https://github.com/trangel/OPTpy.git  
cd OPTpy  
python setup.py install   
```
