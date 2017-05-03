from OPTpy import RPMNSflow
from OPTpy import Structure

flow = RPMNSflow(
   nval=8,
   ecut=5.0,
   nspinor=1,
   nkTetra=5, 
)
flow.write()


