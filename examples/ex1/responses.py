from OPTpy import RESPONSESflow

flow = RESPONSESflow(
   case="gaas",
   lt="total",
#  Total number of bands in the NSCF calculation:
   nband=18,
#  Total number fo valence bands:
   nval_total=8,
#  Number of valence and conduction bands to compute the response:
#  These could be less than the total number of bands.
   ncond=8,
   nval=8,
#  Number of k-points in the tetrahedra file: 
   nkTetra=5,
#  Number of spinorial components:
   nspinor=1,
#  Kinetic energy cutoff (Ha):
   ecut=5.0,
#  Response to calculate, see Doc. in responses.py
   response=1,
   components=["xx","yy","zz"],
   vnlkss=False,
   option=1, #Full
   smearvalue=0.15,
)
flow.write()

#---------  choose a response ---------
#1  chi1----linear response           24 calChi1-layer linear response     
#3  eta2----bulk injection current    25 calEta2-layer injection current   
#41 zeta----bulk spin injection       29 calZeta-layer spin injection      
#21 shg1L---Length gauge-1w&2w faster 22 shg2L---Length gauge-2w           
#42 shg1V---Velocity gauge-1w&2w      43 shg2V---Velocity gauge-2w         
#44 shg1C---Layer-Length gauge-1w&2w  45 shg2C---Layer-Length gauge-2w     
#26 ndotccp-layer carrier injection   27 ndotvv--carrier injection   


