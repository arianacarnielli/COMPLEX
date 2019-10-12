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


            
            
            
            
            
        
            
