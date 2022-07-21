import numpy as np
import os,sys,glob
from FileRead import FileRead

"""
########################################################
Read/ReadState.py
    
    state = LoadState(filename)
    state = ReadState(filename)
    specs = ReadSpec(filename)
    
        ReadState always reads the state file while LoadState accesses the 
        binary if it exists and creates it if it doesn't such that access
        will be accelerated next time.
        
        state is a dictionary containing all the specs as well as 
        trajectories. 
        specs contains the same except for the trajectories
        
    
On Execution: 
    Read/ReadState.py filename 
        
        Reads state file, prints specs in terminal and creates trajectory
        binary file.
        
########################################################
"""

def remove_newline(string):
    if string[-1] == "\n":
        return string[:-1]

def LoadState(filename):
    
    pos_fnpy    = filename[:-6]+'_pos.npy'
    triads_fnpy = filename[:-6]+'_triads.npy'
    Omegas_fnpy = filename[:-6]+'_Omegas.npy'
    
    state     = ReadSpec(filename)
    all_found=False
    if state['pos_contained'] and not os.path.isfile(pos_fnpy):
        all_found = False
    if state['triads_contained'] and not os.path.isfile(triads_fnpy):
        all_found = False
    if state['Omegas_contained'] and not os.path.isfile(Omegas_fnpy):
        all_found = False
        
    if all_found:
        if state['pos_contained']:
            state['pos']    = np.load(pos_fnpy)
        if state['triads_contained']:
            state['triads'] = np.load(triads_fnpy)
        if state['Omegas_contained']:
            state['Omegas'] = np.load(Omegas_fnpy)
    else:
        state = ReadState(filename)
        if state['pos_contained']:
            SavePos(pos_fnpy,state['pos'])
        if state['triads_contained']:
            SavePos(triads_fnpy,state['triads'])
        if state['Omegas_contained']:
            SavePos(Omegas_fnpy,state['Omegas'])
    return state

def ReadSpec(filename):
    specs = dict()
    specs["pos_contained"]    = False
    specs["triads_contained"] = False
    specs["Omegas_contained"] = False
    
    FR = FileRead(filename)
    line = FR.readline()
    ll = FR.linelist()
    while line!="":
        while ll[0] != "Snapshot":
            if ll[0] == "Mode":
                specs["Mode"]     = remove_newline(ll[2])
            if ll[0] == "Segments:":
                specs["Segments"] = int(ll[1])
                N = int(ll[1])
            if ll[0] == "disc_len:":
                specs["disc_len"] = float(ll[1])
            if ll[0] == "Ia_range:":
                specs["Ia_range"] = int(ll[1])
            if ll[0] == "T":
                specs["T"]        = float(ll[2])
            if ll[0] == "closed":
                specs["closed"]   = int(ll[2])
            if ll[0] == "Lk_fixed:":
                specs["Lk_fixed"] = int(ll[1])
            if ll[0] == "EVactive:":
                specs["EVactive"] = int(ll[1])
            if ll[0] == "EVradius:":
                specs["EVradius"] = float(ll[1])
            if ll[0] == "delta_LK:":
                specs["delta_LK"] = float(ll[1])
            if ll[0] == "force":
                specs["force"]    = float(ll[2])
                
            if ll[0] == "pos":
                specs["pos_contained"]    = bool(int(ll[2]))
            if ll[0] == "triads":
                specs["triads_contained"] = bool(int(ll[2]))
            if ll[0] == "Omegas":
                specs["Omegas_contained"] = bool(int(ll[2]))
                                
            line = FR.readline()
            ll = FR.linelist()
            if line=="":
                break
        if ll[0] == "Snapshot":
            break
        line = FR.readline()
        ll = FR.linelist()
    
    if "Segments" not in specs:
        print("Error: Not specs found in file '"+filename+"'")
        specs["pos_contained"]    = False
        specs["triads_contained"] = False
        specs["Omegas_contained"] = False
        specs["Mode"]     = "None"
        specs["Segments"] = 0
        specs["disc_len"] = 0
        specs["Ia_range"] = 0
        specs["T"]        = 0
        specs["closed"]   = 0
        specs["Lk_fixed"] = 0
        specs["EVactive"] = 0
        specs["EVradius"] = 0
        specs["delta_LK"] = 0
        specs["force"]    = 0
        specs["sigma"]    = 0
    else:
        Lk0 = specs["Segments"]*specs["disc_len"]/0.34/10
        specs["sigma"] = specs["delta_LK"]/Lk0
    return specs

