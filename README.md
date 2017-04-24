
A python module to operate Tiniba (Under construction).


Documentation
-------------

This repository is a python script with automatic workflows to compute optical responses of materials.
The script can read geometry data from material sciences repositories as PyMatGen, and other common file formats.

Below we show an example of calculation obtained with this script. 

 
<div class="image">
<a href="url"><img src="https://github.com/trangel/OPTpy/blob/master/doc/figures/GeS-responses.png" height="300" ></a><br clear="all" />
<div>Optical spectra calculated with OPTpy and Tiniba.<br>
<small> Shift current (top) and linear absorption (bottom).
See <a href="https://arxiv.org/abs/1610.06589">Rangel et a., 2017.</a>
</small>
</div>
</div>



Requirements
------------

The following software and modules are required to use OPTpy.

  * python 2.7 required (Python 3 not supported at the moment) 
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


License
-------

This software is free to use under the BSD license.
See license.txt for more information.

