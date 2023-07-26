import os, sys
import numpy as np
from typing import Dict, Any, List, Tuple

########################################################################
########################################################################
########################################################################


def build_branchtree(topol: Dict[str, Any]) -> Tuple[List[Dict], List[Dict]]:
    """build branch tree for chain topology

    Arguments:
    ----------
        topol : dictionary
            topology dictionary

    Returns:
    ----------
        tree structure of branches
            list of lists
    """
    if not topol["no_overlap"]:
        raise ValueError(
            "Requires branchoverlap to be removed! Set no_overlap to True when running find_plecs"
        )

    treeroots = list()
    branches = [{"root": branch, "branches": list()} for branch in topol["branches"]]

    for i, br in enumerate(branches):
        src_branch = None
        for j in range(i - 1, -1, -1):
            cbr = branches[j]
            if is_downstream(br["root"], cbr["root"]):
                src_branch = cbr
                break
        if src_branch is None:
            treeroots.append(br)
        else:
            src_branch["branches"].append(br)

    return treeroots, branches


def find_endloops(topol: Dict):
    endpoints = list()
    treeroots, branches = build_branchtree(topol)
    for branch in branches:
        if len(branch['branches']) == 0:
            endpoint = 0.5*(branch['root']['x2'] + branch['root']['y1'])
            endpoints.append(endpoint)
    return endpoints


def is_downstream(branch, upbranch):
    if branch["x1"] < upbranch["x1"]:
        return False
    if branch["y1"] > upbranch["y1"]:
        return False
    return True
