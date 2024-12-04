

import numpy as np

def mdf(prm, q):
    """Fonction simulant avec la méthode des différences finies

    Entrées:
        - prm : Objet class parametres()
            -Re = 0.25 [m] Rayon externe du disque de frein
            -Ri [m] Rayon minimal où il y a propagation de température
            -k [W/m*K] Coefficient conductivité thermique du matériau du disque de frein
            -Cp [J/kg*K] Capacité calorifique du matériau du disque de frein
            -rho [kg/m^3] Densité
            -Tair [K] Température infini de l'air
            -h [W/m^2*K] Coefficient de convection thermique
            -tfrein [s] Temps freinage pour génération chaleur
            -tatt [s] Temps attente pour T max
            -Tmax [K] T maximum sécuritaire
            -n [-] Nombre de noeuds
            -dr [m] Pas en espace
        - q : [W/m^3] génération de chaleur [faible, fort, urgence]

    Sortie (dans l'ordre énuméré ci-bas):
        - r : Vecteur (array) de dimension N composé de la position radiale à laquelle les températures sont calculées, où N le nombre de noeuds.
        - sol : Vecteur (array) de dimension N composé de la température en fonction du rayon, où N le nombre de noeuds
        -Ttot : Vecteur (array) de dimension N*15 composé des vecteurs sol mis ensemble par vstack
    """


    # Initialisation des matrice A, b 
    A = np.zeros([prm.n,prm.n])
    b = np.zeros(prm.n)

    # Création d'un vecteur avec un nombre n de rayon et des valeurs de 0 au rayon externe
    r = np.linspace(0, prm.Re, prm.n)

    # Initalisation de la matrice de temps 
    tempe_init = np.full(prm.n, prm.Tair)
    tempe_avant = tempe_init
    Ttot= []
    t=0
   
    # Calcul du pas de temps, temps total de la simulation divisé par le nombre d'intervalles
    dt = (prm.tfrein + prm.tatt) / (prm.n -1)

    # Première condition frontière 
    # Matrice A
    A[0,0]= -3
    A[0,1]= 4
    A[0,2]= -1

    # Matrice B
    b[0] = 0

    # Deuxième condition frontière 
    # Matrice A
    A[-1,-1]= ((-3*prm.k)/(2*prm.dr))-prm.h
    A[-1,-2]= (4*prm.k)/(2*prm.dr)
    A[-1,-3]= (-prm.k)/(2*prm.dr)

    # Matrice B
    b[-1] = -prm.h * prm.Tair

    # Tant que le temps est inférieur à la somme du temps de freinage et du temps d'attente ( = 15 secondes)
    while t <= (prm.tfrein + prm.tatt):
        for i in range(1, prm.n - 1):
            # Si le temps est inférieur à 10 secondes et le rayon est supérieur au rayon inférieur
            # q est égale à la une valeur en fonction du freinage

            if t < prm.tfrein and r[i] >= prm.Ri:
                q_local = q

            # Sinon q est égale à zéro
            else:
                q_local = 0

            # Matrice A
            A[i, i - 1] = ((-prm.k * dt) / (prm.rho * prm.Cp * prm.dr**2)) + ((prm.k * dt) / (2 * prm.rho * prm.Cp * prm.dr * r[i]))
            A[i, i] = 1 + ((2 * prm.k * dt) / (prm.rho * prm.Cp * prm.dr**2)) + ((100 * prm.h * r[i]**2 * dt) / (prm.rho * prm.Cp))
            A[i, i + 1] = -((prm.k * dt) / (prm.rho * prm.Cp * prm.dr**2)) - ((prm.k * dt) / (2 * prm.rho * prm.Cp * prm.dr * r[i]))

            # Vecteur b
            b[i] = tempe_avant[i] + ((q_local * dt) / (prm.rho * prm.Cp)) + ((100 * prm.h * r[i]**2 * dt * prm.Tair) / (prm.rho * prm.Cp))

        # Résolution 
        sol = np.linalg.solve(A, b) #Résolution avec fonction numpy
        Ttot.append(sol)  # Stocker la solution dans le temps
        tempe_avant = sol  # Mise à jour prochaine itération
        t += dt # Pas du dt pour avancer dans le temps

    return r, sol, Ttot 
