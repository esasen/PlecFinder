import numpy as np

from ._writhemap_python import wmp_writhemap_klenin1a
from ._writhemap_numba  import wmn_writhemap_klenin1a
from ._writhemap_cython import wmc_writhemap_klenin1a

WM_METHODS = ['klenin1a']

def writhemap(config,method='klenin1a',implementation='cython'):
    
    if method not in WM_METHODS:
        raise ValueError(f"Method '{method}' not implemented")
    
    if method == 'klenin1a':

        if   implementation == 'numba':
            return wmn_writhemap_klenin1a(config)
        elif implementation == 'python':
            return wmp_writhemap_klenin1a(config)
        elif implementation == 'cython':
            return np.asarray(wmc_writhemap_klenin1a(config))
        else:
            raise ValueError(f"Invalid implementation '{implementation}' for method '{method}'")
            
    print('done')
