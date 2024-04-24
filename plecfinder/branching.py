import os, sys
import numpy as np
from typing import Dict, Any, List, Tuple

########################################################################
########################################################################
########################################################################


def build_branchtree(branches_or_topol) -> Tuple[List[Dict], List[Dict]]:
    """build branch tree for chain topology

    Arguments:
    ----------
        branches : List[Dict]
            List of branch dictionaries or full topol dictionary

    Returns:
    ----------
        tree structure of branches
            list of lists
    """
    if isinstance(branches_or_topol,dict):
        branches = branches_or_topol['branches']
        if not branches_or_topol["no_overlap"]:
            raise ValueError(
                "Requires branchoverlap to be removed! Set no_overlap to True when running find_plecs"
            )
    else:
        branches = branches_or_topol

    treeroots = list()
    treebranches = [{"root": branch, "branches": list()} for branch in branches]

    for i, br in enumerate(treebranches):
        src_branch = None
        for j in range(i - 1, -1, -1):
            cbr = treebranches[j]
            if is_downstream(br["root"], cbr["root"]):
                src_branch = cbr
                break
        if src_branch is None:
            treeroots.append(br)
        else:
            src_branch["branches"].append(br)

    return treeroots, treebranches


def find_endloops(branches):
    endpoints = list()
    treeroots, branches = build_branchtree(branches)
    for branch in branches:
        if len(branch['branches']) == 0:
            if isinstance(branch,dict):
                endpoint = 0.5*(branch['root']['x2'] + branch['root']['y1'])
            else:
                endpoint = 0.5*(branch['root'][1] + branch['root'][2])
            endpoints.append(endpoint)
    return endpoints


def is_downstream(branch, upbranch):
    if isinstance(branch,dict):
        if branch["x1"] < upbranch["x1"]:
            return False
        if branch["y1"] > upbranch["y1"]:
            return False
        return True
    else:
        if branch[0] < upbranch[0]:
            return False
        if branch[2] > upbranch[2]:
            return False
        return True