# PlecFinder
Analyzes the topology of polymer configurations

## Install
```
git clone https://github.com/eskoruppa/PlecFinder.git
```



### Required packages:






### Topology Dictionary Keys:
- N :         number of chain segments
- L : Length of chain
- disc_len : discretization length (segment size)
- plecs :     list of plectonemes
- wr :  total writhe in configuration
- num_plecs :  number of plectonemes
- num_branches :  list of branches
- num_tracers :  list of tracers
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
        
        
## Writhe Map
Methods to calculate the writhe map are contained in the directory CalWM/. The is a cython, a numba and a bare python implementation of method 1 from Klenin et al (Ref. [1]). Cython is recommended as it is several times faster than the numba implementation but it requires compilation. To compile execute the bash script: ./compile.sh


1. Klenin, K., & Langowski, J. (2000). Computation of writhe in modeling of supercoiled DNA. Biopolymers, 54(5), 307–317. [https://doi.org/10.1002/1097-0282(20001015)54:5<307::AID-BIP20>3.0.CO;2-Y](https://doi.org/10.1002/1097-0282(20001015)54:5<307::AID-BIP20>3.0.CO;2-Y)
