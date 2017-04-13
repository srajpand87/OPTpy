#from OPTpy import abinittask
from os import path, mkdir,chdir
from OPTpy import Structure #..external 

class KKflow(Workflow):
    def __init__(self,**kwargs):
    ''' keyword arguments:
        structure : pymatgen.Structure
            Structure object containing information on the unit cell.
    '''
    super(KKflow, self).__init__(**kwargs)
    self.structure = kwargs['structure']

#Create KK directory:
#Directory of the script being run:
dirname=path.dirname(path.abspath(__file__))
newdir="KK"
KKdir=path.join(dirname,newdir)
if not path.exists(KKdir):
    mkdir(KKdir)

#Change dir:
chdir(KKdir)

#Make class: KK
#Copy from GWflow, and add required variables for abinit input.
#Make an instance of the class here.

flow = KKflow(
   structure=Structure.from_file('../../Data/GaAs.json')
)

#super(AbinitTask, self).__init__(dirname, **kwargs)

#self.ngkpt  = kwargs.get('ngkpt', 3*[1])
#self.kshift = kwargs.get('kshift', 3*[.0])
#self.qshift = kwargs.get('qshift', 3*[.0])

#self.prefix = kwargs.get('prefix', 'abinit')

#self.input = AbinitInput(fname=self.prefix + '.in')
#self.input.set_structure(self.structure)

#Now run symmetries using self.structure?

#pymatgen.symmetry.analyzer module
#get_symmetry_operations(cartesian=False)[source]
#Return symmetry operations as a list of SymmOp objects. By default returns fractional coord symmops. But cartesian can be returned too.

#Returns:	List of symmetry operations.
#Return type:	([SymmOp])

