import numpy as np
import sys,os

def gen_topol_snapshot(fn,config,topol,colorby='plectoneme'):
    """ Generates an xyz file for the configuration highlighting the topology
    
        
        Arguments:
        ----------
            colorby : sets whether plectonemes or branches are colors individually. 
                - plec / plectoneme : same color for full plectoneme
                - branch            : different color for each branch
    """ 
    
    xyz = dict()
    xyz['data']     = np.array([config])
    xyz['types']    = ['A' for i in range(len(config))]
    addtopology2xyz(xyz,topol,colorby=colorby)
    write_xyz(xyzfn,xyz)



def write_xyz(outfn,dat):
    data  = dat['data']
    types = dat['types']
    nbp   = len(data[0])
    nsnap = len(data)
    with open(outfn,'w') as f:
        for s in range(nsnap):
            f.write('%d\n'%nbp)
            f.write('Atoms. Timestep: %d\n'%(s))
            for i in range(nbp):
                f.write('%s %.4f %.4f %.4f\n'%(types[i],data[s,i,0],data[s,i,1],data[s,i,2]))
                
def state2xyz(state):
    N = state["Segments"]
    xyz = dict()
    xyz['data']     = state['pos']
    xyz['types']    = ['A' for i in range(N)]
    return xyz
    
def addtopology2xyz(xyz,topol,colorby='plectoneme'):
    """
    
        Arguments:
        ----------
            colorby : sets whether plectonemes or branches are colors individually. 
                - plec / plectoneme : same color for full plectoneme
                - branch            : different color for each branch
    """
    
    atom_types = ['C','N','O','K','F','P','S']
    curr_type_id = 0
    
    if len(xyz['types']) != topol['N']:
        raise ValueError('Chain lengths inconsistent')
    
    if colorby.lower() in ['plec','plectoneme','plecs','plectonemes']:
        plecs = topol['plecs']
        for plec in plecs:
            id1 = plec['id1']
            id2 = plec['id2']
            at = atom_types[curr_type_id]
            curr_type_id = (curr_type_id+1)%len(atom_types)

            xyz['types'][id1:id2+1] = [at for i in range(id2-id1+1)]
              
    elif colorby.lower() in ['branch','branches']:
        branches = topol['branches']
        
        for branch in branches:
            x1 = branch['x1']
            x2 = branch['x2']
            y1 = branch['y1']
            y2 = branch['y2']
            
            at = atom_types[curr_type_id]
            curr_type_id = (curr_type_id+1)%len(atom_types)
            xyz['types'][x1:x2+1] = [at for i in range(x2-x1+1)]
            xyz['types'][y1:y2+1] = [at for i in range(y2-y1+1)]
    return xyz
    
    

########################################################################
########################################################################
########################################################################

if __name__ == "__main__":

    from plecfinder.iopolymc import ReadState
    from plecfinder import state2plecs
    
    import state2topol as s2p

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
    statefn         = sys.argv[5]
    
    print('evaluating "%s"'%statefn)
    topols = state2plecs(statefn, min_wd, min_writhe = min_writhe,connect_dist=connect_dist,om0=om0,plot_every=plot_every,save_topol=save_topol,load_topol=load_topol,include_wm=include_wm)

    state = ReadState(statefn)
    
    snap    = 35
    colorby = 'branch'
    # ~ colorby = 'plectoneme'
    
    xyzfn = statefn.replace('.state','.xyz')
    gen_topol_snapshot(xyzfn,state['pos'][snap],topols[snap],colorby=colorby)
    

        
        
        
        
        