def ReadState(filename):    
    specs = dict()
    specs["pos_contained"]    = False
    specs["triads_contained"] = False
    specs["Omegas_contained"] = False
    
    FR = FileRead(filename)
    line = FR.readline()
    ll = FR.linelist()
    while line!="":
        while ll[0] != "Snapshot":
            if ll[0] == "Mode":
                specs["Mode"]     = remove_newline(ll[2])
            if ll[0] == "Segments:":
                specs["Segments"] = int(ll[1])
            if ll[0] == "disc_len:":
                specs["disc_len"] = float(ll[1])
            if ll[0] == "Ia_range:":
                specs["Ia_range"] = int(ll[1])
            if ll[0] == "T":
                specs["T"]        = float(ll[2])
            if ll[0] == "closed":
                specs["closed"]   = int(ll[2])
            if ll[0] == "Lk_fixed:":
                specs["Lk_fixed"] = int(ll[1])
            if ll[0] == "EVactive:":
                specs["EVactive"] = int(ll[1])
            if ll[0] == "EVradius:":
                specs["EVradius"] = float(ll[1])
            if ll[0] == "delta_LK:":
                specs["delta_LK"] = float(ll[1])
            if ll[0] == "force":
                specs["force"]    = float(ll[2])

            if ll[0] == "pos":
                specs["pos_contained"]    = bool(int(ll[2]))
            if ll[0] == "triads":
                specs["triads_contained"] = bool(int(ll[2]))
            if ll[0] == "Omegas":
                specs["Omegas_contained"] = bool(int(ll[2]))
                
            line = FR.readline()
            ll = FR.linelist()
            if line=="":
                break
        if ll[0] == "Snapshot":
            break
        line = FR.readline()
        ll = FR.linelist()
    
    # This line accounts for older versions that didn't contain the dump specifier and only dumped positions
    if (not specs["pos_contained"] and not specs["triads_contained"] and not specs["Omegas_contained"]):
        specs["pos_contained"] = True
        
    if specs["pos_contained"]:
        all_pos    = list()
    if specs["triads_contained"]:
        all_triads = list()
    if specs["Omegas_contained"]:
        all_Omegas = list()
        
    num_bp = specs["Segments"]
    if specs["closed"]:
        num_bps = num_bp
    else:
        num_bps = num_bp-1
    
    counter=0
    while line!="":
        ll = FR.linelist()
        if ll[0] == "Snapshot":
            counter+=1
            #~ print("reading snapshot %d"%counter)
            
            if specs["pos_contained"]:
                valid=True
                pos=np.zeros([num_bp,3])
                for i in range(num_bp):
                    line = FR.readline()
                    ll = FR.linelist()
                    if len(ll) != 4:
                        valid=False
                        break
                    pos[i] = [float(ll[0]),float(ll[1]),float(ll[2])]
                if valid==True:
                    all_pos.append(pos)
                else:
                    print("Error encountered while reading state file positions")
                    raise InputError
                    
            if specs["triads_contained"]:
                valid=True
                triads=np.zeros([num_bp,3,3])
                for i in range(num_bp):
                    line = FR.readline()
                    ll = FR.linelist()
                    if len(ll) != 10:
                        valid=False
                        break
                    triads[i,0] = [float(ll[0]),float(ll[1]),float(ll[2])]
                    triads[i,1] = [float(ll[3]),float(ll[4]),float(ll[5])]
                    triads[i,2] = [float(ll[6]),float(ll[7]),float(ll[8])]
                if valid==True:
                    all_triads.append(triads)
                else:
                    print("Error encountered while reading state file triads")
                    raise InputError
                    
            if specs["Omegas_contained"]:
                valid=True
                Omegas=np.zeros([num_bps,3])
                for i in range(num_bps):
                    line = FR.readline()
                    ll = FR.linelist()
                    if len(ll) != 4:
                        valid=False
                        break
                    Omegas[i] = [float(ll[0]),float(ll[1]),float(ll[2])]
                if valid==True:
                    all_Omegas.append(Omegas)
                else:
                    print("Error encountered while reading state file Omegas")
                    raise InputError
                    
        line = line = FR.readline()
    FR.close()
    
    state = specs
    if state['pos_contained']:
        state['pos'] = np.array(all_pos)
    if state['triads_contained']:
        state['triads'] = np.array(all_triads)
    if state['Omegas_contained']:
        state['Omegas'] = np.array(all_Omegas)
    return state
    
def SavePos(outname,snapshots):
    if outname[-4:] == '.npy':
        outn = outname
    else:
        outn = outname + '.npy'
    np.save(outn,snapshots)
    
if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("usage: python %s filename"%sys.argv[0])
        sys.exit(0)
    fn  = sys.argv[1]
    
    state = LoadState(fn)
    pos = state['pos']
    fnpy = fn.split['.'][0]+'.npy'
    SavePos(fnpy,pos)
    for key,val in specs.items():
        print( key, "=", val )
    print("%d snapshots found"%len(snapshots))
    
