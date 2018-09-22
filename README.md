# KCureve simple implementation in python
_A very simple and non-optimizal version of SIGGRAPH2017 paper [k-Curves: Interpolation at Local Maximum Curvature](http://s2017.siggraph.org/technical-papers/sessions/sketching-curves) python implementation,just for presentation_

## Origin Paper
[paper link](http://faculty.cs.tamu.edu/schaefer/research/kcurves.pdf)

## REF
_some python libs used in this implementation_
- [matplotlib](https://matplotlib.org/tutorials/index.html)
- [numpy](https://docs.scipy.org/doc/)
- [scipy](https://www.scipy.org/docs.html)

## Deficiency
- Uses a non-optimized method to calculate C_i,1, should had used Cyclic tri - diagonal equations to calculate instead, it can both accelarating convergence and making the results more accurate, due to my poor code, it is rather hard for me to make what I had written clear ```T_T```, and I do not plan to spend too much time to fix it now...
- As a program which should focus on performance I really do not think my code is good enough, maybe it need some optimization to make it fast,maybe some CPython extensions...
- Do not implement the condition where the curve does not close.

