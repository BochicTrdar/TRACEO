#==================================================================
#  
#  TRACEO: Munk SSP
#  Faro, Seg 11 Abr 2022 16:41:06 WEST 
#  Written by Tordar
#  
#==================================================================

from os import system
import sys
from numpy import *
from scipy.io import *
from matplotlib.pyplot import *
from wtraceoinfil import *

system("rm -rf eig.mat")

case_title = '''Munk profile & eigenrays''';

#==================================================================
#  
#  Define source data:
#  
#==================================================================

freq   =  50
Rmaxkm = 101
Rmax   = Rmaxkm*1000
Dmax   = 5000

ray_step = 100

zs = 1000.0
rs =    0.0
thetamax = 14
nthetas =  101
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

rarray = array( [100*1000] )
zarray = array( [zs] )

miss = 100

output_data = {"ctype":"ERF","array_shape":"RRY","r":rarray,"z":zarray,"miss":miss}

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

data = loadmat('eig.mat')

rayname = 'ray00000'

neigrays = int( data["neigrays"] )

figure(1)
for i in range(1,neigrays+1):

   if i < 10:
      rayname = 'ray0000' + str(i)
   elif i < 100:
      rayname = 'ray000'  + str(i)
   elif i < 1000:
      rayname = 'ray00'   + str(i)
   elif i < 10000:
      rayname = 'ray0'    + str(i)
   else:
      rayname = 'ray'     + str(i)   

   rayi = data[rayname]
   
   r =  rayi[0,]
   z = -rayi[1,]
   plot(r,z)

xlabel('Range (m)')
ylabel('Depth (m)')
title('TRACEO - Munk waveguide, eigenrays')   
xlim(0,Rmax)
grid(True)
show()

print('done.')
