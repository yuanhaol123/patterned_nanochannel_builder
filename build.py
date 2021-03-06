import numpy as np

nx = 34
ny = 20
nz = 20
nBasis = 8
nAtoms = nx*ny*nz*nBasis
#print 'nAtoms = '+str(nAtoms)

magnitude_of_fluid_to_remove = 97
magnitude_of_space = 8
magnitude_of_height = -15
# Lattice Constant
a = 5.4321 
frac = np.zeros( (nBasis,3));
frac[0,:] = np.array([0, 0, 0]) * a
frac[1,:] = np.array([0, 0.5, 0.5]) * a
frac[2,:] = np.array([0.5, 0, 0.5]) * a
frac[3,:] = np.array([0.5, 0.5, 0]) * a
frac[4,:] = np.array([0.25, 0.25, 0.25]) * a
frac[5,:] = np.array([0.25, 0.75, 0.75]) * a
frac[6,:] = np.array([0.75, 0.25, 0.75]) * a
frac[7,:] = np.array([0.75, 0.75, 0.25]) * a

Xn = np.zeros( (nAtoms,3) )

print ('Calculating...')
for ii in range(0,nx):
    for jj in range(0,ny):
        for kk in range(0, nz):
            for mm in range(0, nBasis):
                Xn[ ( ii * ny * nz + jj * nz + kk ) * nBasis + mm,:] = np.array( [ ii, jj,kk] ) * a + frac[mm,:]

print ('Writing...')

f = open('Si.d','w')

f.write('coordinate generated by Matlab\n');
f.write(str(nAtoms)+'\t atoms\n');
f.write('\n');
f.write('8 atom types\n');
f.write('\n');
f.write( str(0) + '\t' + str(nx*a) + '\t' + 'xlo xhi\n' );
f.write( str(0) + '\t' + str(ny*a) + '\t' + 'ylo yhi\n' );
f.write( str(0) + '\t' + str(nz*a) + '\t' + 'zlo zhi\n' );
f.write('\n');
f.write('Masses\n\n');
f.write('1 \t 28.015\n');
f.write('2 \t 28.015\n');
f.write('3 \t 28.015\n');
f.write('4 \t 28.015\n');
f.write('5 \t 39.015\n');
f.write('6 \t 28.015\n');
f.write('7 \t 28.015\n');
f.write('8 \t 28.015\n\nAtoms\n\n');
for ii in np.arange(0,nAtoms):
    f.write( str(ii) + '\t' + '1' + '\t' + str(Xn[ii,0]) + '\t' + str(Xn[ii,1]) + '\t' + str( Xn[ii,2]) +'\n' )
f.close()



## Si square generates and solid builder starts
dataIn = open('Si.d','r')
dataOut = open('Si_cut.txt','w')

def edgefunc(y, pos, d):
    t = y%d
    if t > magnitude_of_space*d/10:
       
       t = magnitude_of_height
    else:
        t=0

    return  pos+t 

def zfunc(z, pos, d):
    t = z%d
    if t > magnitude_of_space*d/10:
       t = magnitude_of_height
    else:
        t=0
    print type (t)
    return  pos+t 

def flat(y, pos, d):
    t = y%d
    if t > d//2:   
       t = 0
    else:
        t=0
    return  pos+t 

for ii in range(0,21):
    line = dataIn.readline()
    dataOut.write(line)
dataOut.write('\n')
dataIn.readline()

xn = np.zeros( (nAtoms, 3) )
flag = np.zeros( nAtoms )

for ii in range(0,nAtoms):
    line = dataIn.readline()
    data = line.split()
    xn[ii,:] = data[2:5]

    x = xn[ii,0]
    y = xn[ii,1]
    z = xn[ii,2]
   #### if x> 100 and x < edgefunc(y,2050,80):
    if x < flat(y,7,2):
        flag[ii] = 1
    elif x < flat(y,22,2):
        flag[ii] = 2
    elif x < edgefunc(y,62,20) and x < zfunc(z,62,20):
    #elif x < zfunc(z,40,20):
        flag[ii] = 3

    elif x < flat(y,magnitude_of_fluid_to_remove,2):
        flag[ii] = 4
    elif x < flat(y,122,2):
        flag[ii] = 5
    elif x < flat(y,162,2):
        flag[ii] = 6
    elif x < flat(y,177,2):
        flag[ii] = 7
    else:
        flag[ii] = 8

for ii in np.arange(0, nAtoms):
   ## print int(flag[ii])
    dataOut.write( str(ii+1) + '\t' + str( int(flag[ii]) ) + '\t' + str(xn[ii,0]) + '\t' + str(xn[ii,1]) + '\t' + str(xn[ii,2])+'\n')
    

dataOut.close()




dataIn = open('Si_cut.txt','r')
dataOut = open('pillar.d','w')
natoms = 108800
prev_line = 21

for ii in range(prev_line):
	line = dataIn.readline()
	dataOut.write(line)

dataOut.write('\n')
dataIn.readline()

xn = np.zeros( (natoms, 3))
atom_type = np.zeros(natoms)
 
counter = 0
for ii in range(0,natoms):
	line = dataIn.readline()
	data = line.split()
	xn[ii,:]= data[2:5]
	atom_type = data[1]
	#print(data[1])
	if atom_type == '1' or atom_type == '2' or atom_type == '3' or atom_type == '6' or atom_type == '7' or atom_type == '8':
		dataOut.write( str(counter+1) + '\t' + str( data[1] ) + '\t' + str(data[2]) + '\t' + str(data[3]) + '\t' + str(data[4])+'\n')
		counter += 1

dataOut.close()


dataOutRead = open('pillar.d','r')
dataOutNew = open('pillar_new.d', 'w')

for ii in range(counter + prev_line + 2):
	line = dataOutRead.readline()
	if ii == 1:
		dataOutNew.write(str(counter) + " atoms\n")	
	else:
		dataOutNew.write(line)
dataOutNew.close()
dataOutRead.close()