import os, sys
import time

from .plottopol import plot_topol
from .plecfinder import find_plecs, cal_disc_len
from .tofile import save_topol, load_topol, load_topol_by_specs
from .IOPolyMC.iopolymc.xyz import read_xyz

########################################################################
########################################################################
########################################################################


def xyz2plecs(
    xyzfn: str,
    min_writhe_density: float,
    min_writhe: float,
    connect_dist: float = 10,
    no_overlap=True,
    om0=1.76,
    plot_every=0,
    save=False,
    load=False,
    include_wm=False,
):
    if load or save or plot_every > 0:
        outpath = xyzfn.replace(".xyz", "")
        if not os.path.exists(outpath):
            os.makedirs(outpath)

        settingsname = (
            "mwd{min_writhe_density}_mwr{min_writhe}_cd{connect_dist}"
        ).replace(".", "p")
        plec_fn = outpath + "/topols_" + settingsname

    # load from file
    if load:
        topols = load_topol_by_specs(outpath, min_writhe_density, min_writhe, connect_dist)
        # topols = load_topol(plec_fn)
        if topols is not None:
            return topols

    # load xyz
    xyz = read_xyz(xyzfn)
    configs = xyz["pos"]
    disc_len = None

    # make directory for plots
    if plot_every > 0:
        figpath = outpath + "/figs_" + settingsname
        if not os.path.exists(figpath):
            os.makedirs(figpath)

    # calculate discretization length
    if disc_len is None:
        disc_len = cal_disc_len(configs[0])

    # loop over configurations and calculate topology
    topols = list()

    t1 = time.time()
    print_every = 100
    for i, config in enumerate(configs):
        if i % print_every == 0 and i != 0:
            print(f"Config {i}/{len(configs)}")
            t2 = time.time()
            print("dt = %.2f s (%.4f s/config)" % (t2 - t1, (t2 - t1) / print_every))
            t1 = time.time()

        # plot topology
        topol = find_plecs(
            config,
            min_writhe_density=min_writhe_density,
            plec_min_writhe=min_writhe,
            disc_len=disc_len,
            no_overlap=no_overlap,
            connect_dist=connect_dist,
            om0=om0,
            include_wm=include_wm,
        )

        topols.append(topol)

        # plot topology
        if plot_every > 0:
            if i % plot_every == 0:
                figfn = figpath + "/snapshot_%d" % i
                print(figfn)
                plot_topol(topol, savefn=figfn)

    # save topology
    if save:
        save_topol(plec_fn, topols)
    return topols


########################################################################
########################################################################
########################################################################

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(
            "usage: python %s min_wd min_writhe connect_dist plot_every xyzfns"
            % sys.argv[0]
        )
        sys.exit(0)

    min_writhe = 0.25
    connect_dist = 25.0
    om0 = 1.76

    include_wm = False
    load = True
    save = True

    min_wd = float(sys.argv[1])
    min_writhe = float(sys.argv[2])
    connect_dist = float(sys.argv[3])
    plot_every = int(sys.argv[4])
    xyzfns = sys.argv[5:]

    xyzfns = [fn for fn in xyzfns if os.path.isfile(fn)]
    print("%d statefiles found" % len(xyzfns))
    for xyzfn in xyzfns:
        
        print('evaluating "%s"' % xyzfn)
        t1 = time.time()
        topols = xyz2plecs(
            xyzfn,
            min_wd,
            min_writhe=min_writhe,
            connect_dist=connect_dist,
            om0=om0,
            plot_every=plot_every,
            save=save,
            load=load,
            include_wm=include_wm,
        )
        t2 = time.time()
        print(f"timing = {t2-t1}")
