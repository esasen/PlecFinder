import os,sys
import numpy as np
from typing import Dict, Any


########################################################################
########################################################################
########################################################################

def build_branchtree(topol: Dict[str,Any]):
    """ build branch tree for chain topology

        Arguments:
        ----------
            topol : dictionary
                topology dictionary

        Returns:
        ----------
            tree structure of branches
                list of lists
    """
    if not topol['no_overlap']:
        raise ValueError("Requires branchoverlap to be removed! Set no_overlap to True when running find_plecs")

    treeroot = list()
    branches = [{'root': branch, 'branches': list()} for branch in topol['branches']]

    for i,br in enumerate(branches):
        src_branch = None
        for j in range(i-1,-1,-1):
            cbr = branches[j]
            if is_downstream(br['root'],cbr['root']):
                src_branch = cbr
                break
        if src_branch is None:
            treeroot.append(br)
        else:
            src_branch['branches'].append(br)

    return treeroot,branches

def is_downstream(branch,upbranch):
    if branch['x1'] < upbranch['x1']:
        return False
    if branch['y1'] > upbranch['y1']:
        return False
    return True
