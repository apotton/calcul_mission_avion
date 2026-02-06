from constantes.Constantes import Constantes
from avions.Avion import Avion
from atmosphere.Atmosphere import Atmosphere
from enregistrement.Enregistrement import Enregistrement
from missions.Mission import Mission
import matplotlib.pyplot as plt
import numpy as np
import timeit

A320 = Avion()


test_atmos  = Atmosphere()


# # Test du moteur un peu plus en détail: poussée à différentes altitudes et Mach (figure 2D)
# valeurs_mach = [i/100 for i in range(0, 90)]  # Mach de 0.0 à 0.8
# altitudes_ft = range(0, 40000, 1000)  # Altitudes en pieds

# # tableau 2D des poussées
# poussees_2D = []


# # Boucle 2D sur les altitudes et Mach, indéxée sur les indices des tableaux

# for h_ft in altitudes_ft:
#     poussees_ligne = []
#     for mach in valeurs_mach:
#         A320.set_h(h_ft * Constantes.conv_ft_m)  # Met à jour l'altitude de l'avion en mètres
#         A320.Aero.Mach_t = mach                       # Met à jour le Mach de l'avion
#         A320.Moteur.Calculate_F()            # Calcule la poussée
#         # poussees_ligne.append(A320.Moteur.getF() / 1000)  # Stocke la poussée en kN
#         A320.Moteur.Calculate_SFC_climb() #(A320.Moteur.getF()/2)            # Calcule la poussée
#         poussees_ligne.append(A320.Moteur.getSFC() / 1000)  # Stocke la poussée en kN
#     poussees_2D.append(poussees_ligne)
# # Convertir en numpy array pour faciliter le tracé
# poussees_2D = np.array(poussees_2D)

# # Tracé d'une figure en 3D (Mach, altitude, poussée)
# from mpl_toolkits.mplot3d import Axes3D
# fig = plt.figure(figsize=(10, 7))
# ax = fig.add_subplot(111, projection='3d')
# X, Y = np.meshgrid(valeurs_mach, altitudes_ft)
# ax.plot_surface(X, Y, poussees_2D, cmap='viridis')
# ax.set_title('Consommation spécifique du moteur en fonction de l\'altitude et du Mach')
# ax.set_xlabel('Mach')
# ax.set_ylabel('Altitude (ft)')
# plt.show()

mission = Mission()
dt = 1  # Pas de temps en secondes

def f():
    Enregistrement.reset()
    mission.Montee.climb_sub_h_1500_ft(A320, test_atmos, dt)
    mission.Montee.climb_Palier(A320, test_atmos, dt)
    mission.Montee.climb_iso_CAS(A320, test_atmos, dt)
    mission.Montee.climb_iso_Mach(A320, test_atmos, dt)

print(timeit.timeit(f, number=1))


# mission.Montee.climb_sub_h_1500_ft(A320, test_atmos, dt)
# mission.Montee.climb_Palier(A320, test_atmos, dt)
# mission.Montee.climb_iso_CAS(A320, test_atmos, dt)
# mission.Montee.climb_iso_Mach(A320, test_atmos, dt)
print("Taille tableau: " + str(Enregistrement.counter))

Enregistrement.cut()

plt.figure()

plt.plot(Enregistrement.data["t"], Enregistrement.data["F_N"]) 

plt.show()

print("Test complete.")