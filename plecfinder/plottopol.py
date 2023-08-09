import os,sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from typing import List, Dict, Any, Tuple

from .IOPolyMC.iopolymc import read_state, read_xyz
from .plecfinder import find_plecs, cal_disc_len

########################################################################
########################################################################
########################################################################
# plot plectonemes


def plot_topol(
    topol: Dict[str,Any], 
    savefn: str = None, 
    flip_positive: bool = True, 
    remove_negative_wr: bool = True, 
    branches: List = None,
    print_branch_writhe: bool = True
):
    ###############################################
    # defines
    label_fontsize = 8
    tick_labelsize = 7
    branch_label_fontsize = 5
    ###############################################

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
        
        if print_branch_writhe:
            midpoint = 0.5 * ( branch["x1"] +  branch["x2"] )
            ax1.text(
                midpoint,
                branch["y2"] + N * 0.002,
                r"$Wr = %.2f$" % branch["wr"],
                verticalalignment="bottom",
                horizontalalignment="center",
                fontsize=branch_label_fontsize,
            )
        
        

    print(f'num plecs: {len(topol["plecs"])}')
    for plec in topol["plecs"]:
        ax1.add_patch(
            Rectangle(
                (plec["id1"], plec["id1"]),
                (plec["id2"] - plec["id1"]),
                (plec["id2"] - plec["id1"]),
                edgecolor="black",
                facecolor="none",
                fill=False,
                lw=1,
                alpha=1,
            )
        )

        midpoint = 0.5 * ( plec["id1"] +  plec["id2"] ) 
        ax1.text(
            midpoint,
            plec["id2"] + N * 0.01,
            r"$Wr = %.2f$" % plec["wr"],
            verticalalignment="bottom",
            horizontalalignment="center",
            fontsize=label_fontsize,
        )

        # boundary text
        # ~ ax1.text(plec['id1'], plec['id1']-N*0.01, r'$%d$'%plec['id1'],
        # ~ verticalalignment='top', horizontalalignment='left',fontsize=tick_labelsize)
        # ~ ax1.text(plec['id2'], plec['id1']-N*0.01, r'$%d$'%plec['id2'],
        # ~ verticalalignment='top', horizontalalignment='left',fontsize=tick_labelsize)

    if branches is not None:
        for br in branches:
            if len(br["branches"]) > 0:
                for cbr in br["branches"]:
                    ax1.plot(
                        [br["root"]["x2"], cbr["root"]["x1"]],
                        [br["root"]["y1"], cbr["root"]["y2"]],
                        color="black",
                        lw=1,
                    )
                    ax1.plot(
                        [br["root"]["y1"], cbr["root"]["y2"]],
                        [br["root"]["x2"], cbr["root"]["x1"]],
                        color="black",
                        lw=1,
                    )
            if len(br["branches"]) > 1 or len(br["branches"]) == 0:
                ax1.add_patch(
                    Rectangle(
                        (br["root"]["x1"], br["root"]["x1"]),
                        (br["root"]["y2"] - br["root"]["x1"]),
                        (br["root"]["y2"] - br["root"]["x1"]),
                        edgecolor="black",
                        facecolor="none",
                        linestyle="--",
                        fill=False,
                        lw=1,
                        alpha=0.7,
                    )
                )

    ax1.xaxis.tick_bottom()
    ax1.tick_params(labelsize=tick_labelsize, direction="in")
    ax1.tick_params(axis="x", pad=1)
    ax1.tick_params(axis="y", pad=1.8)
    fig.subplots_adjust(
        left=0.10, right=0.99, top=0.994, bottom=0.09, wspace=0.30, hspace=0.04
    )

    plt.tight_layout()
    if savefn is None:
        plt.show()
    else:
        fig.savefig(savefn + ".pdf", dpi=300, transparent=True, bbox_inches="tight")
        fig.savefig(savefn + ".png", dpi=300, transparent=False, bbox_inches="tight")
        plt.close()

  
def plot_single(fn: str, snapshot: int, min_wd: float, min_writhe: float, connect_dist: float=10., om0: float=1.76, no_overlap: float=True):
    if os.path.splitext(fn.lower())[-1] == '.state':
        state = read_state(fn)
        configs = state["pos"]
    elif os.path.splitext(fn.lower())[-1] == '.xyz':
        xyz = read_xyz(fn)
        configs = xyz['pos']
    else:
        raise ValueError(f'Unknown filetype of file "{fn}"')
    
    if len(configs) < snapshot-1:
        raise ValueError(f'Attempting to access snapshot {snapshot}, but provided file only contains {len(configs)} snapshots.')
    
    config = configs[snapshot]
    disc_len = cal_disc_len(config)
    
    topol = find_plecs(
        config,
        min_writhe_density=min_wd,
        plec_min_writhe=min_writhe,
        disc_len=disc_len,
        no_overlap=no_overlap,
        connect_dist=connect_dist,
        om0=om0,
        include_wm=True,
        )
    
    outpath = os.path.splitext(fn)[0]
    if not os.path.exists(outpath):
        os.makedirs(outpath)
        
    settingsname = (
        "mwd%s_mwr%s_cd%s" % (min_wd, min_writhe, connect_dist)
    ).replace(".", "p")
    figpath = outpath + "/figs_" + settingsname
    if not os.path.exists(figpath):
        os.makedirs(figpath)
    figfn = figpath + "/snapshot_%d" % snapshot
    plot_topol(topol, savefn=figfn)
          
    
    
    
########################################################################
########################################################################
########################################################################


if __name__ == '__main__':
    
    if len(sys.argv) < 3:
        print("usage: python %s fn snapshot min_wd min_writhe" %sys.argv[0])
        sys.exit(0)
    
    fn = sys.argv[1]
    snapshot = int(sys.argv[2])
    min_wd     = float(sys.argv[3])
    min_writhe = float(sys.argv[4])

    plot_single(fn, snapshot, min_wd, min_writhe, connect_dist=10., om0=1.76, no_overlap=True)