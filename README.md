# PlecFinder
Analyzes the topology of polymer configurations











## Writhe Map
Methods to calculate the writhe map are contained in the directory CalWM/. The is a cython, a numba and a bare python implementation of method 1 from Klenin et al (Ref. [1]). Cython is recommended as it is several times faster than the numba implementation but it requires compilation. To compile execute the bash script: ./compile.sh


1. Klenin, K., & Langowski, J. (2000). Computation of writhe in modeling of supercoiled DNA. Biopolymers, 54(5), 307–317. https://doi.org/10.1002/1097-0282(20001015)54:5
