from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from missions.Croisiere import Croisiere
from missions.Descente import Descente
from missions.Montee import Montee
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

Inputs.Aero_simplified = False

# def f():
#     A320 = Avion()
#     test_atmos  = Atmosphere()
#     Montee.Monter(A320, test_atmos)
#     Enregistrement.reset()
#     A320.Aero.setMach_t(0.78)
#     A320.set_h(11000)
#     Descente.Descendre(A320, test_atmos)

# print(timeit.timeit(f, number=1))
tstart = timeit.default_timer()


Enregistrement.reset()
Enregistrement.enregistrement_descente = False
A320.setupDescente()
Descente.Descendre(A320, test_atmos)
Enregistrement.enregistrement_descente = True
l_descent = A320.l_descent
print("Distance de descente: " + str(A320.l_descent / 1000) + " km")

N = 10
for i in range(N):
    A320 = Avion()
    A320.l_descent = l_descent
    Montee.Monter(A320, test_atmos)
    Croisiere.Croisiere(A320, test_atmos)
    Descente.Descendre(A320, test_atmos)
    # Enregistrement.reset()

tend = timeit.default_timer()

temps_moyen = (tend - tstart) / N

print(f"Temps moyen pour une montée + croisière + descente : {temps_moyen:.4f} secondes")


print("Taille tableau: " + str(Enregistrement.counter))


Enregistrement.cut()

plt.figure()

# plt.plot(Enregistrement.data["t"], Enregistrement.data["F_N"])
plt.plot(Enregistrement.data["t"], Enregistrement.data["l"])

plt.show()


print("Test complete.")

# Profilage : python -m cProfile -o output.prof alexandre.py
# Visualisation du profilage : snakeviz output.prof