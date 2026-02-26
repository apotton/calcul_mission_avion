from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from missions.PointPerformance import PointPerformance
from missions.Mission import Mission
from inputs.Inputs import Inputs
import matplotlib.pyplot as plt
from avions.Avion import Avion
import numpy as np
import timeit

inputs = Inputs()
A320 = Avion(inputs)
test_atmos  = Atmosphere(inputs)
Saving = Enregistrement()

# Coeur du logiciel
Mission.Principal(A320, test_atmos, Saving, inputs)

Saving.cut()

# plt.figure()
# plt.plot(Saving.data["l"]/Constantes.conv_NM_m, Saving.data["Mach"])
# plt.xlabel("Distance parcourue (NM)")
# plt.ylabel("Mach")
# plt.show()

# plt.figure()
# plt.plot(Saving.data["l"]/Constantes.conv_NM_m, Saving.data["h"]/Constantes.conv_ft_m)
# plt.xlabel("Distance parcourue (NM)")
# plt.ylabel("Altitude (ft)")
# plt.show()

plt.figure()
plt.plot(Saving.data["l_cruise"]/Constantes.conv_NM_m, Saving.data["ECCF"])
plt.xlabel("Distance croisière (NM)")
plt.ylabel("SGR")
plt.show()

# plt.figure()
# plt.plot(A320.Aero.getMach(), A320.Aero.getCz())
# plt.plot(A320.Aero.getMach(), A320.Aero.getCx())
# plt.show()

# A320.Aero.convertMachToTAS(test_atmos)

# plt.figure()
# plt.plot(A320.Aero.getMach(), A320.Moteur.getF())
# plt.show()
# print("Mach avion: " + str(A320.Aero.getMach()))

# plt.figure()
# plt.plot(Saving.data["l"]/Constantes.conv_NM_m, Saving.data["Cx"])
# plt.xlabel("Distance parcourue (NM)")
# plt.ylabel("Cx")
# plt.show()

# plt.figure()
# plt.plot(Saving.data["l"]/Constantes.conv_NM_m, Saving.data["Cz"])
# plt.xlabel("Distance parcourue (NM)")
# plt.ylabel("Cz")
# plt.show()

# plt.figure()
# plt.plot(Saving.data["l"]/Constantes.conv_NM_m, Saving.data["f"])
# plt.xlabel("Distance parcourue (NM)")
# plt.ylabel("Finesse")
# plt.show()

# plt.figure()
# plt.plot(Saving.data["l"]/Constantes.conv_NM_m, Saving.data["m"])
# plt.xlabel("Distance parcourue (NM)")
# plt.ylabel("Masse (kg)")
# plt.show()

# plt.figure()
# plt.plot(Saving.data["l"]/Constantes.conv_NM_m, Saving.data["h"]/Constantes.conv_ft_m)
# plt.xlabel("Distance parcourue (NM)")
# plt.ylabel("Altitude (ft)")
# plt.show()

# plt.figure()
# plt.plot(np.log10(Saving.data_simu["ecart_mission"]))
# plt.show()

# plt.figure()
# plt.plot(Saving.data_simu["l_descent"])
# plt.plot(Saving.data_simu["l_descent_diversion"])
# plt.show()

# plt.figure()
# plt.plot(Saving.data_simu["FB_mission"])
# plt.show()


# Profilage : python -m cProfile -o output.prof alexandre.py
# Visualisation du profilage : snakeviz output.prof


# Calcul de Point Performance
# PointPerformance.Performance(A320, test_atmos)