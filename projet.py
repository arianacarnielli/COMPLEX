#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 16:33:23 2019

@author: Ariana CARNIELLI
"""

"""
Méthodes initiales pour le projet de COMPLEX
"""
import networkx as nx
import numpy as np

class Graphe:
    
    def __init__(self):
        """
        """
        self.graphe = nx.Graph()

    
    def readFile(self, nomfichier):
        """
        """
        with open(nomfichier, 'r') as file:
            assert file.readline() == "Nombre de sommets\n"
            nbSommets = int(file.readline())
            assert file.readline() == "Sommets\n"
            
            for i in range(nbSommets):
                nomSommet = int(file.readline())
                self.graphe.add_node(nomSommet)
 
            assert file.readline() == "Nombre d aretes\n"
            nbAretes = int(file.readline())
            assert file.readline() == "Aretes\n"
            
            for i in range(nbAretes):
                line = file.readline()
                debut, fin = line.split(" ")
                debut = int(debut)
                fin = int(fin)
                self.graphe.add_edge(debut, fin)
    
    
    def supprimerSommet(self, sommet):
        """
        """
        g2 = Graphe()
        g2.graphe = nx.Graph(self.graphe)
        g2.graphe.remove_node(sommet)
        
        return g2
        
    def supprimerSommets(self, sommets):
        """
        """
        g2 = Graphe()
        g2.graphe = nx.Graph(self.graphe)
        g2.graphe.remove_nodes_from(sommets)
        return g2   
           
    def degresSommet(self):
        """
        """
        return dict(self.graphe.degree())
    
    def degreMax(self):
        """
        """
        degres = self.degresSommet()
        return max(degres, key=lambda key: degres[key])

    def creerAlea(self, nbSommets, probaArete):
        """
        """
        self.graphe.add_nodes_from(np.arange(nbSommets))
            
        for i in range(nbSommets):
            for j in range(i + 1, nbSommets):
                if np.random.rand() <= probaArete:
                    self.graphe.add_edge(i, j)
            
            
    def algoCouplage(self):
        """
        """
        couverture = set()
        for arete in (self.graphe.edges):
            i, j = arete
            if (i not in couverture) and (j not in couverture):
                couverture.add(i)
                couverture.add(j)
        return couverture
    
    def algoGlouton(self):
        """
        """
        g = self
        couverture = set()
        while len(g.graphe.edges) != 0:
            v = g.degreMax()
            couverture.add(v)
            g = g.supprimerSommet(v)
        return couverture
    
    def algoBranchement(self, debug = False):
        """
        """
        #la pile reçoit les sommets retirés du graphe aka une couverture partielle
        pile = []
        #on commence avec la couverture partielle vide
        pile.append(set())
        
        #compteur de noeuds visités
        n = 0
        
        couvMin = set(self.graphe.nodes)
        
        while pile != []:
            #on retire le dernier élément qui a été mis dans la pile
            couvPart = pile.pop()
            
            #on augmente le compteur de noeuds visites
            n += 1
            
            #on cree le graphe sans les sommets dans la couverture partiel
            gPart = self.supprimerSommets(couvPart)
            aretes = list(gPart.graphe.edges)
            
            #prints debug
            if debug:
                print(n)
                print(gPart.graphe.nodes)
                print(aretes)
            
            #si on a encore des aretes, on continue a empiler
            if len(aretes) > 0:
                u, v = aretes[0]
                pile.append(couvPart | {u})
                pile.append(couvPart | {v})
            #sinon on est au cas de base, on voit si la taille de la couverture
            #est plus petite que ce qu'on avait déjà
            else:
                couvMin = couvPart if len(couvPart) < len(couvMin) else couvMin
            
        return couvMin, n
    
    def algoBranchementBorne(self):
        """
        """
        #la pile reçoit les sommets retirés du graphe aka une couverture partielle
        pile = []
        #on commence avec la couverture partielle vide
        pile.append(set())
        
        couvMin = set(self.graphe.nodes)
        
        while pile != []:
            #on retire le dernier élément qui a été mis dans la pile
            couvPart = pile.pop()
            #on cree le graphe sans les sommets dans la couverture partiel
            gPart = self.supprimerSommets(couvPart)
            aretes = list(gPart.graphe.edges)
            
            #si on a encore des aretes, on continue a empiler
            if len(aretes) > 0:
                u, v = aretes[0]
                
                #calcul d'une solution realisable qui sert comme borne max
                #sur le graphe partiel par l'algorithme de couplage.
                coupPart = gPart.algoCouplage()
                
                #calcul d'une borne min
                n = len(gPart.graphe.nodes)
                m = len(gPart.graphe.edges)
                
                b1 = m // gPart.degreMax()
                
                b2 = borneMax 
                
                b3 = (2 * n - 1 - np.sqrt((2 *n - 1)**2 - 8 * m)) / 2
                
                borneMin = np.max(b1, b2, b3)
                
                #on ajoute les couvertures partiels a la pile que si on a la 
                #possibilité de trouver la solution maximale
                if borneMin <= borneMax:
                    pile.append(couvPart | {u})
                    pile.append(couvPart | {v})
            #sinon on est au cas de base, on voit si la taille de la couverture
            #est plus petite que ce qu'on avait déjà
            else:
                couvMin = couvPart if len(couvPart) < len(couvMin) else couvMin
            
        return couvMin
    
    
    
    
    
    
        