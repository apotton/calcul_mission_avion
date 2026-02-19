from enregistrement.Enregistrement import Enregistrement
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from missions.Mission import Mission
from inputs.Inputs import Inputs
import matplotlib.pyplot as plt
from avions.Avion import Avion
import numpy as np
import timeit


A320 = Avion()
test_atmos  = Atmosphere()
Saving = Enregistrement()


tstart = timeit.default_timer()

Saving.reset()

# Coeur du logiciel
Mission.Principal(A320, test_atmos, Saving)

tend = timeit.default_timer()

temps_total = (tend - tstart)

print(f"Temps pour une boucle complète: {temps_total:.4f} secondes")
print("Essence mission: " + str(A320.Masse.getFuelMission()) + " kg")
print("Essence réserve: " + str(A320.Masse.getFuelReserve()) + " kg")



# print("Taille tableau: " + str(Saving.counter))


Saving.cut()

plt.figure()
plt.plot(Saving.data["l"]/Constantes.conv_NM_m, Saving.data["Mach"])
plt.xlabel("Distance parcourue (NM)")
plt.ylabel("Mach")
plt.show()

plt.figure()
plt.plot(Saving.data["l"]/Constantes.conv_NM_m, Saving.data["h"]/Constantes.conv_ft_m)
plt.xlabel("Distance parcourue (NM)")
plt.ylabel("Altitude (ft)")
plt.show()

plt.figure()
plt.plot(np.log10(Saving.data_simu["ecart_mission"]))
plt.show()

# plt.figure()
# plt.plot(Saving.data_simu["l_descent"])
# plt.plot(Saving.data_simu["l_descent_diversion"])
# plt.show()

# plt.figure()
# plt.plot(Saving.data_simu["FB_mission"])
# plt.show()


# Profilage : python -m cProfile -o output.prof alexandre.py
# Visualisation du profilage : snakeviz output.prof