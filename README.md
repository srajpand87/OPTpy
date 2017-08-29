
A python module to operate <a href="https://github.com/bemese/tiniba">Tiniba</a>.


Documentation
-------------

This repository is a python script with automatic workflows to compute optical responses of materials.
The script can read geometry data from material sciences repositories as PyMatGen, and other common file formats.
See a list of examples in the "examples" directory.


Below we show an example of calculation obtained with this script. 

 
<div class="image">
<a href="url"><img src="https://github.com/trangel/OPTpy/blob/master/doc/figures/GeS-responses.png" height="300" ></a><br clear="all" />
<div>Optical spectra calculated with OPTpy and Tiniba.<br>
<small> Shift current (top) and linear absorption (bottom).
See <a href="https://arxiv.org/abs/1610.06589">Rangel, M. Fregoso et al., 2017.</a>
</small>
</div>
</div>



Requirements
------------

The following software and modules are required to use OPTpy.

  * python 2.7 (version 3 is not yet supported) 
  * numpy 1.6+      (http://www.scipy.org/)
  * pymatgen 3.0+   (http://pymatgen.org/)
  * Tiniba-v3+ (https://github.com/bemese/tiniba)

Note that the binary executables of Tiniba must be found
in your PATH environment variable.


Installing
----------

Once you have satisfied the requirements, install the package with

  python setup.py install

See the file INSTALL for more information about configuring
the module's default parameters.


Here are some specific examples on how to install in Lawrencium and NERSC clusters.
Last update (July 2017)

**Lawrencium**

1. Load python modules  
module swap intel gcc   
module load python/2.7.8   
module load virtualenv   
  
2. Make a virtual environment   
mkdir venv   
virtualenv venv   
        — this folder contains bin, include, lib   
source venv/bin/activate   
        — to deactivate type:   
                deactivate    

3. Upgrade packages, otherwise you get errors:   
pip install --upgrade setuptools    
pip install --upgrade pip

4. Install numpy numpy pymatgen  
pip install numpy
pip install pymatgen 

5. Install OPTpy, under the OPTpy directory:  
python setup.py install


**NERSC**  
(Benjamin M. Fregoso)
NERSC is no longer using pip, so better use conda.  

1. Create a virtual envirnment in $HOME/.conda  
module load python/2.7-anaconda 
conda create -n myenv python=2.7  
source activate myenv        

2. Install numpy and pymatgen
conda install numpy            
conda install --channel matsci pymatgen
pip install pyyaml   
pip install pyspglib   

3. Install OPTpy  
git clone  https://github.com/trangel/OPTpy.git  
cd OPTpy  
python setup.py install   

License
-------

This software is free to use under the BSD license.
See license.txt for more information.

