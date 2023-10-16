import os,glob
import numpy as np

from typing import List, Dict, Any


########################################################################
######## SAVE AND LOAD TOPOLS ##########################################
########################################################################

def load_topol_by_specs(path: str, mwd: float, mdr: float, cd: float):
    npys = glob.glob(path+'/*.npy')
    for npy in npys:
        splits = npy.split('/')[-1].split('.')[0].replace('p','.').split('_')[1:]
        if (    float(splits[0].replace('mwd','')) == mwd 
            and float(splits[1].replace('mwr','')) == mdr
            and float(splits[2].replace('cd','')) == cd
        ):
            return load_topol_npy(npy)
    return None
            

def load_topol(fn: str) -> List[Dict[str, Any]]:
    """
    Load topology form file
    """

    if os.path.splitext(fn)[-1] != ".npy":
        npyfn = fn + ".npy"
        if os.path.isfile(npyfn):
            return load_topol_npy(fn)
        topols = load_topol_text(fn)
        if topols is not None:
            save_topol_npy(npyfn, topols)
            os.remove(fn)
    return load_topol_npy(fn)


def save_topol(fn: str, topols: List[Dict[str, Any]], to_binary: bool = True) -> None:
    """
    Save topology to file
    """
    if to_binary:
        save_topol_npy(fn, topols)
    else:
        save_topol_text(fn, topols)


def load_topol_text(fn: str) -> List[Dict[str, Any]]:
    """
    Load topology form file
    """
    if not os.path.isfile(fn):
        return None
    with open(fn, "r") as f:
        topols = f.read()
        topols = topols.replace("array", "np.array")
        topols = eval(topols)
    return topols


def save_topol_text(fn: str, topols: List[Dict[str, Any]]) -> None:
    """
    Save topology to file
    """
    if "wm" in topols[0].keys():
        largest = np.prod(topols[0]["wm"].shape)
        np.set_printoptions(threshold=largest)
    with open(fn, "w") as outfile:
        outfile.write(repr(topols))
    np.set_printoptions(threshold=1000)


def load_topol_npy(fn: str) -> List[Dict[str, Any]]:
    """
    Load topology form numpy binary
    """
    if os.path.splitext(fn)[-1] != ".npy":
        fn = fn + ".npy"
    if not os.path.isfile(fn):
        return None
    topols = np.load(fn, allow_pickle=True)
    if isinstance(topols,np.ndarray):
        topols = list(topols)
    return topols


def save_topol_npy(fn: str, topols: List[Dict[str, Any]]) -> None:
    """
    Save topology to numpy binary
    """
    if os.path.splitext(fn)[-1] != ".npy":
        fn = fn + ".npy"
    np.save(fn, topols)
