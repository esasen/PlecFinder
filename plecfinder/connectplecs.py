import numpy as np
from typing import Dict, Any, List, Tuple

########################################################################
########################################################################
########################################################################

def connect_plecs(plecs: List[Dict[str,Any]], combine_dist: float, om0: float = 1.76) -> List[Dict[str,Any]] :
    if combine_dist <= 0 or len(plecs) == 0:
        return plecs
    plec = plecs[0]
    disc_len = plec['L'] / plec['num_segs']
    wr2dens_conv_fac = 2 * np.pi / om0
    combine_segs = int(np.ceil(combine_dist/disc_len))
    
    retain = list()
    last_plec = plecs[0]
    retain.append(last_plec)
    for i in range(1,len(plecs)):
        segdist = plecs[i]['id1'] - last_plec['id2'] 
        if segdist <= combine_segs:
            last_plec['id2'] = plecs[i]['id2']
            last_plec['num_segs'] = last_plec['id2'] - last_plec['id1']
            last_plec['L'] = last_plec['num_segs'] * disc_len
            last_plec['wr'] += plecs[i]['wr']
            last_plec['wrdens'] = wr2dens_conv_fac * last_plec['wr'] / last_plec['L']
            last_plec['branch_ids'] += plecs[i]['branch_ids']
        else:
            last_plec = plecs[i]
            retain.append(last_plec)
    return retain
