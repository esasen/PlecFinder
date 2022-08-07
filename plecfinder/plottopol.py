import numpy as np
import os,sys,glob
import json
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Rectangle
from cycler import cycler

########################################################################
########################################################################
########################################################################
# plot plectonemes

def plot_topol(topol,savefn=None,flip_positive=True,remove_negative_wr=True):
    ###############################################
    # defines
    label_fontsize = 8
    tick_labelsize = 7
    ###############################################
    
    colors = list()
    for i in range(100):
        colors += plt.get_cmap('tab20c').colors

    N      = topol['N']
    
    fig = plt.figure(figsize=(2*8.7/2.54,2*8.7/2.54), dpi=100, facecolor='w',edgecolor='k')
    ax1 = plt.subplot2grid((1,1), (0, 0),colspan=1,rowspan=1)

    ax1.plot([0,N],[0,N],lw=2,alpha=0.5,color='black')
    if 'wm' in topol.keys(): 
        wm = np.array(topol['wm'])
        if flip_positive:
            wm = np.sign(np.mean(wm))*wm
        if remove_negative_wr:
            wm[wm<0] = 0
        ax1.matshow(wm.T,cmap=plt.get_cmap('Greys'),aspect='auto',interpolation='none')
    ax1.set_xlim([0,N])
    ax1.set_ylim([0,N])

    for i,tracer in enumerate(topol['tracers']):
        tpts = np.array(tracer['points'])
        ax1.scatter(tpts[:,0],tpts[:,1],s=8,color=colors[i])
        ax1.scatter(tpts[:,1],tpts[:,0],s=8,color=colors[i])
        ax1.plot(tpts[:,0],tpts[:,1],color='black',lw=0.5)
        ax1.plot(tpts[:,1],tpts[:,0],color='black',lw=0.5)

    for i,branch in enumerate(topol['branches']):
        color = colors[i]
        ax1.add_patch(Rectangle((branch['x1'],branch['y1']), (branch['x2']-branch['x1']), (branch['y2']-branch['y1']),
             edgecolor = 'black',
             facecolor = 'none',
             fill=False,
             lw=1,
             alpha=0.5))
        ax1.fill_between([branch['x1'],branch['x2']], [branch['y1'],branch['y1']],[branch['y2'],branch['y2']],alpha=0.5,color=colors[i])

        ax1.add_patch(Rectangle((branch['y1'],branch['x1']), (branch['y2']-branch['y1']), (branch['x2']-branch['x1']),
             edgecolor = 'black',
             facecolor = 'none',
             fill=False,
             lw=1,
             alpha=0.5))   
        ax1.fill_between([branch['y1'],branch['y2']], [branch['x1'],branch['x1']],[branch['x2'],branch['x2']],alpha=0.5,color=colors[i])
             
    for plec in topol['plecs']:
        ax1.add_patch(Rectangle((plec['id1'],plec['id1']), (plec['id2']-plec['id1']), (plec['id2']-plec['id1']),
             edgecolor = 'black',
             facecolor = 'none',
             fill=False,
             lw=1,
             alpha=1))
        
        midpoint = (0.2*plec['id1']+0.8*plec['id2'])
        ax1.text(midpoint, plec['id2']+N*0.01, r'$Wr = %.2f$'%plec['wr'], 
            verticalalignment='bottom', horizontalalignment='right',fontsize=label_fontsize)
        
        # boundary text    
        # ~ ax1.text(plec['id1'], plec['id1']-N*0.01, r'$%d$'%plec['id1'], 
            # ~ verticalalignment='top', horizontalalignment='left',fontsize=tick_labelsize)
        # ~ ax1.text(plec['id2'], plec['id1']-N*0.01, r'$%d$'%plec['id2'], 
            # ~ verticalalignment='top', horizontalalignment='left',fontsize=tick_labelsize)
    
    
    ax1.xaxis.tick_bottom()
    ax1.tick_params(labelsize = tick_labelsize,direction="in")
    ax1.tick_params(axis="x", pad=1)
    ax1.tick_params(axis="y", pad=1.8)
    fig.subplots_adjust(left=0.10, right=0.99, top=0.994, bottom=0.09,wspace=0.30, hspace=0.04)
    
    plt.tight_layout()
    if savefn is None:
        plt.show()
    else:
        fig.savefig(savefn+'.pdf',dpi=300, transparent=True,bbox_inches='tight')
        fig.savefig(savefn+'.png',dpi=300, transparent=False,bbox_inches='tight')
        plt.close()

    
########################################################################
########################################################################
########################################################################

