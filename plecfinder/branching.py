import os,sys
import numpy as np
from   numba import jit

########################################################################
########################################################################
########################################################################

# ~ def find_plectonemes(conf: np.ndarray,min_writhe_density: float,plec_min_writhe: float ,disc_len=None, no_branch_overlap=True ,connect_dist=10.0, om0=1.76,include_wm=False):
    
    """ Calculates the topology of a given configuration.

        Arguments:
        ----------
            conf : np.ndarray
                3D configruation, should be Nx3 numpy array containing the position vectors
            
            min_writhe_dens : float   
                minimum writhe density for a region to be detected as as plectonemic coil
            
            plec_min_writhe : float
                minimum writhe for a coil to be identified as a plectoneme
            
            disc_len :  float, optional       
                discretization length, if None discretization length will be calculated based on 
                provided configuration (default: None)
                
            no_branch_overlap: bool, optional
                remove overlap of neighboring branches (default: True)

            connect_dist: float, optional
                distance in nm for which neighboring points of sufficient writhedensity points are connected to form a branch (default: 10nm)
            
            om0: float, optional
                intrinsic twist (default: 1.76 rad/nm)
                
            include_wm: bool, optional
                include writhemap in return dictionary. This may lead to large memory consumption. (default: False)
            
        Returns:
        ----------
            topology dictionary:
            
                ### Keys:
                - N :         number of chain segments
                - L : Length of chain
                - disc_len : discretization length (segment size)
                - wr :  total writhe in configuration
                - num_plecs :  number of plectonemes
                - num_branches :  list of branches
                - num_tracers :  list of tracers
                - plecs :     list of plectonemes
                - branches :  list of branches
                - tracers :  list of tracers
                - wm : writhe map (this key is optional)

                Elements of the plectoneme list are dictionaries themselves. 
                ### Plectoneme Keys:
                - id1 : entrance index
                - id2 : exit index
                - wrdens : writhe density within plectoneme
                - wr : total writhe in plectoneme
                - num_segs : number of contained segments
                - L : length of plectoneme
                - branch_ids : indices of branches and tracers contained in plectoneme

                Banches and Tracers are likewise dictionaries. 
                ### Branch keys:
                - id : index in branches list
                - x1 : entrance x id
                - x2 : exit x id
                - y1 : entrance y id
                - y2 : exit y id

                ### Tracer keys:
                - id : index in tracers list
                - points : list of points tracing the branch, each of which contains an x index and y index for the two pairs consituting the two segments on opposing strands of the superhelix 
            
    """
  
    
# ~ @jit(nopython=True,cache=True) 
# ~ def 

