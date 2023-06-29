import plecfinder as pf

import os,sys,glob
import json
import time
import copy
import numpy as np
from numba import jit

# ~ from plecfinder.iopolymc   import state
import plecfinder as pf



    
########################################################################
########################################################################
########################################################################

if __name__ == "__main__":

    if len(sys.argv) < 5:
        print("usage: python %s min_wd min_writhe connect_dist plot_every files" %sys.argv[0])
        sys.exit(0)
    
    min_writhe      = 0.25
    connect_dist    = 25.0
    om0             = 1.76
    
    include_wm  = False
    load        = True
    save        = True
    
    min_wd          = float(sys.argv[1])
    min_writhe      = float(sys.argv[2])
    connect_dist    = float(sys.argv[3])
    plot_every      = int(sys.argv[4])
    fns        = sys.argv[5:]
    
    print('%d files found'%len(fns))
    for fn in fns:
        print('evaluating "%s"'%fn)
        t1 = time.time()
        
        if os.path.splitext(fn)[-1].lower() == '.state':
            topols = pf.state2plecs(fn, 
                                    min_wd, 
                                    min_writhe = min_writhe,
                                    connect_dist=connect_dist,
                                    om0=om0,
                                    plot_every=plot_every,
                                    save=save,
                                    load=load,
                                    include_wm=include_wm)
        if os.path.splitext(fn)[-1].lower() == '.xyz':
            topols = pf.xyz2plecs(  fn, 
                                    min_wd, 
                                    min_writhe = min_writhe,
                                    connect_dist=connect_dist,
                                    om0=om0,
                                    plot_every=plot_every,
                                    save=save,
                                    load=load,
                                    include_wm=include_wm)
        t2 = time.time()
        print('timing =',(t2-t1))





















