#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import numpy as np
from lib import fgeneric as fg, bbobbenchmarks as bb
from lib.support import *
from src import Ilot, globals as gb

datapath = 'out'
dimensions = (2,)
funs_id = (1,)
nb_run = 30

# function_ids = bbobbenchmarks.noisyIDs if len(argv) < 3 else eval(argv[2])

opts = dict(algid='SOS',
            comments='PUT MORE DETAILED INFORMATION, PARAMETER SETTINGS ETC')

t_start = time.time()
np.random.seed(int(t_start))

f = fg.LoggingFunction(datapath, **opts)


def run_optimizer_sos(f, dim, maxfunevals):
    """start the optimizer, allowing for some preparation.
    This implementation is an empty template to be filled

    """
    for _ in range(gb.NB_ILOTS):
        ilot = Ilot.Ilot(dim, gb.NB_INDIVUDUALS, f.evalfun)
        gb.ILOTS_LIST.append(ilot)

    for _ in range(maxfunevals/(gb.NB_INDIVUDUALS*gb.NB_ILOTS)):
        for ilot in gb.ILOTS_LIST:
            ilot.selection()

        if f.fbest < f.ftarget: break

    gb.ILOTS_LIST = []


def run_optimizer(fun, dim, maxfunevals, ftarget=-np.Inf):
    """start the optimizer, allowing for some preparation.
    This implementation is an empty template to be filled

    """
    # prepare
    x_start = 8. * np.random.rand(dim) - 4

    # call, REPLACE with optimizer to be tested
    PURE_RANDOM_SEARCH(fun, x_start, maxfunevals, ftarget)

def PURE_RANDOM_SEARCH(fun, x, maxfunevals, ftarget):
    """samples new points uniformly randomly in [-5,5]^dim and evaluates
    them on fun until maxfunevals or ftarget is reached, or until
    1e8 * dim function evaluations are conducted.

    """
    dim = len(x)
    maxfunevals = min(1e8 * dim, maxfunevals)
    popsize = min(maxfunevals, 200)
    fbest = np.inf

    for iter in range(0, int(np.ceil(maxfunevals / popsize))):
        xpop = 10. * np.random.rand(popsize, dim) - 5.
        fvalues = fun(xpop)
        idx = np.argsort(fvalues)
        if fbest > fvalues[idx[0]]:
            fbest = fvalues[idx[0]]
            xbest = xpop[idx[0]]
        if fbest < ftarget:  # task achieved
            break

    return xbest

for fun_id in funs_id:
    print '+++ date and time: %s' % (time.asctime())
    print('++ fun id: %d ' % fun_id)

    for dim in dimensions:
        print('++ %d dimensions' % dim)

        for iinstance in xrange(nb_run):
            f.setfun(*bb.instantiate(fun_id, iinstance=iinstance))

            # run algo with args
            # f.evalfun: the function (to call with a vector)
            # dim: the number of dimensions
            # f.ftarget: the target to reach (+ or - np.Inf)\


            ###########################################################
            ###########################################################
            ###########################################################
            #                           Par ici
            ###########################################################
            ###########################################################
            ###########################################################


            ### Run avec notre algo
            run_optimizer_sos(f, dim,  10000)

            ### Run purement aleatoire (au pire on montre ces resultats xD)
            #run_optimizer(f.evalfun, dim,  10000, f.ftarget)

            f.finalizerun()

            print('+ instance %d: fbest-ftarget=%.4e in %d evaluations,'
                  ' elapsed time [s]: %.2f'
                  % (iinstance, f.fbest - f.ftarget, f.evaluations,
                     (time.time()-t_start)))
