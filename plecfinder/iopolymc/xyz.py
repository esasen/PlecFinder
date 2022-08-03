import numpy as np
import sys,os
from ._file_read import file_read

"""
########################################################
    
    
    specs,snapshots = load_xyz(filename)
    specs,snapshots = read_xyz(filename)
    
        readxyz always reads the xyz file while loadxyz accesses the 
        binary if it exists and creates it if it doesn't such that access
        will be accelerated next time.
        
On Execution: 
    Read/readxyz.py filename 
        
        Reads state file, prints specs in terminal and creates trajectory
        binary file.
        
########################################################
"""

XYZ_NPY_EXT = '_xyz'

def load_xyz(filename,savenpy=True,loadnpy=True):
    fnpy = filename[:-4]+XYZ_NPY_EXT+'.npy'
    print(fnpy)
    if os.path.isfile(fnpy) and loadnpy:
        xyz          = dict()
        print(f"loading positions from '{fnpy}'")
        xyz['pos']   = np.load(fnpy)
        xyz['types'] = read_xyz_atomtypes(filename)
    else:
        xyz = read_xyz(filename)
        if savenpy:
            save_xyz_binary(fnpy,xyz['pos'])
    return xyz


def read_xyz(fn):
    print(f"reading '{fn}'")
    data = list()
    F = file_read(fn)
    line = F.readline()
    while line!='':
        ll = F.linelist()
        if len(ll)>=4 and ll[0]!='Atoms.':
            snapshot = list()
            while len(ll)>=4:
                snapshot.append( [float(ft) for ft in ll[1:4]])
                line = F.readline()
                ll   = F.linelist()
            data.append(snapshot)
        line = F.readline()
    data = np.array(data)
    
    xyz = dict()
    xyz['pos']   = data
    xyz['types'] = read_xyz_atomtypes(fn)
    return xyz
    
def read_xyz_atomtypes(fn):
    data = list()
    F = file_read(fn)
    line = F.readline()
    num = 0
    types = list()
    while line!='':
        ll = F.linelist()
        if len(ll)>=4 and ll[0]!='Atoms.':
            num += 1
            if num > 1:
                break
            while len(ll)>=4:
                types.append(ll[0])
                line = F.readline()
                ll   = F.linelist()
        line = F.readline()
    return types
    
def write_xyz(outfn,data,add_extension=True):
    """
    Writes configuration to xyz file
    
    Parameters
    ----------
    outfn : string 
        name of xyz file
    
    """
    if '.xyz' not in outfn.lower() and add_extension:
        outfn += '.xyz'
    
    pos   = data['pos']
    types = data['types']
    nbp   = len(pos[0])
    with open(outfn,'w') as f:
        for s,snap in enumerate(pos):
            f.write('%d\n'%nbp)
            f.write('Atoms. Timestep: %d\n'%(s))
            for i in range(nbp):
                f.write('%s %.4f %.4f %.4f\n'%(types[i],snap[i,0],snap[i,1],snap[i,2]))
    
def save_xyz_binary(outname,data):
    if outname[-4:] == '.npy':
        outn = outname
    else:
        outn = outname + '.npy'
    np.save(outn,data)    


if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print("usage: python %s fin fout"%sys.argv[0])
        sys.exit(0)
    fin  = sys.argv[1]
    fout = sys.argv[2]
    xyz  = load_xyz(fin)
    # ~ fnpy = fin[:-4]+XYZ_NPY_EXT+'.npy'
    # ~ save_xyz_binary(fnpy,xyz)
    
    types = read_xyz_atomtypes(fin)
    print(f'number of atoms = {len(types)}')
    
    # ~ print(xyz.keys())
    # ~ write_xyz(fout,xyz)
    
