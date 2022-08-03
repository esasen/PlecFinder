import numpy as np
import os,sys,glob
from .state import *

def scan_path(path,ext):
    if not os.path.exists(path):
        print("Path '%s' does not exist"%path)
        return []
    
    entries = list()
    statefiles = np.sort(glob.glob(path+"/*.%s"%ext))
    for stfn in statefiles:
        specs = ReadSpec(stfn)
        raw_fn = stfn[:-6]
        entries.append([raw_fn,specs])
    return entries
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python %s path"%sys.argv[0])
        sys.exit(0)
    
    path = sys.argv[1]
    entries = scan_path(path)
    
    for entry in entries:
        if entry[1]['EVradius'] == 7.0:
            print(entry[0])
    
    

