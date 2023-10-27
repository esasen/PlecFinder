import os, sys, glob
import gc
import numpy as np
from .IOPolyMC import iopolymc as io
from .xyz2topol import xyz2plecs
from .state2topol import state2plecs
from .in2topol import in2plecs

from typing import List, Dict, Any, Callable, Tuple

def read_polymc_topols(
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
        recursive: bool = False,    
):
    return PolyMCTopols(
        path,
        select,
        min_writhe_density,
        min_writhe,
        connect_dist = connect_dist,
        no_overlap = no_overlap,
        om0 = om0,
        plot_every = plot_every,
        save_topols = save_topols,
        include_wm = include_wm,
        recursive = recursive,
    )


class PolyMCTopols:
    
    def __init__(
        self,
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
        recursive: bool = False,
        sim_partial_startid: int = 0,
        sim_partial_endid: int = 1000000000
    ):
        self.path = path
        self.select = select
        self.min_writhe_density = min_writhe_density
        self.min_writhe = min_writhe
        self.connect_dist = connect_dist
        self.no_overlap = no_overlap
        self.om0 = om0
        self.plot_every = plot_every
        self.save_topols = save_topols
        self.include_wm = include_wm
        self.plot_every = plot_every
        
        self.sims = io.querysims(path, select=select, recursive=recursive)
        self.index_sim = 0
        self.topols = None
        self.index_sim_topol = 0
        
        self.sim_partial_startid = sim_partial_startid
        if self.sim_partial_startid < 0:
            sim_partial_startid = 0
        self.sim_partial_endid   = sim_partial_endid
        
        self._load_next_sim()
        
    def __iter__(self):
        return self

    def __next__(self):
        if self.index_sim_topol >= len(self.topols) or self.index_sim_topol >= self.sim_partial_endid:
            print(self.index_sim_topol)
            if not self._load_next_sim():
                raise StopIteration
        topol = self.topols[self.index_sim_topol] 
        self.index_sim_topol += 1
        return topol
    
    def _load_next_sim(self):
        if self.topols is not None:
            del self.topols
            gc.collect()
        
        topols = []
        while len(topols) == 0:
            if self.index_sim >= len(self.sims):
                return False
            
            topols = polymc_sim2topols(
                self.sims[self.index_sim],
                self.min_writhe_density,
                self.min_writhe,
                connect_dist = self.connect_dist,
                no_overlap = self.no_overlap,
                om0 = self.om0,
                plot_every = self.plot_every,
                save_topols = self.save_topols,
                include_wm = self.include_wm,
            )
            print(f'{len(topols)=}')
            self.index_sim += 1

        self.topols = topols
        self.index_sim_topol = self.sim_partial_startid
        return True

        
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
    # valid_dataformats: List[str] = ["state", "xyz"],
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
        
        sim_topols = polymc_sim2topols(
            sim,
            min_writhe_density,
            min_writhe,
            connect_dist = connect_dist,
            no_overlap = no_overlap,
            om0 = om0,
            plot_every = plot_every,
            save_topols = save_topols,
            include_wm = include_wm,
        )
        if len(sim_topols) > 0:
            topols += sim_topols
            num += 1
    return topols

def polymc_sim2topols(
    sim: Dict[str,Any],
    min_writhe_density: float,
    min_writhe: float,
    connect_dist: float = 10,
    no_overlap: bool = True,
    om0: float = 1.76,
    plot_every: int = 0,
    save_topols: bool = True,
    include_wm: bool = False,
) -> List[Dict[str, Any]]:
    for fn in sim["files"]:
        if os.path.splitext(fn)[-1].lower() == ".state":
            print(f'Loading {fn}')
            return state2plecs(
                fn,
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
        if os.path.splitext(fn)[-1].lower() == ".xyz":
            print(f'Loading {fn}')
            return xyz2plecs(
                fn,
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
        if os.path.splitext(fn)[-1].lower() == ".in":
            topols = in2plecs(
                fn,
                min_writhe_density,
                min_writhe,
                connect_dist=connect_dist
            )
            if topols is None:
                topols = []
            return topols
    return []
    
    
    
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
