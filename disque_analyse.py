
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
    Re = 0.25          #[m] Rayon externe du disque de frein
    Ri = (2*Re)/3      #[m] Rayon minimal où il y a propagation de température
    k = 70             #[W/m*K] Coefficient conductivité thermique du matériau du disque de frein
    Cp = 480           #[J/kg*K] Capacité calorifique du matériau du disque de frein
    rho = 7200         #[kg/m^3] Densité
    Tair = 293.15      #[K] Température infini de l'air
    h = 10             #[W/m^2*K] Coefficient de convection thermique
    tfrein = 10        #[s] Temps freinage pour génération chaleur
    tatt = 5           #[s] Temps attente pour T max
    Tmax = 425+273.15  #[K] T maximum sécuritaire
    n = 100            #[-] Nombre de noeuds
    dr = (Re)/(n-1)    #[m] Pas en espace 
      
prm = parametres()

# Méthode de différences finies


# 3 cas de génération de chaleur q [W/m^3] pour [faible, fort, urgence]
q = [(3*10**7),(6*10**7),(1.3*10**8)]
labels = ["Freinage faible", "Freinage fort", "Freinage d'urgence"]
colors = ["blue", "orange", "red"]


# Tracage des courbes pour chaque cas
for i, qdot in enumerate(q): 
    r, sol, Ttot = mdf(prm, qdot)
    print(f"T max avec {labels[i]}: {round((max(sol)-273.15), 2)} °C")
    plt.plot(r, (sol-273.15), label=labels[i], color=colors[i], linewidth=2)

# Ajout Courbe à 425 Celcius
y_max = np.full(prm.n, prm.Tmax-273.15)
x = np.linspace(0, prm.Re, prm.n)
plt.plot(x , y_max, label='température maximale permise de 425 °C')

# Graphique

plt.title("Distribution radiale de la température pour différents cas de freinage à 15 sec", fontsize=10)
plt.xlabel("Rayon [m]", fontsize=10)
plt.ylabel("Température [°C]", fontsize=10)
plt.legend(fontsize=9)
plt.grid(True)
plt.tight_layout()
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

plt.show()

# Verification: posons un Ri inférieur (R/3)

#bla bla bla