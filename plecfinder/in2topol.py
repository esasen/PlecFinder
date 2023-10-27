import os, sys
from .tofile import load_topol_by_specs

########################################################################
########################################################################
########################################################################

def in2plecs(
    infn: str,
    min_writhe_density: float,
    min_writhe: float,
    connect_dist: float = 10,
):
    
    outpath = infn.replace(".state", "")
    if not os.path.exists(outpath):
        return None

    return load_topol_by_specs(outpath, min_writhe_density, min_writhe, connect_dist)
