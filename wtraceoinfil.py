def wtraceoinfil(filename=None, thetitle=None, source_info=None, surface_info=None, ssp_info=None, object_info=None, bathymetry_info=None, output_info=None):

    # Writes Traceo input (waveguide) file. 
    #
    # SYNTAX: wtraceoinfil( filename, title, source, surface, ssp, object, bottom, output )
    #

    #*******************************************************************************
    # Arraial do Cabo, Qui Out  6 16:01:06 WEST 2016
    # Written by Simone Pacheco and Orlando Camargo Rodriguez
    #*******************************************************************************
    
    separation_line = "--------------------------------------------------------------------------------"
    
    #*******************************************************************************
    # Get source data: 

    ds = source_info["ds"]
    xs = source_info["position"]
    rbox = source_info["rbox"]
    freq = source_info["f"]
    thetas = source_info["thetas"]
    nthetas = thetas.size

    theta1 = thetas[0]
    thetan = thetas[nthetas-1]

    #*******************************************************************************
    # Get surface data: 

    atype = surface_info["type"]
    aptype = surface_info["ptype"]
    aitype = surface_info["itype"]
    xati = surface_info["x"]
    nati = xati[0,].size

    atiu = surface_info["units"]
    aproperties = surface_info["properties"]

    #*******************************************************************************
    # Get sound speed data: 

    cdist  = ssp_info["cdist"]
    cclass = ssp_info["cclass"]

    c = ssp_info["c"]
    z = ssp_info["z"]
    r = ssp_info["r"]

    #*******************************************************************************
    # Get object data:

    nobj = object_info["nobjects"]

    if nobj > 0:
        npobj = object_info["npobjects"]
        otype = object_info["type"]
        oitype = object_info["itype"]
        xobj = object_info["x"]
        obju = object_info["units"]
        oproperties = object_info["properties"]

    #*******************************************************************************  
    # Get bathymetry data:

    btype = bathymetry_info["type"]
    bptype = bathymetry_info["ptype"]
    bitype = bathymetry_info["itype"]
    xbty = bathymetry_info["x"]
    nbty = xbty[0,].size
    btyu = bathymetry_info["units"]
    bproperties = bathymetry_info["properties"]

    #*******************************************************************************  
    # Get output options: 

    calc_type = output_info["ctype"]
    array_shape = output_info["array_shape"]
    array_r = output_info["r"]
    array_z = output_info["z"]
    array_miss = output_info["miss"]

    m = array_r.size
    n = array_z.size

    #*******************************************************************************  
    # Write the INFIL: 

    fid = open(filename, 'w')
    fid.write('\'');fid.write(thetitle);fid.write('\'\n')
    fid.write(separation_line);fid.write("\n")
    
    fid.write(str(ds))
    fid.write("\n")
    fid.write(str(xs[0]))
    fid.write(" ")
    fid.write(str(xs[1]))
    fid.write("\n")
    fid.write(str(rbox[0]))
    fid.write(" ")
    fid.write(str(rbox[1]))
    fid.write("\n")
    fid.write(str(freq))
    fid.write("\n")
    fid.write(str(nthetas))
    fid.write("\n")
    fid.write(str(theta1))
    fid.write(" ")
    fid.write(str(thetan))     
    fid.write("\n")
    fid.write(separation_line);fid.write("\n")
    fid.write('\'');fid.write(atype) ;fid.write('\'\n')
    fid.write('\'');fid.write(aptype);fid.write('\'\n')
    fid.write('\'');fid.write(aitype);fid.write('\'\n')
    fid.write('\'');fid.write(atiu)  ;fid.write('\'\n')
    fid.write(str(nati))
    fid.write("\n")
    
    if aptype == 'H':
       fid.write(str(aproperties[0]));fid.write(" ")
       fid.write(str(aproperties[1]));fid.write(" ")
       fid.write(str(aproperties[2]));fid.write(" ")
       fid.write(str(aproperties[3]));fid.write(" ")
       fid.write(str(aproperties[4]));fid.write('\n')
       for i in range(nati):
          fid.write(str(xati[0][i]));fid.write(" ")
	  fid.write(str(xati[1][i]));fid.write('\n')
    elif aptype == 'N':
       for i in range(nati):
          fid.write(str(xati[0][i]));fid.write(" ")
	  fid.write(str(xati[1][i]));fid.write(" ")
          fid.write(str(aproperties[0][i]));fid.write(" ")
          fid.write(str(aproperties[1][i]));fid.write(" ")
          fid.write(str(aproperties[2][i]));fid.write(" ")
          fid.write(str(aproperties[3][i]));fid.write(" ")
          fid.write(str(aproperties[4][i]));fid.write('\n')	  	  
    else:
       print('Unknown surface properties...')

    fid.write(separation_line);fid.write("\n")
    fid.write('\'');fid.write(cdist) ;fid.write('\'\n')
    fid.write('\'');fid.write(cclass);fid.write('\'\n')
    if cdist == 'c(z,z)':
       nz = z.size
       fid.write('1 ');fid.write(str(nz));fid.write('\n')
       for i in range(nz):
          fid.write(str(z[i]));fid.write(" ")
	  fid.write(str(c[i]));fid.write('\n')    
    elif cdist == 'c(r,z)':
       nz = z.size
       nr = r.size
       fid.write(str(nr));fid.write(" ")
       fid.write(str(nz));fid.write('\n')
       for i in range(nr):
          fid.write(str(r[i]));fid.write(" ")
       fid.write('\n')  
       for i in range(nz):
          fid.write(str(z[i]));fid.write(" ")
       fid.write('\n')
       for i in range(nz):
           for j in range(nr):
	      fid.write(str(c[i,j])),fid.write(" ")
	   fid.write("\n")
    else:
       print('Unknown sound speed distribution...')
    fid.write(separation_line);fid.write("\n")
    fid.write(str(nobj));fid.write("\n")
    if nobj > 0:
       fid.write('\'');fid.write(oitype);fid.write('\'\n')
       for i in range(nobj):
          fid.write('\'');fid.write(otype[i]);fid.write('\'\n')
          fid.write('\'');fid.write( obju[i]);fid.write('\'\n')
	  fid.write(str(npobj[i]));fid.write('\n')
	  fid.write(str(oproperties[i][0]));fid.write(" ")
          fid.write(str(oproperties[i][1]));fid.write(" ")
          fid.write(str(oproperties[i][2]));fid.write(" ")
          fid.write(str(oproperties[i][3]));fid.write(" ")
          fid.write(str(oproperties[i][4]));fid.write('\n')
	  for j in range(npobj[i]):
	     fid.write(str(xobj[i][0][j]));fid.write(" ")
	     fid.write(str(xobj[i][1][j]));fid.write(" ")
	     fid.write(str(xobj[i][2][j]));fid.write("\n")
    fid.write(separation_line);fid.write("\n")
    
    fid.write('\'');fid.write(btype) ;fid.write('\'\n')
    fid.write('\'');fid.write(bptype);fid.write('\'\n')
    fid.write('\'');fid.write(bitype);fid.write('\'\n')
    fid.write('\'');fid.write(btyu)  ;fid.write('\'\n')
    fid.write(str(nbty))
    fid.write("\n")
    
    if aptype == 'H':
       fid.write(str(bproperties[0]));fid.write(" ")
       fid.write(str(bproperties[1]));fid.write(" ")
       fid.write(str(bproperties[2]));fid.write(" ")
       fid.write(str(bproperties[3]));fid.write(" ")
       fid.write(str(bproperties[4]));fid.write('\n')
       for i in range(nbty):
          fid.write(str(xbty[0][i]));fid.write(" ")
	  fid.write(str(xbty[1][i]));fid.write('\n')
    elif aptype == 'N':
       for i in range(nbty):
          fid.write(str(xbty[0][i]));fid.write(" ")
	  fid.write(str(xbty[1][i]));fid.write(" ")
          fid.write(str(bproperties[0][i]));fid.write(" ")
          fid.write(str(bproperties[1][i]));fid.write(" ")
          fid.write(str(bproperties[2][i]));fid.write(" ")
          fid.write(str(bproperties[3][i]));fid.write(" ")
          fid.write(str(bproperties[4][i]));fid.write('\n')	  	  
    else:
       print('Unknown bottom properties...')
    
    fid.write(separation_line);fid.write("\n")
    fid.write('\'');fid.write(array_shape);fid.write('\'\n')
    fid.write(str(m));fid.write(" ")
    fid.write(str(n));fid.write('\n')
    
    for i in range(m):
        fid.write(str(array_r[i]));fid.write(" ")
    fid.write('\n')
    
    for i in range(n):
        fid.write(str(array_z[i]));fid.write(" ")
    fid.write('\n')
    
    fid.write(separation_line);fid.write("\n")
    
    fid.write('\'');fid.write(calc_type);fid.write('\'\n')
    fid.write(str(array_miss));fid.write("\n")

    fid.close()
