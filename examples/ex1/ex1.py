from OPTpy import KKflow
from OPTpy import Structure

flow = KKflow(
   case="gaas",
   structure=Structure.from_file('../data/structures/GaAs.json'),
   grid_response=[4,4,4],
)
flow.write()

