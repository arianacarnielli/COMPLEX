# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 22:55:40 2019

@author: arian
"""
from projet import Graphe
from progressBar import ProgressBar

import time as t
import numpy as np

def testTempsN(nMax, p, nomMethode, fois = 10, **kwargs):
    """
    """
    n = np.linspace(nMax / 10, nMax, 10, dtype = int)
    res = np.zeros(n.shape)
    progressBar = ProgressBar(maxValue = n.size * fois)
    
    for ni in range(n.size):
        for f in range(fois):
            progressBar.update(ni * fois + f + 1)
            graphe = Graphe(nbSommets = n[ni], probaArete = p)
            start =  t.process_time()
            getattr(graphe, nomMethode)(**kwargs)
            res[ni] += t.process_time() - start
    print("")
    
    return res / fois, n

def testTempsPfunc(nMax, p, nomMethode, fois = 10, **kwargs):
    """
    """
    n = np.linspace(nMax / 10, nMax, 10, dtype = int)
    res = np.zeros(n.shape)
    progressBar = ProgressBar(maxValue = n.size * fois)
    
    for ni in range(n.size):
        for f in range(fois):
            progressBar.update(ni * fois + f + 1)
            graphe = Graphe(nbSommets = n[ni], probaArete = p(n[ni]))
            start =  t.process_time()
            getattr(graphe, nomMethode)(**kwargs)
            res[ni] += t.process_time() - start
    print("")
    
    return res / fois, n

def testEcart(nMax, p, nomMethode, fois = 10):
    """
    """
    n = np.linspace(nMax / 10, nMax, 10, dtype = int)
    res = np.zeros((n.size, fois))
    progressBar = ProgressBar(maxValue = n.size * fois)
    
    for ni in range(n.size):
        for f in range(fois):
            progressBar.update(ni * fois + f + 1)
            graphe = Graphe(nbSommets = n[ni], probaArete = p)
            resMethode = getattr(graphe, nomMethode)()
            resExacte, _ = graphe.algoBranchementAmeliore(sommetMax = True, elimDegre1 = True)
            res[ni, f] = len(resMethode) / len(resExacte) if len(resExacte) != 0 else 1
    print("")
    
    return res, n

def testNoeud(n, p, listAlgo):
    """
    """
    assert n.size == p.size
    res = np.zeros((len(listAlgo), n.size), dtype = int)
    progressBar = ProgressBar(maxValue = n.size * len(listAlgo))
    
    for ni in range(n.size):
        for i, (algoName, algoArgs) in enumerate(listAlgo):
            progressBar.update(ni * len(listAlgo) + i + 1)
            graphe = Graphe(nbSommets = n[ni], probaArete = p[ni])
            _, noeuds = getattr(graphe, algoName)(**algoArgs)
            res[i, ni] = noeuds
    print("")
    
    return res
    
