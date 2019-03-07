import numpy as np

class Fiber_level:
    def fiber_level_getK(d, section_deformations, nof, fibyy1,fibyy2, fibxx1, fibxx2):
        section_strain = np.zeros(nof)
        for fib in range(0,nof):
            yoffib = (d / 2) * (1 - (1 / nof) - 2 * (fib - 1) / nof);
            strainfib = np.dot([1 - yoffib] * section_deformations);
            section_strain[fib] = strainfib;
            for fibx in range(0,nofx):
                if(strainfib<0):
                    if(fib>=fibyy1 and fib<=fibyy2 and fibx>=fibxx1 and fibx<=fibxx2):
                        sigmafib = (fcc_dash*(strainfib/E_cc)*r)/(r-1+(strainfib/E_cc)^r)