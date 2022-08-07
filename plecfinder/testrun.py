import plecfinder as pf

import os,sys,glob
import json
import time
import copy
import numpy as np
from numba import jit

from plecfinder.iopolymc   import read_state
from plecfinder.pylk       import writhemap
from plecfinder            import plot_topol

import pkg_resources

def testrun():
    
    include_wm = False
    load_topol = False
    save_topol = False
    
    min_wd          = 0.02
    min_writhe      = 0.5
    connect_dist    = 25.0
    om0             = 1.76
    
    resource_package = __name__
    
    statefn = pkg_resources.resource_filename(__name__, 'examples/s_0p0400_run1.state')

    state = read_state(statefn)
    configs  = state['pos']
    disc_len = state['disc_len']
    nbp      = state['Segments']
    dlk      = state['delta_LK']
    
    for config in configs:
        t1 = time.time()
        
        topols = list()    
        topol = pf.find_plectonemes(config, min_writhe_density = min_wd,
                                            plec_min_writhe    = min_writhe,
                                            disc_len           = None,
                                            no_overlap         = True,
                                            connect_dist       = connect_dist,
                                            om0                = om0,
                                            include_wm         = False)
         
        t2 = time.time()
        print('timing =',(t2-t1))

        plot_topol(topol,savefn=None,flip_positive=True,remove_negative_wr=True)
