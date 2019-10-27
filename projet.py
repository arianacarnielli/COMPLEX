#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 16:33:23 2019

@author: Ariana CARNIELLI
Méthodes pour le projet de COMPLEX 2019-2020
"""

import networkx as nx
import numpy as np

class Graphe:
    """
    Classe pour representer des graphes non orientés.
    Contient des fonctions de creation, manipulation et des algorithmes pour
    le calcul exact et approché d'une couverture minimale.
    Utilise le module networkx pour manipuler des graphes.
    
    Attributs :
        graphe : objet du type networkx.Graph. 
    """
    
    def __init__(self, **kwargs):
        """
        Cree un graphe vide, depuis un fichier ou aléatoire. Le graphe est cree
        depuis un fichier si l'argument nomFichier est present. Sinon, il est 
        cree de façon aleatoire si nbSommets et probaArete sont presents. 
        Args : 
            nomFichier (facultatif) : nom d'un fichier depuis lequel on lit le 
                graphe. Le format attendu est celui donné à l'enoncé.
            nbSommets (facultatif) : nombre de sommets du graphe aleatoire a 
                etre cree.
            probaArete (facultatif) : probabilite d'avoir une arete (i, j) au 
                graphe aleatoire, i et j deux sommets quelconques. Les tirages
                sont independants.
        """
        self.graphe = nx.Graph()
        if "nomFichier" in kwargs:
            self._readFile(kwargs["nomFichier"])
        elif "nbSommets" in kwargs and "probaArete" in kwargs:
            self._creerAlea(kwargs["nbSommets"], kwargs["probaArete"])

#==============================================================================
# Fonctions de creation et manipulation
#==============================================================================
    
    def _readFile(self, nomFichier):
        """
        Modifie l'attribut graphe, en lisant des donnees a partir d'un fichier.
        Args : 
            nomFichier : nom d'un fichier depuis lequel on lit le graphe. Le 
                format attendu est celui donné à l'enoncé.
        """
        with open(nomFichier, 'r') as file:
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
                
    def _creerAlea(self, nbSommets, probaArete):
        """
        Modifie l'attribut graphe, en creant nbSommets sommets et en rajoutant
        des aretes de façon aleatoire.
        Args :
            nbSommets : nombre de sommets du graphe aleatoire a etre cree.
            probaArete : probabilite d'avoir une arete (i, j) au graphe 
                aleatoire, i et j deux sommets quelconques. Les tirages sont 
                independants.
        """
        self.graphe.add_nodes_from(np.arange(nbSommets))
            
        for i in range(nbSommets):
            for j in range(i + 1, nbSommets):
                if np.random.rand() <= probaArete:
                    self.graphe.add_edge(i, j)
    
    def supprimerSommet(self, sommet):
        """
        Retourne un nouveau graphe g2 obtenu a partir de self en supprimant le 
        sommet sommet (et les aretes incidentes).
        Args :
            sommet : le sommet a etre retire.
        Returns :
            un nouveau graphe sans sommet.
        """
        g2 = Graphe()
        g2.graphe = nx.Graph(self.graphe)
        g2.graphe.remove_node(sommet)
        
        return g2
        
    def supprimerSommets(self, sommets):
        """
        Retourne un nouveau graphe g2 obtenu a partir de self en supprimant les 
        sommets dans la liste sommets (et les aretes incidentes).
        Args :
            sommets : liste de sommets a etre retires.
        Returns :
            un nouveau graphe sans sommets.
        """
        g2 = Graphe()
        g2.graphe = nx.Graph(self.graphe)
        g2.graphe.remove_nodes_from(sommets)
        return g2   
           
    def degresSommet(self):
        """
        Renvoie un dictionnaire contenant les degres des sommets du graphe.
        Returns : 
            un dictionnaire ou les cles sont les sommets et les valeurs sont
            les degres.
        """
        return dict(self.graphe.degree())
    
    def degreMax(self):
        """
        Retourne un sommet de degre maximum.
        Returns : 
            un sommet de degre maximum.
        """
        degres = self.degresSommet()
        return max(degres, key=lambda key: degres[key])
    
    def voisinsSommet(self, sommet):
        """
        Retourne l'ensemble des voisins d'un sommet donne.
        Args : 
            sommet : sommet dont on veut determiner les voisins.
        Returns :
            un ensemble des voisins de sommet.
        """
        return set(self.graphe[sommet])
    
#==============================================================================
# Fonctions por le probleme de la couverture minimale
#==============================================================================
            
    def algoCouplage(self):
        """
        Determine une solution 2-approche au probleme de la couverture minimale
        (Vertex cover) en utilisant un couplage. 
        Returns : 
            un ensemble de sommets qui forment une couverture du graphe.
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
        Determine une solution approche au probleme de la couverture minimale
        (Vertex cover) en utilisant un algorithme glouton qui selectionne les 
        sommets en ordre decroissant de degres.
        À chaque suppression de sommet, une nouvelle copie du graphe est faite.
        Returns : 
            un ensemble de sommets qui forment une couverture du graphe.
        """
        g = self
        couverture = set()
        while len(g.graphe.edges) != 0:
            v = g.degreMax()
            couverture.add(v)
            g = g.supprimerSommet(v)
        return couverture
    
    def algoGloutonSansCopies(self):
        """
        Determine une solution approche au probleme de la couverture minimale
        (Vertex cover) en utilisant un algorithme glouton qui selectionne les 
        sommets en ordre decroissant de degres.
        Une seule copie du graphe est faite au début et modifiée à chaque
        étape, ce qui permet d'accélerer l'exécution.
        Returns : 
            un ensemble de sommets qui forment une couverture du graphe.
        """
        g = Graphe()
        g.graphe = nx.Graph(self.graphe)
        couverture = set()
        while len(g.graphe.edges) != 0:
            v = g.degreMax()
            couverture.add(v)
            g.graphe.remove_node(v)
        return couverture
    
    def algoBranchement(self, debug = False):
        """
        Determine une solution exacte au probleme de la couverture minimale
        (Vertex cover) en utilisant un arbre binaire de recherche.
        Args : 
            debug (facultatif) : si True, affiche des messages a chaque etape
                montrant le fonctionnement etape a etape de l'algorithme.
        Returns : 
            Un tuple forme par un ensemble de sommets qui forment une 
            couverture minimale du graphe et les nombre des noeuds de l'arbre 
            parcourus.        
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
                print("nombre de sommets visités :", n)
                print("sommets dans la couverture partielle :", couvPart)
                print("sommets restants dans le graphe partiel :", gPart.graphe.nodes)
                print("aretes restants dans le graphe partiel :", aretes)
            #si on a encore des aretes, on continue a empiler
            if len(aretes) > 0:
                u, v = aretes[0]
                pile.append(couvPart | {v})
                pile.append(couvPart | {u})
            #sinon on est au cas de base, on voit si la taille de la couverture
            #est plus petite que ce qu'on avait déjà
            else:
                couvMin = couvPart if len(couvPart) < len(couvMin) else couvMin
        return couvMin, n
    
    def algoBranchementBorne(self, debug = False, methodeMax = 0, methodeMin = 0):
        """
        Determine une solution exacte au probleme de la couverture minimale
        (Vertex cover) en utilisant un arbre binaire de recherche et en coupant
        des branches par elagage a l'aide des bornes maximale et minimale.
        Args : 
            debug (facultatif) : si True, affiche des messages a chaque etape
                montrant le fonctionnement etape a etape de l'algorithme.
            methodeMax (facultatif) :
                0 : BorneMax calculé par l'algorithme de couplage 
                1 : BorneMax calculé par l'algorithme glouton
                2 : BorneMax calculé par la solution actuelle (naive)
            methodeMin (facultatif) :
                0 : BorneMin calculé par b1, b2, b3 
                (avec b2 calculé par l'algorithme de couplage)
                1 : BorneMin calculé par b1, b3
                2 : BorneMin calculé par la couverture partielle actuelle 
                (naive).
        Returns : 
            Un tuple forme par un ensemble de sommets qui forment une 
            couverture minimale du graphe et les nombre des noeuds de l'arbre 
            parcourus.  
        """
        #la pile reçoit les sommets retirés du graphe aka une couverture partielle
        pile = []
        #on commence avec la couverture partielle vide
        pile.append(set())
        #compteur de noeuds visités
        cpt = 0
        #couverture minimale actuelle
        couvMin = set(self.graphe.nodes)
        #borneMax pour l'elagage
        borneMax = len(couvMin) 
        while pile != []:
            #on retire le dernier élément qui a été mis dans la pile
            couvPart = pile.pop()
            #on cree le graphe sans les sommets dans la couverture partiel
            gPart = self.supprimerSommets(couvPart)
            aretes = list(gPart.graphe.edges)
            #on augmente le compteur de noeuds visites
            cpt += 1
            #prints debug
            if debug:
                print("nombre de sommets visités :", cpt)
                print("sommets dans la couverture partielle :", couvPart)
                print("sommets restants dans le graphe partiel :", gPart.graphe.nodes)
                print("aretes restants dans le graphe partiel :", aretes)
            #si on a encore des aretes, on continue a empiler
            if len(aretes) > 0:
                u, v = aretes[0]
                #calcul d'une solution realisable sur le graphe partiel pour borneMax
                if methodeMax == 0:
                #par l'algorithme de couplage
                    coupPart = gPart.algoCouplage()
                elif methodeMax == 1:
                    #par l'agorithme glouton
                    coupPart = gPart.algoGloutonSansCopies() 
                #mis-a-jour de la borneMax
                if methodeMax != 2:
                    borneMax = min(borneMax, (len(couvPart) + len(coupPart)))
                #calcul de la borneMin
                if methodeMin != 2:
                    n = len(gPart.graphe.nodes)
                    m = len(gPart.graphe.edges)              
                    degres = gPart.degresSommet()
                    b1 = np.ceil(m / max(degres.values()))
                    b3 = (2 * n - 1 - np.sqrt((2 *n - 1)**2 - 8 * m)) / 2
                    #on calcule b2 mais on n'a pas encore de couplage
                    if methodeMin == 0 and methodeMax != 0:
                        coupPart = gPart.algoCouplage()
                    if methodeMin == 0:
                        b2 = len(coupPart) / 2
                    #on ne calcule pas b2
                    else: 
                        b2 = 0
                    borneMin = len(couvPart) + max(b1, b2, b3) 
                #borneMin naive
                else: 
                    borneMin = len(couvPart)
                if debug:
                    print("bornes :", borneMin, borneMax)
                #on ajoute les couvertures partiels a la pile que si on a la 
                #possibilité de trouver la solution maximale
                if borneMin <= borneMax:
                    pile.append(couvPart | {v})
                    pile.append(couvPart | {u})
            #sinon on est au cas de base, on voit si la taille de la couverture
            #est plus petite que ce qu'on avait déjà
            else:
                couvMin = couvPart if len(couvPart) < len(couvMin) else couvMin
                borneMax = len(couvMin)
        return couvMin, cpt
    
    def algoBranchementAmeliore(self, debug = False, sommetMax = False, elimDegre1 = False):
        """
        Determine une solution exacte au probleme de la couverture minimale
        (Vertex cover) en utilisant un arbre binaire de recherche et en coupant
        des branches par elagage a l'aide des bornes maximale et minimale. La
        borne maximale est calculee par l'algorithme de couplage et la borne
        minimale par b1, b2, b3. A chaque branchement on rajoute, dans une 
        branche, un sommet et, dans l'autre, tous les voisins de ce sommet.
        Args : 
            debug (facultatif) : si True, affiche des messages a chaque etape
                montrant le fonctionnement etape a etape de l'algorithme.
            sommetMax (facultatif) : si True, le sommet pris a chaque etape est
                un sommet de degre maximal. Sinon c'est un sommet quelconque.               
            elimDegre1 (facultatif) : si True, ne cree pas une branche pour un 
            sommet de degre 1.
        Returns : 
            Un tuple forme par un ensemble de sommets qui forment une 
            couverture minimale du graphe et les nombre des noeuds de l'arbre 
            parcourus.  
        """
        #la pile reçoit les sommets retirés du graphe aka une couverture partielle
        pile = []
        #on commence avec la couverture partielle vide
        pile.append(set())
        #compteur de noeuds visités
        cpt = 0
        #couverture minimale actuelle
        couvMin = set(self.graphe.nodes)
        #borneMax pour l'elagage
        borneMax = len(couvMin)
        while pile != []:
            #on retire le dernier élément qui a été mis dans la pile
            couvPart = pile.pop()
            #on cree le graphe sans les sommets dans la couverture partiel
            gPart = self.supprimerSommets(couvPart)
            aretes = list(gPart.graphe.edges)
            #on augmente le compteur de noeuds visites
            cpt += 1
            #prints debug
            if debug:
                print("nombre de sommets visités :", cpt)
                print("sommets dans la couverture partielle :", couvPart)
                print("sommets restants dans le graphe partiel :", gPart.graphe.nodes)
                print("aretes restants dans le graphe partiel :", aretes)
            #si on a encore des aretes, on continue a empiler
            if len(aretes) > 0:
                #on prend le sommet de plus grand degré
                if sommetMax:
                    u = gPart.degreMax()    
                else:
                    u, _ = aretes[0]
                #calcul d'une solution realisable sur le graphe partiel pour borneMax
                #par l'algorithme de couplage
                coupPart = gPart.algoCouplage()
                #mis-a-jour de la borneMax
                borneMax = min(borneMax, (len(couvPart) + len(coupPart)))
                #calcul de la borneMin
                n = len(gPart.graphe.nodes)
                m = len(gPart.graphe.edges)                
                degres = gPart.degresSommet()
                b1 = np.ceil(m / max(degres.values()))
                b3 = (2 * n - 1 - np.sqrt((2 *n - 1)**2 - 8 * m)) / 2
                b2 = len(coupPart) / 2
                borneMin = len(couvPart) + max(b1, b2, b3)                  
                if debug:
                    print("bornes :", borneMin, borneMax)
                #on ajoute les couvertures partiels a la pile que si on a la 
                #possibilité de trouver la solution maximale
                if borneMin <= borneMax:
                    #on ajoute les voisins de u
                    pile.append(couvPart | gPart.voisinsSommet(u))
                    #eliminations de sommet de degre 1
                    if degres[u] != 1 or not elimDegre1:
                        pile.append(couvPart | {u})
            #sinon on est au cas de base, on voit si la taille de la couverture
            #est plus petite que ce qu'on avait déjà
            else:
                couvMin = couvPart if len(couvPart) < len(couvMin) else couvMin
                borneMax = len(couvMin)
        return couvMin, cpt
    
    
    
    
    
    
    
    
        