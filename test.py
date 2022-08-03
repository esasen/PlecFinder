import plecfinder as pf

import os,sys,glob
import json
import time
import copy
import numpy as np
from numba import jit

# ~ from plecfinder.iopolymc   import state
from plecfinder.iopolymc   import state

from plecfinder.pylk   import writhemap


if __name__ == "__main__":

    if len(sys.argv) < 5:
        print("usage: python %s min_wd min_writhe connect_dist plot_every statefns" %sys.argv[0])
        sys.exit(0)
    
    min_writhe      = 0.25
    connect_dist    = 25.0
    om0             = 1.76
    
    include_wm = False
    load_topol = True
    save_topol = True
    
    min_wd          = float(sys.argv[1])
    min_writhe      = float(sys.argv[2])
    connect_dist    = float(sys.argv[3])
    plot_every      = int(sys.argv[4])
    statefns        = sys.argv[5:]
    

    print('%d statefiles found'%len(statefns))
    for statefn in statefns:
        print('evaluating "%s"'%statefn)
        
        state = state.load_state(statefn)
        configs  = state['pos']
        disc_len = state['disc_len']
        nbp      = state['Segments']
        dlk      = state['delta_LK']
        
        t1 = time.time()
        
        topol = pf.find_plectonemes(configs[0],    min_writhe_density = min_wd,
                                            plec_min_writhe    = min_writhe,
                                            disc_len           = None,
                                            no_branch_overlap  = True,
                                            connect_dist       = 25,
                                            om0                = connect_dist,
                                            include_wm         = False)
         
        t2 = time.time()
        print('timing =',(t2-t1))
