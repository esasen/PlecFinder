import os,sys
import numpy as np
from   numba import jit

########################################################################
########################################################################
########################################################################

def build_branchtree(topol):
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
    if not topol[no_overlap]:
        raise ValueError("Requires branchoverlap to be removed! Set no_overlap to True when running find_plecs")

    branches = [[branch,list()] for branch in topol['branches']]



def is_downstream(branch,upbranch):
    if branch[]



    
# ~ @jit(nopython=True,cache=True) 
# ~ def 

