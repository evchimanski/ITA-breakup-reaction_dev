# Transform cross section from CM to LAB 
# Emanuel V Chimanski Aug 20 2020
# It reads in xcm,ycm and m1, m2 and it prints out xlab, ylab
# tau = m1/m2: if tau > 0.2 we might find differences between the two frams.
# Attention the calculation here assumes elastic scattering m2(m1,m1)m2 

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.optimize import root
from scipy.interpolate import interp1d

def get_interp(x,f,xmin,xmax):
	xout=0.
	if x >= xmin and x <= xmax:xout=f(x)

#	if x > xmax:x=xmax
#	if x < xmin:x=xmin
	return xout

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


def get_angle(deg,flag):
	xr=deg*np.pi/180.
	xguess=xr
	if flag == 'LAB':
		c=lhs(xr)
		rts=getroot(xguess,c,m1,m2,flag)
		print("input: ANG LAB=",deg," output: ANG CM=",rts)
		anglab=deg
		angcm=rts

	if flag == 'CM':
		c=rhs(m1,m2,xr)
		rts=getroot(xguess,c,m1,m2,flag)
		print("input: ANG CM=",deg," output: ANG LAB=",rts)	
		anglab=rts
		angcm=deg
	return rts

def transform(f,xcm,ycm,m1,m2,deg):
	xf=[];yf=[]
	xmin=min(xcm);xmax=max(xcm)
	
	flag='CM'
	tau=m1/m2
	print("tau=",tau)
	if tau > 0.3 and tau < 1.:
		print(tau)
		print(bb)
		
	angLAB=get_angle(deg,flag)
	
	q0=1.+tau*np.cos(angCM*np.pi/180.)
	fact1=((np.sin(angCM*np.pi/180.)/np.sin(angLAB*np.pi/180.))**3)/q0
	fac2 = m2/(m1+m2)
	for i in range(0,len(xcm)):
		x0=xcm[i]/fac2
		y0=ycm[i]*fact1
		xf.append(x0)
		yf.append(y0)
		
	
	return(xf,yf,angLAB)


f1 = open('input.inp', 'r')
n=0
for line in f1:
    p = line.split()
    if n==0 : m1=float(p[0]);m2=float(p[1])
    if n==1 : angCM=float(p[0])
    if n==2 : xfile=p[0]
    if n==3 : xind=p[0];yind=p[1]
    if n==4 : outfile=p[0]
 
    n=n+1
    
f1.close()

DATA=np.loadtxt('%s'%xfile) # this is in the CM frame
xcm=DATA[:,1]
ycm=DATA[:,8]


f = interp1d(xcm, ycm)

(xlab,ylab,angLAB) = transform(f,xcm,ycm,m1,m2,angCM)

fout=open('%s'%outfile,'w')

# current date and time
now = datetime.now()
print("# %s "%(now),file=fout)
print("#projectile mass = %s     target mass = %s "%(m1,m2),file=fout)
print("#ANG LAB [deg] = %4.3f    ANG CM [deg] = %4.3f"%(angLAB,angCM),file=fout)
print("#x(LAB)   y(LAB)",file=fout)
for i in range(0,len(xlab)):
	print("%4.3e %4.3e"%(xlab[i],ylab[i]),file=fout)
	
fout.close()

