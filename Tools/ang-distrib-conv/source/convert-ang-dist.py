# Transform cross section from CM to LAB 
# Emanuel V Chimanski Aug 20 2020
# It reads in xcm,ycm and m1, m2 and it prints out xlab, ylab
# tau = m1/m2: if tau > 0.2 we might find differences between the two frams.
# Attention the calculation here assumes elastic scattering m2(m1,m1)m2 
# July 5 2021:
# This reads in angular distributions and convert it following user request
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.optimize import root
from scipy.interpolate import interp1d


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

def transform(xcm,ycm,m1,m2,deg):
	
	flag='CM'
	tau=m1/m2
	print("tau=",tau)
	if tau > 0.3 and tau < 1.:
		print(tau)
		print(bb)
		

	angLAB=get_angle(deg,flag)
	angLAB=float(angLAB[0])

	if deg == 0.:
		deg=0.0001
		angLAB=deg
	
	q0=1.+tau*np.cos(deg*np.pi/180.)

	fact1=((np.sin(deg*np.pi/180.)/np.sin(angLAB*np.pi/180.))**3)/q0
	fac2 = m2/(m1+m2)

	
	xf=xcm/fac2
	yf=ycm*fact1
		
	return(xf,yf,angLAB)


def read_data(xfile):
	print(xfile)
	
	Ecm=0
	angcm=[];sigcm_EB=[];sigcm_NEB=[];sigcm_INC=[]	
	
	with open('%s'%xfile, mode='r') as rfile:
		for row in rfile:
			line=row.split()
			if '#' not in row:
				if Ecm == 0:
					Ecm=float(line[0])
				 
				else:
					angcm.append(float(line[0]))
					sigcm_EB.append(float(line[4]))
					sigcm_NEB.append(float(line[5]))
					sigcm_INC.append(float(line[6]))
					
	return Ecm,np.array(angcm),np.array(sigcm_EB),np.array(sigcm_NEB),np.array(sigcm_INC)
	
	

f1 = open('input.inp', 'r')
n=0
for line in f1:
    p = line.split()
    if n==0 : m1=float(p[0]);m2=float(p[1])
    if n==1 : xfile=p[0]
    if n==2 : outfile=p[0]
 
    n=n+1
    
f1.close()

(Ecm,angCM,sigCM_EB,sigCM_NEB,sigCM_INC)=read_data(xfile) # this is in the CM frame

Anglab=[]
siglab_EB=[]
siglab_NEB=[]
siglab_INC=[]

Elab=[]

for i in range(0,len(angCM)):
	angCM0=angCM[i]
	
	ycm=sigCM_EB[i]
	xcm=Ecm
	(xlab,ylab,angLAB) = transform(xcm,ycm,m1,m2,angCM0)
	siglab_EB.append(ylab)

	ycm=sigCM_NEB[i]
	xcm=Ecm
	(xlab,ylab,angLAB) = transform(xcm,ycm,m1,m2,angCM0)
	siglab_NEB.append(ylab)

	ycm=sigCM_INC[i]
	xcm=Ecm
	(xlab,ylab,angLAB) = transform(xcm,ycm,m1,m2,angCM0)
	siglab_INC.append(ylab)
	
	Anglab.append(angLAB)
	Elab.append(xlab)


fout=open('%s'%outfile,'w')

print(len(Elab),len(Anglab),len(siglab_EB),len(siglab_NEB),len(siglab_INC))
# current date and time
now = datetime.now()
print("# %s "%(now),file=fout)
print("#projectile mass = %s     target mass = %s "%(m1,m2),file=fout)
print("#E LAB [MeV] ANG(LAB) SIGEB(LAB)  SIGNEB(LAB)  SIGINC(LAB)",file=fout)
print(len(Elab))
for i in range(0,len(Elab)):
	x1=float(Elab[i])
	x2=float(Anglab[i])
	x3=float(siglab_EB[i])
	x4=float(siglab_NEB[i])
	x5=float(siglab_INC[i])
	print("%8.4e %8.4e %8.4e %8.4e %8.4e"%(x1,x2,x3,x4,x5),file=fout)

fout.close()

