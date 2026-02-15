from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from missions.Mission import Mission
from inputs.Inputs import Inputs
import matplotlib.pyplot as plt
from avions.Avion import Avion
import numpy as np
import timeit




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
#         A320.Moteur.Calculate_F_Descent()            # Calcule la poussée
#         poussees_ligne.append(A320.Moteur.getF() / 1000)  # Stocke la poussée en kN
#         # A320.Moteur.Calculate_SFC_Descent() #(A320.Moteur.getF()/2)            # Calcule la poussée
#         # poussees_ligne.append(A320.Moteur.getSFC() / 1000)  # Stocke la poussée en kN
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

A320 = Avion()
test_atmos  = Atmosphere()

# def f():
#     A320 = Avion()
#     Mission.Principal(A320, test_atmos)

# print(timeit.timeit(f, number=1))


tstart = timeit.default_timer()

Enregistrement.reset()

# Coeur du logiciel
Mission.Principal(A320, test_atmos)

tend = timeit.default_timer()

temps_total = (tend - tstart)

print(f"Temps pour une boucle complète: {temps_total:.4f} secondes")
print("Essence mission: " + str(A320.Masse.getFuelMission()) + " kg")
print("Essence réserve: " + str(A320.Masse.getFuelReserve()) + " kg")



# print("Taille tableau: " + str(Enregistrement.counter))


Enregistrement.cut()

# plt.figure()
# plt.plot(Enregistrement.data["t"]/60, Enregistrement.data["CAS"])
# plt.show()

# plt.figure()
# plt.plot(Enregistrement.data["t"]/60, Enregistrement.data["h"])
# plt.show()

# plt.figure()
# plt.plot(np.log10(Enregistrement.data_simu["ecart_mission"]))
# plt.show()

# plt.figure()
# plt.plot(Enregistrement.data_simu["l_descent"])
# plt.plot(Enregistrement.data_simu["l_descent_diversion"])
# plt.show()

# plt.figure()
# plt.plot(Enregistrement.data_simu["FB_mission"])
# plt.show()


# Profilage : python -m cProfile -o output.prof alexandre.py
# Visualisation du profilage : snakeviz output.prof