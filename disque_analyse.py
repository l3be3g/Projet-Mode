

"""
Created on Tue Nov 26 11:59:49 2024

@author: maevasigouin
"""

import numpy as np
import matplotlib.pyplot as plt

try:
    from code_projet_disquefrein import *
except:
    pass

#------------------------------------------------------------------------------
# Code principal pour l'analyse des résultats
# On fait appel aux fonctions programmées dans code_projet_disquefrein.py afin de
# calculer la température dans lau travers du disque selon le rayon. Des graphiques sont générés pour
# visualiser les résultats.
#------------------------------------------------------------------------------

# Assignation des paramètres
# ATTENTION! Ne pas changer le nom des attributs, seulement les valeurs
class parametres():
    Re = 0.25 #[m] rayon externe du disque de frein
    Ri = (2*Re)/3 #[m] rayon minimal où il y a propagation de température
    k = 70 #[W/m*K] coefficient conductivité thermique du matériau du disque de frein
    Cp = 480 #[J/kg*K] capacité calorifique du matériau du disque de frein
    rho = 7200 #[kg/m^3] densité
    Tair = 293.15 #[K] Température infini de l'air
    h = 10 # [W/m^2*K] coefficient de convection thermique
    tfrein = 10 #[s] temps freinage pour génération chaleur
    tatt = 5 #[s] temps attente pour T max
    Tmax = 425 #[K] T maximum sécuritaire
    n = 100 # Nombre de noeuds [-]
    dr = (Re-Ri)/(n-1) #Pas en espace [m]
      
prm = parametres()


# trois cas de génération de chaleur q [W/m^3] pour [faible, fort, urgence]
q = [(3*10**7),(6*10**7),(1.3*10**8)]

# Méthode de différences finies


qdot=q[1]
sim=mdf(prm, qdot)
y = sim[1]
x = sim[0]

plt.plot(x, y)


## Représentation graphique dans un disque circulaire
#theta = np.linspace(0, 2 * np.pi, 100)  # Angle pour les coordonnées polaires
#r_grid, theta_grid = np.meshgrid(r, theta)  # Grille en coordonnées polaires

## Conversion vers les coordonnées cartésiennes
#x = r_grid * np.cos(theta_grid)
#y = r_grid * np.sin(theta_grid)

## Température étendue sur les angles pour la visualisation
#T_grid = np.tile(T, (len(theta), 1))
