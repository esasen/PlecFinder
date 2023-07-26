import os, sys, glob
import numpy as np
from .IOPolyMC import iopolymc as io
from .plecfinder import state2plecs, xyz2plecs

from typing import List, Dict, Any, Callable, Tuple


def polymc_collect_topols(
    path: str,
    select: Dict[str, Any],
    min_writhe_density: float,
    min_writhe: float,
    connect_dist: float = 10,
    no_overlap: bool = True,
    om0: float = 1.76,
    plot_every: int = 0,
    save_topols: bool = True,
    include_wm: bool = False,
    valid_dataformats: List[str] = ["state", "xyz"],
    recursive: bool = False,
    num_files: int = None
) -> List[Dict[str, Any]]:
    # querey sims
    sims = io.querysims(path, select=select, recursive=recursive)

    # calculate topols for each simulation
    topols = []
    num = 0
    for sim in sims:
        if num_files is not None and num >= num_files:
            break
        
        statefn = None
        xyzfn = None
        for fn in sim["files"]:
            if os.path.splitext(fn)[-1].lower() == ".state":
                statefn = fn
            if os.path.splitext(fn)[-1].lower() == ".xyz":
                xyzfn = fn
        if statefn is not None:
            print(statefn)
            topols += state2plecs(
                statefn,
                min_writhe_density,
                min_writhe,
                connect_dist=connect_dist,
                no_overlap=no_overlap,
                om0=om0,
                plot_every=plot_every,
                save=save_topols,
                load=True,
                include_wm=include_wm,
            )
            num += 1
            continue
        if xyzfn is not None:
            print(xyzfn)
            topols += xyz2plecs(
                xyzfn,
                min_writhe_density,
                min_writhe,
                connect_dist=connect_dist,
                no_overlap=no_overlap,
                om0=om0,
                plot_every=plot_every,
                save=save_topols,
                load=True,
                include_wm=include_wm,
            )
            num += 1
    return topols


if __name__ == "__main__":
    
    
    path = "PATH/TO/FILE"
    select = {"force": 0.5, "sigma": 0.02}

    min_writhe_density = 0.01
    min_writhe = 0.5
    connect_dist = 10.0

    valid_dataformats: List[str] = (["state", "xyz"],)
    recursive: bool = False

    topols = polymc_collect_topols(
        path,
        select,
        min_writhe_density=min_writhe_density,
        min_writhe=min_writhe,
        connect_dist=connect_dist,
        valid_dataformats=valid_dataformats,
        recursive=recursive,
    )

    print(len(topols))
