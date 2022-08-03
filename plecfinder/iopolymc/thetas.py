import numpy as np
import os,sys,glob

def load_thetas(filename):
    npyfn = '.'.join(filename.split('.')[:-1])+'_thetas.npy'
    if os.path.isfile(npyfn):
        print(f"loading thetas from '{npyfn}'")
        return np.load(npyfn)    
    
    Thetas = read_thetas(filename)
    np.save(npyfn,Thetas)
    return Thetas

def read_thetas(filename):
    print(f"reading '{filename}'")
    Thetas = np.loadtxt(filename)
    num_Thetas = len(Thetas)
    if num_Thetas == 0:
        return None
    num_bps = 1
    curr_id = Thetas[0,0]
    for i in range(1,num_Thetas):
        if Thetas[i,0] > curr_id:
            curr_id = Thetas[i,0]
            num_bps += 1
        else:
            break
    if num_Thetas%num_bps != 0:
        print("Error in Thetas File. Number of lines is inconsistent with number of bps")
        return None
    num_snap = int(num_Thetas/num_bps)
    Thetas = np.reshape(Thetas[:,1:],(num_snap,num_bps,3))
    return Thetas
    

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("usage: python %s filename"%sys.argv[0])
        sys.exit(0)
    fn  = sys.argv[1]
    
    Thetas = load_thetas(fn)
    print("%d snapshots - %d bps"%(len(Thetas),len(Thetas[0])))
