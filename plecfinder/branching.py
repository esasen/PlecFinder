import os, sys
import numpy as np
from typing import Dict, Any, List, Tuple
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

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


def connect_branchtrees(treeroots,branches,combine_dist,disc_len):
    combine_segs = int(np.ceil(combine_dist/disc_len))
    
    # find clusters
    curr = [treeroots[0]]
    clusters = [curr]
    for i in range(1,len(treeroots)):
        segdist = treeroots[i]['root']['x1'] - curr[-1]['root']['y2'] 
        if segdist <= combine_segs:
            curr.append(treeroots[i])
        else:
            curr = [treeroots[i]]
            clusters.append(curr)
    
    extended_branches = [branch for branch in branches]
    # unify clusters
    unified_treeroots=[]
    for cluster in clusters:
        if len(cluster) == 1:
            unified_treeroots.append(cluster[0])
        else:
            x1 = cluster[0]['root']['x1']
            x2 = x1+1
            y2 = cluster[-1]['root']['y2']
            y1 = y2-1
            wr = 0
            wr_down = np.sum([tb['root']['wr_down'] for tb in cluster])
            id = 10000
            root = {
                'id': id, 
                'x1': x1, 
                'x2': x2, 
                'y1': y1, 
                'y2': y2, 
                'wr': wr, 
                'wr_down': wr_down
                }
            mainbranch = {
                'root' : root,
                'branches' : cluster
            }
            unified_treeroots.append(mainbranch)
            extended_branches.append(mainbranch)
    return unified_treeroots,extended_branches


def number_of_branches(topol, min_downstream_writhe: float = 0) -> List[int]: 
    treeroots, branches = build_branchtree(topol)
    return [len(looplevels) for looplevels in endloop_levels(topol, min_downstream_writhe)]


def endloop_levels(topol, min_downstream_writhe: float = 0) -> List[int]:
    def _move_downstream(treebranch,level):
        sbs = [sb for sb in treebranch['branches'] if _valid_downstream_branch(sb,min_downstream_writhe)]
        if len(sbs) == 0:
            return [level]
        if len(sbs) == 1:
            return _move_downstream(sbs[0],level)
        else:
            partial_endloops = []
            for sb in sbs:
                partial_endloops += _move_downstream(sb,level+1)
            return partial_endloops
            
    treeroots, branches = build_branchtree(topol)
    plec_endloops=[_move_downstream(treeroot,0) for treeroot in treeroots if _valid_downstream_branch(treeroot,min_downstream_writhe)]
    return plec_endloops


def unify_branch_pieces(topol: Dict[str,Any]) -> Dict[str,Any]:  
    treeroots, treebranches = build_branchtree(topol)
    for treebranch in treebranches:
        if 'rm' in treebranch['root']:
            continue
        if len(treebranch["branches"]) == 1:
            subbr = treebranch["branches"][0]
            treebranch["root"]['wr'] = treebranch["root"]['wr'] + subbr['root']['wr']
            treebranch["root"]['x2'] = subbr['root']['x2']
            treebranch["root"]['y1'] = subbr['root']['y1']
            treebranch['branches'] = subbr['branches']
            # flag subbranch for deletition
            subbr['root']['rm'] = True
    topol['branches'] = [branch for branch in topol['branches'] if 'rm' not in branch]      
    return topol


def _valid_downstream_branch(branch,min_downstream_writhe: float):
    return np.abs(branch['root']['wr_down']) > min_downstream_writhe


def plot_branchtree(
    branchtree,
    topol,
    flip_positive: bool = True, 
    remove_negative_wr: bool = True, 
    ):
    
    colors = list()
    for i in range(100):
        colors += plt.get_cmap("tab20c").colors
    
    N = topol["N"]
    fig = plt.figure(
        figsize=(2 * 8.7 / 2.54, 2 * 8.7 / 2.54), dpi=100, facecolor="w", edgecolor="k"
    )
    ax1 = plt.subplot2grid((1, 1), (0, 0), colspan=1, rowspan=1)
    ax1.plot([0, N], [0, N], lw=2, alpha=0.5, color="black")
    if "wm" in topol.keys():
        print("has wm")
        wm = np.array(topol["wm"])
        if flip_positive:
            wm = np.sign(np.mean(wm)) * wm
        if remove_negative_wr:
            wm[wm < 0] = 0
        ax1.matshow(
            wm.T, cmap=plt.get_cmap("Greys"), aspect="auto", interpolation="none"
        )
    ax1.set_xlim([0, N])
    ax1.set_ylim([0, N])
    
    for i, tracer in enumerate(topol["tracers"]):
        tpts = np.array(tracer["points"])
        ax1.scatter(tpts[:, 0], tpts[:, 1], s=8, color=colors[i])
        ax1.scatter(tpts[:, 1], tpts[:, 0], s=8, color=colors[i])
        ax1.plot(tpts[:, 0], tpts[:, 1], color="black", lw=0.5)
        ax1.plot(tpts[:, 1], tpts[:, 0], color="black", lw=0.5)

    for i, branch in enumerate(topol["branches"]):
        color = colors[i]
        ax1.add_patch(
            Rectangle(
                (branch["x1"], branch["y1"]),
                (branch["x2"] - branch["x1"]),
                (branch["y2"] - branch["y1"]),
                edgecolor="black",
                facecolor="none",
                fill=False,
                lw=1,
                alpha=0.5,
            )
        )
        ax1.fill_between(
            [branch["x1"], branch["x2"]],
            [branch["y1"], branch["y1"]],
            [branch["y2"], branch["y2"]],
            alpha=0.5,
            color=colors[i],
        )
        ax1.add_patch(
            Rectangle(
                (branch["y1"], branch["x1"]),
                (branch["y2"] - branch["y1"]),
                (branch["x2"] - branch["x1"]),
                edgecolor="black",
                facecolor="none",
                fill=False,
                lw=1,
                alpha=0.5,
            )
        )
        ax1.fill_between(
            [branch["y1"], branch["y2"]],
            [branch["x1"], branch["x1"]],
            [branch["x2"], branch["x2"]],
            alpha=0.5,
            color=colors[i],
        )
        
    def plot_branch(branch):
        root = branch['root']
        ax1.add_patch(
            Rectangle(
                (root['x1'], root['x1']),
                (root["y2"] - root["x1"]),
                (root["y2"] - root["x1"]),
                edgecolor="black",
                facecolor="none",
                fill=False,
                lw=1,
                alpha=1,
            )
        )
        for br in branch['branches']:
            plot_branch(br)
    
    for br in branchtree:
        plot_branch(br)
    plt.show()