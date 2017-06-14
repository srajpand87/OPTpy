from OPTpy import KKflow
from OPTpy import Structure

flow = KKflow(
   prefix="gaas",
   structure=Structure.from_file('../data/structures/GaAs.json'),
   kgrid_response=[4,4,4],
)
flow.write()

