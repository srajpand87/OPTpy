import numpy as np

#Read file1:
file1="symmetries/sym.d"
file2="SCF/gaas.out"

#Read symmetries from file1
f=open(file1,"r")
lines = f.readlines()
f.close()

nsym=np.int(lines[0])
#print("nsym = "+str(nsym))

sym=np.zeros((nsym,9),dtype=np.int)
for ii in range(0,nsym): 
    sym[ii][:]=np.array(lines[ii+1].split(),dtype=np.int)

#Read symmetries from file2:
state=0
f=open(file2,"r")
for line in f.readlines():
    line2=line.strip()
    if ( state == 0 ):
        if (line2.startswith("nsym")):
            token=line2.split()
            nsym2=np.int(token[2])
            #print("nsym2 = "+str(nsym2))
            sym2=np.zeros((nsym2,9),dtype=np.int)
            state=1
    elif ( state == 1 ):
        if (line2.startswith("symrel")):
            token=line2.split()
            sym2[0][:]=np.array(token[1:10],dtype=np.int)
            isym=1
            if  ( nsym2 > 1 ):
               sym2[1][:]=np.array(token[10:],dtype=np.int)
               isym=2
            state=2
    elif ( state == 2 ):
       token=line2.split()
       sym2[isym][:]=np.array(token[0:9],dtype=np.int)
       isym=isym+1
       if ( isym < nsym2 ):
           sym2[isym][:]=np.array(token[9:],dtype=np.int)
           isym=isym+1
       if ( isym == nsym2 ):
           state=3
f.close()
#print(sym2)
#Compare symmetries
if ( nsym != nsym2 ):
    print("Error found number of symmetries differ\n")
    print("%d symmetries found in %s\n" % (nsym,file1)) 
    print("%d symmetries found in %s\n" % (nsym2,file2))

for isym in range(nsym):
    syma=sym[isym][:]
    syma=np.array(syma,dtype=np.int)
    found=False
    for jsym in range(nsym2):
        symb=sym2[jsym][:]
        symb=np.array(symb,dtype=np.int)
        diff=sum(abs(syma-symb))
        if ( diff == 0 ):
            found=True
            symeqv=symb
    if ( found ):
        print("Sym %d:" % (isym))
        print(syma)
        print(symeqv)
    else:
        print("Error: symmetry not found\n")
        print(syma)
        exit(1)
         
