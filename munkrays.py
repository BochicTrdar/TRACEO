#==================================================================
#  
#  TRACEO: Munk SSP
#  Faro, Seg 11 Abr 2022 16:38:28 WEST 
#  Written by Tordar
#  
#==================================================================

from os import system
import sys
from numpy import *
from scipy.io import *
from matplotlib.pyplot import *
from wtraceoinfil import *

system("rm -rf rco.mat")

case_title = '''Munk profile & ray trajectories''';

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

nati = 501

rati = linspace(rs-2,Rmax+2,nati)
zati = sin( (10*pi*rati/Rmax) )
zati = 200.0*zati*zati

altimetry  = array([rati,zati])
properties = array([0,0,0,0,0])
btype = "V"
ptype = "H"
units = "W"
itype = "2P"

surface_data = {"type":btype, "ptype":ptype, "units":units,"itype":itype,"x":altimetry,"properties":properties}

#==================================================================
#  
#  Define sound speed data:
#  
#==================================================================

np = 51

c = zeros( (np,np) )

ranges = linspace(0,Rmax,np)
depths = linspace(0,Dmax,np)
z1     = linspace(1000,2000,np)

c1 = 1500.0
B = 1.3e3; BxB = B*B
epsilon = 7.37e-3

for i in range(np):
    for j in range(np):
       eta = 2.0*( depths[j] - z1[i] )/B
       c[i,j]  = c1*( 1.0 + epsilon*( eta + exp( -eta ) - 1.0 ) )

ssp_data = {"cdist":"c(r,z)","cclass":"TABL","z":depths,"r":ranges,"c":c}

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

nbty = nati

rbty = linspace(rs-2,Rmax+2,nbty); aaux = ( rbty - 0.5*Rmax );  
zbty = -1500.0*exp( -aaux*aaux/1.0e9 ) + Dmax

bathymetry = array([rbty,zbty])

properties = array([1550.0,600.0,2.0,0.1,0.0])
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

rarray = array( [Rmax] )
zarray = array( [Dmax/2] )

miss = 100

output_data = {"ctype":"RCO","array_shape":"RRY","r":rarray,"z":zarray,"miss":miss}

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

data = loadmat('rco.mat')

rayname = 'ray00000'

thetas = data["ray_elev"]

nthetas = thetas.size

figure(1)
for i in range(1,nthetas+1):

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
plot(rati,-zati,color='b')
plot(rbty,-zbty,color='k')   
xlabel('Range (m)')
ylabel('Depth (m)')
title('TRACEO - Munk waveguide, ray coordinates')   
xlim(0,Rmax)
show()

print('done.')
