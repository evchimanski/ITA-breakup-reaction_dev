##
## Emanuel Chimanski 07 May 2020
## May 23 2020 fixed the order of ws parameters and remove the flags
##
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
from random import *
from scipy.optimize import curve_fit


font = {'size'   : 10}

plt.rc('font', **font)

listcolors = ['blue','green','red','gray']

def WoodSaxon(r,WS,aWS,rWS):
	#return WS/(1.+np.exp((r-(rWS*At13))/aWS))
	return WS/(1.+np.exp((r-rWS)/aWS))

def get_rcm_Ur():
	# just read potential from the file or creates a random WSparameters potential
	#Sample data
	DATA=np.loadtxt('potential.dat')
	x0=DATA[:,0]
	y0=DATA[:,1]
	rcm=x0
	nrcm=len(rcm)
	Ur=y0

	return (rcm,Ur)
	


################### READ INPUTS ##############################
f1 = open('input.inp', 'r')
i=0
for line in f1:

	p = line.split()
	if i == 0:Zt=int(p[0]);At=int(p[1])
	if i == 1:rWSmin=float(p[0]);rWSmax=float(p[1])
	if i == 2:DeltaV0=float(p[0])
	if i == 3:aWSmin=float(p[0]);aWSmax=float(p[1])
		
	i+=1



print("A=",At,"Z=",Zt)
	

At13=At**(1./3.)

(rcm,Ur)  = get_rcm_Ur()
plt.plot(rcm,Ur,'x',label=r"original: Targ$^{%s}_{%s}$"%(At,Zt),color='black')

## print fit ##
rr=np.linspace(0.1,15,500) # CM

# set bounds for strenght parameter-fit range
VWSmin=min(Ur)-DeltaV0;VWSmax=min(Ur)+DeltaV0

myfile = open("fitted_parameters.dat", 'w')
		
# perform the best fit
#Constrain the optimization to the defined region region :
popt, pcov = curve_fit(WoodSaxon, rcm, Ur, bounds=([VWSmin, aWSmin, rWSmin], [VWSmax, aWSmax, rWSmax]))
chi2=np.sqrt(sum((Ur-WoodSaxon(rcm, *popt))**2)/len(rcm))		
V0=popt[0];a0=popt[1];R=popt[2]
print("result:")
print(V0,R,a0,chi2)
		
plt.plot(rr, WoodSaxon(rr, *popt), '--',color='gray', label='best: $\chi ^{2}$=%5.3f $V_{0}$=%5.3f, $a_{0}$=%5.3f, $R$=%5.3f' %(chi2,popt[0],popt[1],popt[2]))

print("  V0          a0          R0          r0=R0/At^(1/3) ",file=myfile)

r0=R/At13

#R=r0*A13 -0.83
#r00=(R - 0.83)/At13


print("%4.3f      %4.3f       %4.3f       %4.3f"%(V0,a0,R,r0),file=myfile)

print("  W0(0.78*V0) a0          R0          r0=R0/At^(1/3) ",file=myfile)
print("%4.3f      %4.3f       %4.3f       %4.3f"%(V0*0.78,a0,R,r0),file=myfile)


print("RAIOS",r0,r0*At13,R)

myfile.close()

plt.xlabel('r (fm)')
plt.ylabel('V(r) (MeV)')

plt.legend()

#W0=-10
#a0=0.65
#r0=1.22

#plt.plot(rcm,WoodSaxon(rcm,W0,a0,r0,Ap,At),'-',color="black")

plt.xlim(0,15)

plt.savefig('fig.pdf',bbox_inches='tight')
