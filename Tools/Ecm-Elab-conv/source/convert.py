import numpy as np


f1 = open('input.inp', 'r')
n=0
for line in f1:
    p = line.split()
    if n==0 : Mt=float(p[0]);Mp=float(p[1])
    if n==1 : flagin=p[0];Ein=float(p[1])
 
    n=n+1
    
f1.close()

out=0.
if flagin == 'LAB':
	out=Mt/(Mp+Mt)
	Eout=out*Ein
	flagout='CM'

out=0.
if flagin == 'CM':
	out=Mt/(Mp+Mt)
	Eout=Ein/out
	flagout='LAB'
	

f2 = open('output.out','w')

print('%s %s   #Mtarget Mprojectile'%(Mt,Mp),file=f2)

print('%s %s  '%(flagin,Ein),file=f2)
print('%s %s  '%(flagout,Eout),file=f2)

f2.close()
