

import numpy as np

def mdf(prm, q):
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
        - q : 
    Sortie (dans l'ordre énuméré ci-bas):
        - r : Vecteur (array) de dimension N composé de la position radiale à laquelle les températures sont calculées, où N le nombre de noeuds.
        - sol : Vecteur (array) de dimension N composé de la température en fonction du rayon, où N le nombre de noeuds
        -Ttot : Vecteur (array) de dimension N*15 composé des vecteurs sol mis ensemble par vstack
    """

    # Fonction à écrire

    A = np.zeros([prm.n,prm.n])
    b = np.zeros(prm.n)
    r = np.linspace(0, prm.Re, prm.n)

    #t= np.zeros(prm.n)
    tempe_init = np.full(prm.n, prm.Tair)
    tempe_avant = tempe_init
    Ttot= []
    t=0
   

    dt = (prm.tfrein + prm.tatt) / (prm.n -1)

    A[0,0]= -3
    A[0,1]= 4
    A[0,2]= -1
    
    
    A[-1,-1]= ((-3*prm.k)/(2*prm.dr))-prm.h
    A[-1,-2]= (4*prm.k)/(2*prm.dr)
    A[-1,-3]= (-prm.k)/(2*prm.dr)
    
    
    b[0] = 0
    b[-1] = -prm.h * prm.Tair
    

    while t < (prm.tfrein + prm.tatt):
    
        if t < prm.tfrein :
            for i in range (1,(prm.n)-1):
                if r[i] < prm.Ri: 
                    q_local = 0

                else:
                    q_local = q

                A[i,i-1]= ((-prm.k * dt) / (prm.rho * prm.Cp * prm.dr**2)) + ((prm.k * dt) / (2 * prm.rho * prm.Cp * prm.dr * r[i]))
                A[i,i]= 1 + ((2 * prm.k * dt) / (prm.rho * prm.Cp * prm.dr**2)) + ((100 * prm.h * r[i]**2 * dt) / (prm.rho * prm.Cp))
                A[i,i+1]= -((prm.k * dt) / (prm.rho * prm.Cp * prm.dr**2)) - ((prm.k * dt) / (2 * prm.rho * prm.Cp * prm.dr * r[i]))
                b[i] = tempe_avant[i] + ( ( q_local * dt ) / (prm.rho * prm.Cp ) ) + ( 100 * prm.h * r[i]**2 * dt * prm.Tair) / ( prm.rho * prm.Cp )
        
        else:
            q_local = 0
            
        sol= np.linalg.solve(A,b)
        Ttot.append(sol)  #stack les sols pour voir evol en fct du temps
        tempe_avant = sol #ecraser vect_avant avec sol précédente
        t += dt

    return r, sol, np.array(Ttot) #quoi dautre? vecteur temps?

