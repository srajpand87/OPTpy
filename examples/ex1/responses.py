from OPTpy import RESPONSESflow

flow = RESPONSESflow(
   case="gaas",
   lt="total",
   nband=18,
   nval_total=8,
#  The number of bands to calculate the response could be less than the total number of bands above:
   ncond=8,
   nval=8,
#
   ecut=5.0,
   nspinor=1,
   nkTetra=5,
   scissors=0,
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


