import numpy as np
import os,sys,glob
from ._file_read import file_read


RESTART_SEPERATOR = '###############################################################'

def read_restart(filename):
    """
        Returns a list of dictionaries (one for each snaoshot)
        Dictionaries contain keys:
            snapshot: snapshot id
            type:     simulation type
            num_bp:   number of basepairs
            sequence: monomer sequence
            dLK:      linking number
            pos:      monomer positions
            triads:   triads
            
        Parameters:
        -----------
        filename : string
            path of file
    
    """
    
    def read_snapshot(ssl):
        sst = int(ssl[0].split(' ')[-1])
        tpe = ssl[1].split(' ')[-1] 
        nbp = int(ssl[2].split(' ')[-1]) 
        squ = ssl[3].split(' ')[-1] 
        dlk = float(ssl[4].split(' ')[-1])
        if len(ssl) != nbp*2 + 5:
            print('inconsistent restart file')
            return None
        pos    = np.array([[float(elem) for elem in p.split(' ')] for p in ssl[5:5+nbp]])
        triads = np.array([np.reshape(np.array([float(elem) for elem in p.split(' ')]),(3,3),'F') for p in ssl[5+nbp:]])
        
        snapdict = dict()
        snapdict['snapshot'] = sst
        snapdict['type']     = tpe
        snapdict['num_bp']   = nbp
        snapdict['sequence'] = squ
        snapdict['dLK']      = dlk
        snapdict['pos']      = pos
        snapdict['triads']   = triads
        return snapdict
    
    snapshots = list()
    with open(filename,'r') as f:
        line = f.readline().strip()
        while line != '':
            if line == RESTART_SEPERATOR:
                snapshotlines = list()
                line = f.readline().strip()
                while line not in ['',RESTART_SEPERATOR] :
                    snapshotlines.append(line)
                    line = f.readline().strip()
                snapshots.append(read_snapshot(snapshotlines))
                continue
            line = f.readline().strip()
    return snapshots
    
    
def write_restart(filename,snapshots):
    """
        Write snapshots to restart file
        
        Parameters:
        -----------
        
        filename : string
            path of output file
            
        snapshots : list of dictionaries
        
            Each snapshot is separate dictionary. 
            Dictionaries contain keys:
                snapshot: snapshot id
                type:     simulation type
                num_bp:   number of basepairs
                sequence: monomer sequence
                dLK:      linking number
                pos:      monomer positions
                triads:   triads
            
    """
    
    f = open(filename,'w')
    for snapshot in snapshots:
        f.write(RESTART_SEPERATOR+'\n')
        f.write('snapshot: %d'%snapshot['snapshot']+'\n')
        f.write('type:     %s'%snapshot['type']+'\n')
        f.write('num_bp:   %d'%snapshot['num_bp']+'\n')
        f.write('sequence: %s'%snapshot['sequence']+'\n')
        f.write('dLK:      %.4f'%snapshot['dLK']+'\n')
        for p in snapshot['pos']:
            f.write('%.14f %.14f %.14f\n'%(p[0],p[1],p[2]))
        for trd in snapshot['triads']:
            f.write('%.14f %.14f %.14f %.14f %.14f %.14f %.14f %.14f %.14f\n'%(trd[0,0],trd[1,0],trd[2,0],trd[0,1],trd[1,1],trd[2,1],trd[0,2],trd[1,2],trd[2,2]))
    f.close()

    
if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print("usage: python %s in out"%sys.argv[0])
        sys.exit(0)
    fnin  = sys.argv[1]
    fnout = sys.argv[2]
    
    snapshots = read_restart(fnin)
    print('%d snapshots'%len(snapshots))
    print('%d monomers'%snapshots[0]['num_bp'])
    
    # ~ write_restart(fnout,snapshots)
