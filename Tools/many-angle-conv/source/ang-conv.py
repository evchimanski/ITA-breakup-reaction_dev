# Transform Angles from CM to LAB or LAB to CM
# input.inp
# 3.	12. # projectile mass (m1) target mass (m2)
# 83.5 CM #   or 70. LAB
# Emanuel V Chimanski Aug 15 2020
#
import numpy as np

from scipy.optimize import root

def getroot(xguess,c,m1,m2,flag):
	if flag == 'LAB': sols = root(fgetCM,xguess,args=(m1,m2,c))
	if flag == 'CM' : sols = root(fgetLAB,xguess,args=(c))
	rts=sols.x
	rts=rts*180./np.pi
	mes=sols.message

	return rts

def rhs(m1,m2,theta):
	
	return np.sin(theta)/(np.cos(theta)+m1/m2)

def lhs(psi):
	return np.tan(psi)
    
def fgetCM(theta,m1,m2,c):
	return rhs(m1,m2,theta)-c

def fgetLAB(theta,c):
	return lhs(theta)-c

f1 = open('input.inp', 'r')

n=0
for line in f1:
    p = line.split()
    if n==0 : m1=float(p[0]);m2=float(p[1]) # projectile mass (m1) target mass (m2)
    if n==1 : deg=float(p[0]);flag='%s'%p[1]
    if n==2 : initheta=int(p[0]); fintheta=int(p[1]); delta=int(p[2])
	
    n=n+1
    
f1.close()

fout = open('ang_out.out','w')
print("ANG LAB   ANG CM",file=fout)

xr=deg*np.pi/180.
xguess=xr
if flag == 'LAB':
    if deg<=0 : 
        i=0
        for i in range(int((fintheta-initheta)/delta + 1)):
          degaux=float(i*delta+initheta)
          c=lhs(degaux*np.pi/180.)
          rts=getroot(degaux*np.pi/180.,c,m1,m2,flag)
          print("input: ANG LAB=",degaux," output: ANG CM=",rts)
          
          anglab=degaux
          angcm=rts  
          print("%4.3f   %4.3f"%(anglab,angcm),file=fout)
    
    else :
         c=lhs(xr)
         rts=getroot(xguess,c,m1,m2,flag)
         print("input: ANG LAB=",deg," output: ANG CM=",rts)
         
         anglab=deg
         angcm=rts 
         print("%4.3f   %4.3f"%(anglab,angcm),file=fout)
         
         

if flag == 'CM':
    if deg<=0 : 
        i=0
        for i in range(int((fintheta-initheta)/delta + 1)):
          degaux=float(i*delta+initheta)
          xr = degaux*np.pi/180.
          c=rhs(m1,m2,xr)
          rts=getroot(xr,c,m1,m2,flag)
          
          anglab=rts
          angcm=degaux

          
          print("input: ANG CM=",angcm," output: ANG LAB=",anglab)
 
          print("%4.3f   %4.3f"%(anglab,angcm),file=fout)
    
    else :
         
         c=rhs(m1,m2,xr)
         rts=getroot(xr,c,m1,m2,flag)
          
         anglab=rts
         angcm=xr
          
         print("input: ANG CM=",angcm," output: ANG LAB=",anglab)

         print("%4.3f   %4.3f"%(anglab,angcm),file=fout)
          
	

print("projectile mass = %s     target mass = %s "%(m1,m2))
fout.close()
