import numpy as np


def mdf(prm, num_points, qdot, %vecteur%, delta_t)

    """Fonction simulant avec la méthode des différences finies

    Entrées:
        - prm : Objet class parametres()
            - T_inf : Température à l'intérieur de la conduite [K]
            - k     : Conductivité thermique [W*m^-1*K^-1]
            - h     : Coefficient de convection thermique [W*m^-2*K^-1]
            - R     : Rayon du disque de frain [m]
            - N     : Nombre de noeuds [-]
            - qdot  : Génération de chaleur [W (m^-3)]

    Sortie (dans l'ordre énuméré ci-bas):
        - Vecteur (array) de dimension N composé de la position radiale à laquelle les 
          températures sont calculées, où N le nombre de noeuds.

        - Vecteur (array) de dimension N composé de la température en fonction du rayon, 
          où N le nombre de noeuds
    """
    # Création des matrices vide A et B
    A = np.zeros((num_points, num_points))
    B = np.zeros(num_points)
    # création du vecteur des positions sur le disque en fonction de R
    delta_r = R / (num_points - 1)
    position_r = np.linspace(0, R, num_points)