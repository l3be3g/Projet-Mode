#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 11:41:11 2024

@author: maevasigouin
"""

import numpy as np

def mdf(prm):
    """Fonction simulant avec la méthode des différences finies

    Entrées:
        - prm : Objet class parametres()
            - Re : Rayon externe du disque de frein [m]
            - Ri : Rayon minimal où il y a propagation de température [m]
            - k : Conductivité thermique [W / m * K]
            - Cp : Capacité calorifique [J / kg * K]
            - rho : Densité [kg / m3]
            - Tair : Température infinie de l'air
            - h : Coefficient de convection thermique [W / m^2 * K]
            - tfrein : Temps de freinage [s]
            - tatt : Temps attente pour Tmax [s]
            - Tmax : Température maximum sécuritaire [K]
            - n : Nombre de noeuds [-]
            - dr : Pas en espace [m]

    Sortie (dans l'ordre énuméré ci-bas):
        - Vecteur (array) de dimension N composé de la position radiale à laquelle les températures sont calculées, où N le nombre de noeuds.
        - Vecteur (array) de dimension N composé de la température en fonction du rayon, où N le nombre de noeuds
    """

    # Fonction à écrire
    
    A = np.zeros([prm.n,prm.n])
    b = np.zeros(prm.n)
    
    A[0,0]= -3
    A[0,1]= 4
    A[0,2]= -1
    
    
    A[-1,-1]= ((-3*prm.k)/(2*prm.dr))-prm.h
    A[-1,-2]= (4*prm.k)/(2*prm.dr)
    A[-1,-3]= (-prm.k)/(2*prm.dr)
    
    
    b[0] = 0
    b[-1] = -prm.h * prm.Tair
    
    r = np.linspace(prm.Ri,prm.Re,prm.n)
    
    dt = #INITIALISER
    
    for i in range (1,(prm.n)-1):
        A[i,i-1]= ((-prm.k * dt) / (prm.rho * prm.Cp * prm.dr**2)) + ((prm.k * dt) / (2 * prm.rho * prm.Cp * prm.dr * r[i]))
        A[i,i]= 1 + ((2 * prm.k * dt) / (prm.rho * prm.Cp * prm.dr**2)) + ((100 * prm.h * r[i]**2 * dt) / (prm.rho * prm.Cp))
        A[i,i+1]= ((-prm.k * dt) / (prm.rho * prm.Cp * prm.dr**2)) + ((-prm.k * dt) / (2 * prm.rho * prm.Cp * prm.dr * r[i]))
    
    sol= np.linalg.solve(A,b)

    return r, sol

