from constantes.Constantes import Constantes
from avions.Avion import Avion
from atmosphere.Atmosphere import Atmosphere
from missions.Test_Descent import Mission
import matplotlib.pyplot as plt
import numpy as np
import time

A320 = Avion("Airbus_A320.csv")

# print(A320.getWingspan())
# print(A320.getName())
# print(A320.getLength())
# print(A320.getHeight())

# print(Constantes.g)
# print(Atmosphere.T0_K)

test_atmos  = Atmosphere()
test_atmos.CalculateRhoPT(15000)
# print("At 15000 m: rho = {:.4f} kg/m³, p = {:.2f} Pa, T = {:.2f} K".format(test_atmos.rho_t, test_atmos.P_t, test_atmos.T_t))

# print("Cx_t = " + str(A320.Aero.Cx_t))

# print("Masse actuelle = " + str(A320.Masse.getCurrentMass()) + " kg")

# #Test Aero

# A320.Aero.CalculateCz(test_atmos)
# Cz = A320.Aero.getCz()

# A320.Aero.CalculateCxClimb_Simplified()
# Cx_Climb = A320.Aero.getCx()

# A320.Aero.CalculateCxCruise_Simplified()
# Cx_Cruise = A320.Aero.getCx()

# A320.Aero.CalculateCxDescent_Simplified()
# Cx_Descent = A320.Aero.getCx()

# print(Cz)
# print(Cx_Climb)
# print(Cx_Cruise)
# print(Cx_Descent)

# A320.Aero.CalculateAll(test_atmos)

# # Test de l'obtention de l'envergure dans la classe avion
# env = A320.getEnvergure()
# print("Envergure de l'avion : " + str(env) + " m")

# # Test de l'obtention de l'envergure via la méthode getEnvergure()
# env_method = A320.getEnvergure()
# print("Envergure de l'avion via méthode : " + str(env_method) + " m")

# Test du calcul complet de Cx
# A320.Aero.CalculateCx(test_atmos)
# Cx_complete = A320.Aero.getCx()
# print("Cx complet calculé : " + str(Cx_complete))

# # Test du calcul de Cz buffet
# cz_buffet = A320.Aero.CalculateCzBuffet()
# print("Cz buffet calculé : " + str(A320.Aero.getCzBuffet()))

# # Test du calcul de Cz
# A320.Aero.CalculateCz(test_atmos)
# print("Cz calculé : " + str(A320.Aero.getCz()))

# # Test du calcul de la TAS
# tas = A320.Aero.getTAS()
# print("TAS calculée : " + str(tas) + " m/s")

# # Test du calcul du SFC
# A320.Moteur.Calculate_SFC(15000 / Constantes.conv_ft_m)
# sfc = A320.Moteur.getSFC()
# print("SFC actuel : " + str(sfc) + " kg/(N.s)")

# # Test du calcul de la poussée maximale en montée
# A320.Moteur.Calculate_F()
# thrust = A320.Moteur.getF()
# print("Poussée maximale en montée : " + str(thrust) + " N")

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

debut = time.time()

mission.climb_sub_h_1500(A320, Atmosphere=test_atmos, dt = 5)
mission.climb_Palier(A320, Atmosphere=test_atmos, dt = 5)
mission.climb_iso_CAS(A320, Atmosphere=test_atmos, dt = 5)
mission.climb_iso_Mach(A320, Atmosphere=test_atmos, dt = 5)

fin = time.time()

print("Temps de calcul montée: " + str(fin - debut) + " s")

print("Taille tableau:" + str(len(mission.history["Vz"])))
# print(mission.history["h"])

plt.figure()

# plt.plot(mission.history["h"])
# plt.plot(mission.history["pente"] )
plt.plot(mission.history["Mach"])

plt.show()


print("Altitude pas finale (ft): " + str(mission.history["h"][-2] / Constantes.conv_ft_m))
print("Altitude finale (ft): " + str(mission.history["h"][-1] / Constantes.conv_ft_m))

print("Test complete.")