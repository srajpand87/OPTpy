from OPTpy import RPMNSflow
from OPTpy import Structure

flow = RPMNSflow(
   nval_total=4,   # Number of valence bands
   ecut=5.0,       # Kinetic-energy cutoff
   nspinor=1,      # Number of spinorial components
   nkTetra=5,      # k-grid for tetrahedrum integration
)
flow.write()


