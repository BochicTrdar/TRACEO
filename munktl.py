#==================================================================
#  
#  TRACEO: Munk flat waveguide
#  Faro, Seg 11 Abr 2022 16:33:24 WEST 
#  Written by Tordar
#  
#==================================================================

from os import system
import sys
from numpy import *
from scipy.io import *
from matplotlib.pyplot import *
from wtraceoinfil import *

system("rm -rf cpr.mat")

case_title = '''Munk profile & transmission loss''';

#==================================================================
#  
#  Define source data:
#  
#==================================================================

freq   =  50
Rmaxkm = 100
Rmax   = Rmaxkm*1000
Dmax   = 5000

ray_step = 100

zs = 1000.0
rs =    0.0
thetamax = 14
nthetas =  51
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

depths = linspace(0,Dmax,1001)

c1 = 1500.0
z1 = 1300.0
B = 1.3e3; BxB = B*B
epsilon = 7.37e-3
eta = 2.0*( depths - z1 )/B
c   = 1.0 + epsilon*( eta + exp( -eta ) - 1.0 )

ssp_data = {"cdist":"c(z,z)","cclass":"TABL","z":depths,"r":array([0]),"c":c}

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

bathymetry = array([[rs-2,Rmax+2],[Dmax,Dmax]])

properties = array([1550.0,600.0,2.0,0.1,0.0])
btype = "E"
ptype = "H"
units = "W"
itype = "FL"

bottom_data = {"type":btype, "ptype":ptype, "units":units,"itype":itype,"x":bathymetry,"properties":properties}

#==================================================================
#  
#  Define output data:
#  
#==================================================================

nra = 501; rarray = array( linspace(0,Rmax,nra) ); rarraykm = rarray/1000
nza = 501; zarray = array( linspace(0,Dmax,nza) )

miss = 0.5

output_data = {"ctype":"CPR","array_shape":"RRY","r":rarray,"z":zarray,"miss":miss}

#==================================================================
#  
#  Call the function:
#  
#==================================================================

print('Writing TRACEO waveguide input file...')

wtraceoinfil("munk.in",case_title,source_data,surface_data,ssp_data,object_data,bottom_data,output_data)

print('Calling TRACEO...')

system('traceo.exe munk.in')

print('Reading the output data...')

data = loadmat('cpr.mat')

pressure = data["pressure"]
pressure = where( pressure == 0, nan, pressure )

tl = 20*log10( abs( pressure ) );

figure(1)
pcolor(rarraykm,zarray,tl,cmap='jet',vmin=-120,vmax=-50,shading='auto')
plot(rs,zs,marker="<",markersize=16,color="k")
colorbar()
xlim(0,Rmaxkm)
ylim(Dmax,0)
xlabel('Range (km)')
ylabel('Depth (m)')
title('TRACEO - Munk waveguide, TL')

show()

print('done.')
