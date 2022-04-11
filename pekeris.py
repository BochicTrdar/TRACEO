#==================================================================
#  
#  TRACEO: Pekeris flat waveguide
#  Faro, Seg 11 Abr 2022 11:56:25 WEST 
#  Written by Tordar
#  
#==================================================================

from os import system
from numpy import *
from scipy.io import *
from matplotlib.pyplot import *
from wtraceoinfil import *

system("rm -rf cpr.mat")

case_title = "Pekeris waveguide & TL calculation"

#==================================================================
#  
#  Define source data:
#  
#==================================================================

freq   = 100
Rmaxkm =  5.0
Rmax   = Rmaxkm*1000
Dmax   = 1000

ray_step = 5

zs = 500.0
rs =  0.0
thetamax = 20
nthetas = 301
thetas = linspace(-thetamax, thetamax, nthetas)
position = array([rs,zs])
rbox     = array([rs-1,Rmax+1])

source_data = {"ds":ray_step, "position":position, "rbox":rbox,"f":freq,"thetas":thetas}

#==================================================================
#  
#  Define altimetry data:
#  
#==================================================================

altimetry  = array([[rs-2,Rmax+2],[0,0]])
properties = array([0,0,0,0,0])
btype = "V"
ptype = "H"
units = "W"
itype = "FL"

surface_data = {"type":btype, "ptype":ptype, "units":units,"itype":itype,"x":altimetry,"properties":properties}

#==================================================================
#  
#  Define sound speed data:
#  
#==================================================================

c0 = 1500

ssp_data = {"cdist":"c(z,z)","cclass":"ISOV","z":array([0,Dmax]),"r":array([0]),"c":array([c0,c0])}

#==================================================================
#  
#  Define object data:
#  
#==================================================================

npo = array([0])

robj = 0
zup  = 0
zdn  = 0

x = array( [robj,zup,zdn] )
 
xobj = array( [ x ] ) 

properties = [0,0,0,0,0]
oproperties = array([properties])

btype = "R"
units = "W"
itype = "2P"

object_data = {"nobjects":0,"itype":itype,"type":btype,"x":xobj,"units":units,"properties":oproperties,"npobjects":npo}

#==================================================================
#  
#  Define bathymetry data:
#  
#==================================================================

bathymetry = array([[rs-2,2000,2010,2990,3000,Rmax+2],[Dmax,Dmax,500,500,Dmax,Dmax]])

properties = array([2000.0,0.0,2.0,0.5,0.0])
btype = "E"
ptype = "H"
units = "W"
itype = "2P"

bottom_data = {"type":btype, "ptype":ptype, "units":units,"itype":itype,"x":bathymetry,"properties":properties}

#==================================================================
#  
#  Define output data:
#  
#==================================================================

nra = 201; rarray = array( linspace(0,Rmax,nra) )
nza = 201; zarray = array( linspace(0,Dmax,nza) )

miss = 0.5

output_data = {"ctype":"CPR","array_shape":"RRY","r":rarray,"z":zarray,"miss":miss}

#==================================================================
#  
#  Call the function:
#  
#==================================================================

print('Writing TRACEO waveguide input file...')

wtraceoinfil("pekeris.in",case_title,source_data,surface_data,ssp_data,object_data,bottom_data,output_data)

print('Calling TRACEO...')

system('traceo.exe pekeris.in')

print('Reading the output data...')

data = loadmat('cpr.mat')

pressure = data["pressure"]
pressure = where( pressure==0, nan, pressure )

tl = -20*log10( abs( pressure ) );

figure(1)
pcolor(rarray,zarray,tl,cmap='jet_r',vmin=60,vmax=90,shading='auto')
fill_between(bathymetry[0,],bathymetry[1,],Dmax)
colorbar()
plot(rs,zs,marker="<",markersize=16,color="k")
xlim(0,Rmax)
ylim(Dmax,0)
xlabel('Range (m)')
ylabel('Depth (m)')
title('TRACEO - Pekeris waveguide, TL')

show()

print("done.")
