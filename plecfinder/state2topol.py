import os,sys,glob
import json
import time
import copy
import numpy as np
from numba import jit

from plottopol  import plot_topol 
from plecfinder import find_plectonemes,save_topols
from iopolymc   import state


########################################################################
########################################################################
########################################################################

def state2plecs(statefn: str, min_writhe_density: float, min_writhe: float,connect_dist: float,no_branch_overlap=True,om0=1.76,plot_every=0,save_topol=False,load_topol=False,include_wm=False):
    
    plec_fn = statefn.replace('.state',('_topols_mwd%s_mwr%s_cd%s'%(min_writhe_density,min_writhe,connect_dist)).replace('.','p'))
    
    # load from file
    if load_topol:
        if os.path.isfile(plec_fn):
            topols = pf.load_topols(plec_fn)
            if topols is not None:
                # ~ topols = topol_consistency(topols)
                # ~ pf.save_topols(plec_fn,topols)
                return topols
    
    # load state       
    state = state.load_state(statefn)
    configs  = state['pos']
    disc_len = state['disc_len']
    nbp      = state['Segments']
    dlk      = state['delta_LK']
    
    # make directory for plots
    if plot_every > 0:
        path = statefn.replace('.state',f'_mwd{min_writhe_density}_plotplec'.replace('.','p'))
        if not os.path.exists(path):
            os.makedirs(path)    
    
    # calculate discretization length
    if disc_len is None:
        disc_len = pf.cal_disc_len(configs[0])
    
    # loop over configurations and calculate topology
    topols = list()
    for i,config in enumerate(configs):
        if i%200==0:
            print(i)
            
        # plot topology
        topol = find_plectonemes(config, min_writhe_density  = min_writhe_density,
                                            plec_min_writhe     = min_writhe,
                                            disc_len            = disc_len,
                                            no_branch_overlap   = no_branch_overlap,
                                            connect_dist        = connect_dist,
                                            om0                 = om0,
                                            include_wm          = include_wm)
                
        topols.append(topol)
        
        # plot topology
        if plot_every > 0:
            if i%plot_every == 0:
                figfn = path+'/' + ('mwd_%.4f'%min_writhe_density).replace('.','p') + '_#%d'%i
                plot_topol(topol,savefn=figfn)
    
    # ~ # save topology
    if save_topol:
        save_topols(plec_fn,topols)
    return topols
    

########################################################################
########################################################################
########################################################################

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
        t1 = time.time()
        state2plecs(statefn, min_wd, min_writhe = min_writhe,connect_dist=connect_dist,om0=om0,plot_every=plot_every,save_topol=save_topol,load_topol=load_topol,include_wm=include_wm)
        t2 = time.time()
        print('timing =',(t2-t1))
