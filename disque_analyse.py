

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

class parametres():
    Re = 0.25 #[m] rayon externe du disque de frein
    Ri = (2*Re)/3 #[m] rayon minimal où il y a propagation de température
    k = 70 #[W/m*K] coefficient conductivité thermique du matériau du disque de frein
    Cp = 480 #[J/kg*K] capacité calorifique du matériau du disque de frein
    rho = 7200 #[kg/m^3] densité
    Tair = 293.15  #[K] Température infini de l'air
    h = 10 # [W/m^2*K] coefficient de convection thermique
    tfrein = 10 #[s] temps freinage pour génération chaleur
    tatt = 5 #[s] temps attente pour T max
    Tmax = 425+273.15 #[K] T maximum sécuritaire
    n = 100 # Nombre de noeuds [-]
    dr = (Re)/(n-1) #Pas en espace [m]
      
prm = parametres()


# trois cas de génération de chaleur q [W/m^3] pour [faible, fort, urgence]
q = [(3*10**7),(6*10**7),(1.3*10**8)]

# Méthode de différences finies

<<<<<<< Updated upstream
# Truc pour graph
=======
# 3 cas de génération de chaleur q [W/m^3] pour [faible, fort, urgence]
q = [(3*10**7),(6*10**7),(1.3*10**8)]
>>>>>>> Stashed changes
labels = ["Freinage faible", "Freinage fort", "Freinage d'urgence"]
colors = ["blue", "orange", "red"]

plt.figure(figsize=(10, 6))

# Courbes pour chaque cas
for i, qdot in enumerate(q): 
    r, sol, Ttot = mdf(prm, qdot)
    print(f"T max avec {labels[i]}: {round((max(sol)-273.15), 2)} °C")
    plt.plot(r, (sol-273.15), label=labels[i], color=colors[i], linewidth=2)

# Courbe à 425 Celcius

y_max = np.full(prm.n, prm.Tmax-273.15)
x = np.linspace(0, prm.Re, prm.n)
plt.plot(x , y_max, label='température maximale permise de 425 °C')

# Graphique
plt.title("Distribution radiale de la température pour différents cas de freinage à 15 sec", fontsize=14)
plt.xlabel("Rayon [m]", fontsize=12)
plt.ylabel("Température [°C]", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()
<<<<<<< Updated upstream

=======
plt.show()
 

# Représentation graphique

# Sélectionner un cas de freinage (ici, urgent)
qdot = q[2]  # q[2] correspond à freinage urgent
r, sol, Ttot = mdf(prm, qdot)

# Conversion des résultats en une grille polaire
theta = np.linspace(0, 2 * np.pi, 360)  # Angles de 0 à 360 degrés
R, Theta = np.meshgrid(r, theta)  # Grille polaire étendue

# Étendre la température : disque jusqu'à 0.25 m, Tair au-delà
T_extended = np.full_like(R, prm.Tair)  # Initialiser tout à Tair
T_extended[:, :len(r)] = np.tile(sol, (len(theta), 1))  # Mettre la température calculée pour r ≤ 0.25

# Conversion en coordonnées cartésiennes pour le tracé
X = R * np.cos(Theta)
Y = R * np.sin(Theta)

# Création de la heatmap
plt.figure(figsize=(8, 8))
heatmap = plt.pcolormesh(X, Y, T_extended - 273.15, shading='auto', cmap='coolwarm')  # Conversion en °C
plt.colorbar(heatmap, label="Température [°C]")  # Barre de couleur pour les températures

# Ajouts sur le Graphique
plt.title("Heatmap de la température sur le disque de frein (freinage urgent)", fontsize=12)
plt.xlabel("Position X [m]", fontsize=10)
plt.ylabel("Position Y [m]", fontsize=10)
plt.axis("equal")
plt.xlim([-0.3, 0.3])  # Étendre les limites pour inclure la région autour
plt.ylim([-0.3, 0.3])
plt.grid(False)
plt.tight_layout()
>>>>>>> Stashed changes
plt.show()

# Verification: posons des qdot inférieurs

# qdot = q[0]

# sim = mdf(prm,qdot)

# x = sim[0]
# y = sim[1]

# # ## Représentation graphique dans un disque circulaire
# theta = np.linspace(0, 2 * np.pi, 100)  # Angle pour les coordonnées polaires
# r_grid, theta_grid = np.meshgrid(r, theta)  # Grille en coordonnées polaires

# # ## Conversion vers les coordonnées cartésiennes
# x = r_grid * np.cos(theta_grid)
# y = r_grid * np.sin(theta_grid)

# # ## Température étendue sur les angles pour la visualisation
# T_grid = np.tile(T, (len(theta), 1))